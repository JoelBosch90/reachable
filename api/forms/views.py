# Import dependencies.
import json
import os
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

    def post(self, request, format=None):
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
            userSerializer.save()

        # Get access to the user object.
        user = get_object_or_404(User, email=request.data['email'])

        # Create a new form.
        formSerializer = FormSerializer(data={
            'user': user.email,
            'name': request.data['name'],
            'description': request.data['description']
        })

        # If it is not a valid form request, let the client know.
        formSerializer.is_valid(raise_exception=True)

        # Store the new form.
        form = formSerializer.save()

        # Add a message input to the form.
        inputSerializer = InputSerializer(data={
            'name': "Message",
            'title': "Add a message to send to the form's owner.",
            'form': form.id
        })

        # If it is not a input form request, let the client know.
        inputSerializer.is_valid(raise_exception=True)

        # Otherwise, store it.
        inputSerializer.save()

        # Create a new link for this form.
        formLinkSerializer = FormLinkSerializer(data={
            'form': form.id
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

    def post(self, request, format=None):
        """
        Respond to a form.
        """

        # Get the form.
        formLink = get_object_or_404(FormLink, key=request.data['link'])

        # Check if the owner has disabled the form. We should no longer be
        # sending responses.
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

    def get(self, request, key, format=None):
        """
        Try to confirm the form, then link to the associated form link's share
        page.
        """

        # Get the confirmation link.
        confirmationLink = get_object_or_404(FormConfirmationLink, key=key)

        # Explain to the user that this link has expired.
        if confirmationLink.hasExpired():
            return HttpResponseRedirect(redirect_to=f"{os.getenv('CLIENT_URL')}/form/expired")

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

    def get(self, request, key, format=None):
        """
        Disable the form, then redirect to a proper
        """

        # Get the disable link.
        disableLink = get_object_or_404(FormDisableLink, key=key)

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

    def get(self, request, key, format=None):
        """
        Get the details from a form link.
        """

        # Get the link object.
        formLink = get_object_or_404(FormLink, key=key)

        # Check if the link has expired.
        if formLink.hasExpired():
            return response.Response('expired')

        # If the form has not been confirmed, we should not show it.
        if (not formLink.form.confirmed):
            return response.Response('unconfirmed')

        # If the form has been disabled, we should not show it.
        if (formLink.form.disabled):
            return response.Response('disabled')

        # Construct the response object.
        result = {

            # We need to know which form needs to be submitted.
            'id': formLink.form.id,

            # Add the form's name.
            'name': formLink.form.name,

            # Add the form's description.
            'description': formLink.form.description,

            # We need to know all inputs.
            'inputs': [{
                'name': input.name,
                'title': input.title
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
