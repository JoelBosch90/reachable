# Import dependencies.
import json
import os
import datetime
import re
from html import escape
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, Http404
from rest_framework import (
  generics, permissions, response
)
from tools.Mail import (
  FormConfirmationMail, FormResponseMail
)
from .models import (
  User, Form, FormLink, FormConfirmationLink, FormDisableLink, Input
)
from .serializers import (
  UserSerializer, FormSerializer, FormLinkSerializer, InputSerializer
)


class FormListView(generics.CreateAPIView):
    """
    This is the endpoint that allows for creating forms.
    """

    # Everyone can create forms.
    permission_classes = [permissions.AllowAny]

    def uniqueFormname(self, name, user):
        """
        Make sure that a form name is unique.
        """

        # We may have to try getting a unique name multiple times.
        while True:

            # First check if this form name is already for this user.
            if (not Form.objects.filter(name=name, user=user).exists()):

                # If so, simply return it.
                return name

            # Regex to find the number in a name. We assume that this number
            # has a format of '(0)' and is at the end of the name.
            regex = r'(?<=\()\d+(?=\)$)'

            # Check if the name already ends in a number.
            match = re.search(regex, name)

            # Did we find a number?
            if match:

                # Extract the number, convert to integer and add 1.
                newNumber = int(match.group(0), base=10) + 1

                # Insert the new number into the name.
                name = re.sub(regex, str(newNumber), name)

            # Otherwise, we need to add a number.
            else:
                name += '(1)'

    def post(self, request):
        """
        Create a new form.
        """

        # Create a serializer for the user.
        userSerializer = UserSerializer(data={
            'email': request.data['email']
        })

        # If the serializer is valid, that means that a user with this email
        # address does not yet exist.
        if userSerializer.is_valid():

            # We should create the user if we don't have it yet.
            user = userSerializer.save()

        # Get access to the user object.
        user = get_object_or_404(User, email=request.data['email'])

        # Create a new form.
        formSerializer = FormSerializer(data={
            'user': user.pk,

            # Make sure that the form's name is unique.
            'name': self.uniqueFormname(request.data['name'], user),
            'description': request.data['description']
        })

        # If it is not a valid form request, let the client know.
        formSerializer.is_valid(raise_exception=True)

        # Store the new form.
        form = formSerializer.save()

        # Add a message input to the form.
        # @todo: We currently only support this input field, but we can make
        # this app much more powerful when we don't!
        inputSerializer = InputSerializer(data={
            'name': "message",
            'label': "Message",
            'hint': "Add a message to send to the owner of this form.",
            'required': True,
            'type': 'textarea',
            'form': form.pk
        })

        # If it is not a input form request, let the client know.
        inputSerializer.is_valid(raise_exception=True)

        # Otherwise, store it.
        inputSerializer.save()

        # Create a new link for this form.
        formLinkSerializer = FormLinkSerializer(data={
            'form': form.pk
        })

        # If we cannot create a link, let the client know.
        formLinkSerializer.is_valid(raise_exception=True)

        # Otherwise, store the link.
        link = formLinkSerializer.save()

        # Send a confirmation email.
        FormConfirmationMail().send(user, link)

        # Send the link back to the client.
        return response.Response(link.key)


class FormResponseView(generics.CreateAPIView):
    """
    This is the endpoint that processes a form response.
    """

    # Everyone can respond to forms.
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Respond to a form.
        """

        # Get the form.
        formLink = get_object_or_404(FormLink, key=request.data['link'])

        # Check if the owner has confirmed this form. We should not yet be
        # sending responses if the form is not confirmed.
        if type(formLink.form.confirmed) is not datetime.datetime:
            return response.Response(False)

        # Check if the owner has disabled the form. We should no longer be
        # sending responses if the form has been disabled.
        if formLink.form.disabled:
            return response.Response(False)

        # Send the response to the owner of the form.
        FormResponseMail().send(formLink, request.data['inputs'])

        # Send back a success message.
        return response.Response(True)


class FormConfirmationView(generics.RetrieveAPIView):
    """
    This is the endpoint that confirms if a form can be activated.
    """

    # A user does not have to be authenticated to confirm a form. The link
    # itself acts as a unique identifier as we only send this link to the
    # form's owner's email address.
    permission_classes = [permissions.AllowAny]

    def get(self, request, key):
        """
        Try to confirm the form, then link to the associated form link's share
        page.
        """

        # Try to get the confirmation link.
        try:
          confirmationLink = FormConfirmationLink.objects.get(key=key)

        # If we cannot find the confirmation link, we should redirect to the
        # website's normal 404 page.
        except FormConfirmationLink.DoesNotExist:
            return HttpResponseRedirect(redirect_to=f"{os.getenv('CLIENT_URL')}/error/notfound")

        # Explain to the user that this link has expired.
        if confirmationLink.hasExpired():
            return HttpResponseRedirect(redirect_to=f"{os.getenv('CLIENT_URL')}/error/expired")

        # Get access to the form object.
        form = confirmationLink.formLink.form

        # Confirm the form if it has not yet been confirmed.
        if form.confirmed is None:

            # Update the form.
            formSerializer = FormSerializer(
                form,
                data={'confirmed': timezone.now()},
                partial=True
            )

            # Save the form update if possible.
            if formSerializer.is_valid():
                formSerializer.save()

        # Verify the user if the user has not yet been verified.
        if form.user.verified is None:

            # Update the form's user.
            userSerializer = UserSerializer(
                form.user,
                data={'verified': timezone.now()},
                partial=True
            )

            # Save the user update if possible.
            if userSerializer.is_valid():
                userSerializer.save()

        # Redirect the user to the form link's share page.
        return HttpResponseRedirect(redirect_to=confirmationLink.formLink.shareUrl())


class FormDisableView(generics.RetrieveAPIView):
    """
    This is the endpoint that disables a form.
    """

    # A user does not have to be authenticated to disable a form. The link
    # itself acts as a unique identifier as we only send this link to the
    # form's owner's email address.
    permission_classes = [permissions.AllowAny]

    def get(self, request, key):
        """
        Disable the form, then redirect to a disabled form.
        """

        # Try to get the disable link.
        try:
          disableLink = FormDisableLink.objects.get(key=key)

        # If we cannot find the disable link, we should redirect to the
        # website's normal 404 page.
        except FormDisableLink.DoesNotExist:
            return HttpResponseRedirect(redirect_to=f"{os.getenv('CLIENT_URL')}/error/notfound")

        # Update the form.
        formSerializer = FormSerializer(
            disableLink.formLink.form,
            data={'disabled': True},
            partial=True
        )

        # Save the form update if possible.
        if formSerializer.is_valid(raise_exception=True):
            formSerializer.save()

        # Redirect the user to the form link's page that should now state that
        # it has been disabled.
        return HttpResponseRedirect(redirect_to=disableLink.formLink.url())


class FormDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    This is the endpoint that allows for retrieving, updating, and destroying
    individual forms.
    """

    # We're using the Form objects.
    queryset = Form.objects.all()

    # We're using the Form serializer.
    serializer_class = FormSerializer

    # Everyone can view forms, but only the user that owns them can modify
    # them.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class FormLinkListView(generics.ListCreateAPIView):
    """
    This is the endpoint that allows for listing and creating links that link
    to forms.
    """

    # We're using the Link objects.
    queryset = FormLink.objects.all()

    # We're using the Link serializer.
    serializer_class = FormLinkSerializer

    # Only the user that owns them can list or create links.
    permission_classes = [permissions.IsAuthenticated]


class FormLinkDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    This is the endpoint that allows for retrieving, updating, and destroying
    individual links to forms.
    """

    # We're using the Link objects.
    queryset = FormLink.objects.all()

    # We're using the Link serializer.
    serializer_class = FormLinkSerializer

    # Only the user that owns them can modify them.
    permission_classes = [permissions.IsAuthenticated]


class FormLinkView(generics.RetrieveAPIView):
    """
    This is the endpoint that allows for retrieving individual form links.
    """

    # We're using the Link objects.
    queryset = FormLink.objects.all()

    # We're using the Link serializer.
    serializer_class = FormLinkSerializer

    # Everyone can view form links.
    permission_classes = [permissions.AllowAny]

    def get(self, request, key):
        """
        Get the details from a form link.
        """

        # Get the link object.
        formLink = get_object_or_404(FormLink, key=key)

        # Check if the link has expired.
        if formLink.hasExpired():
            return HttpResponseRedirect(redirect_to=
                f"{os.getenv('CLIENT_URL')}/error/expired")

        # Construct the response object. Make sure we escape all user generated
        # strings.
        result = {

            # Add the form's name.
            'name': escape(formLink.form.name),

            # Add the form's description.
            'description': escape(formLink.form.description),

            # Pass on if the form's been disabled.
            'disabled': formLink.form.disabled,

            # Pass on if the form's been confirmed yet.
            'confirmed': type(formLink.form.confirmed) is datetime.datetime,

            # We need to know all inputs.
            'inputs': [{
                'name': escape(input.name),
                'label': escape(input.label),
                'hint': escape(input.hint),
                'required': input.required,
                'type': escape(input.type),
            } for input in formLink.form.inputs.all()]
        }

        # Return the dictionary as a JSON object.
        return response.Response(json.dumps(result))


class InputListView(generics.ListCreateAPIView):
    """
    This is the endpoint that allows for listing and creating inputs.
    """

    # We're using the Input objects.
    queryset = Input.objects.all()

    # We're using the Input serializer.
    serializer_class = InputSerializer

    # Everyone can view inputs, but only the user that owns them can modify
    # them.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class InputDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    This is the endpoint that allows for retrieving, updating, and destroying
    individual inputs.
    """

    # We're using the Input objects.
    queryset = Input.objects.all()

    # We're using the Input serializer.
    serializer_class = InputSerializer

    # Everyone can view inputs, but only the user that owns them can modify
    # them.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
