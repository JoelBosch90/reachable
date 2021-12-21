# Import dependencies.
import json
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import (
  generics, permissions, response
)
from tools.Mail import (
  FormConfirmationMail, FormResponseMail
)
from .models import (
  User, Form, FormLink, Input
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
        if not formSerializer.is_valid():
            return response.Response(formSerializer.errors)

        # Store the new form.
        form = formSerializer.save()

        # Add a message input to the form.
        inputSerializer = InputSerializer(data={
            'name': "Message",
            'title': "Add a message to send to the form's owner.",
            'form': form.id
        })

        # If it is not a input form request, let the client know.
        if not inputSerializer.is_valid():
            return response.Response(inputSerializer.errors)

        # Otherwise, store it.
        inputSerializer.save()

        # Create a new link for this form.
        formLinkSerializer = FormLinkSerializer(data={
            'form': form.id
        })

        # If we cannot create a link, let the client know.
        if not formLinkSerializer.is_valid():
            return response.Response(formLinkSerializer.errors)

        # Otherwise, store the link.
        link = formLinkSerializer.save()

        # Send a confirmation email.
        FormConfirmationMail().send(user, form)

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
        form = get_object_or_404(Form, id=request.data['form'])

        # Send the response to the owner of the form.
        FormResponseMail().send(form.user, form, request.data['inputs'])

        # Send back a success message.
        return response.Response(True)


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
        if (formLink.expires < timezone.now()):
           return response.Response('expired')

        # Check if there's anything we should verify.
        if (formLink.confirmation):

            # Confirm the form if it has not yet been confirmed.
            if formLink.form.confirmed is None:

                # Update the form.
                formSerializer = FormSerializer(
                    formLink.form,
                    data={'confirmed': timezone.now()},
                    partial=True
                )

                # Save the form update if possible.
                if formSerializer.is_valid():
                    formSerializer.save()

            # Verify the user if the user has not yet been verified.
            if formLink.form.user.verified is None:

                # Update the form's user.
                userSerializer = UserSerializer(
                    formLink.form.user,
                    data={'verified': timezone.now()},
                    partial=True
                )

                # Save the user update if possible.
                if userSerializer.is_valid():
                    userSerializer.save()

        # If the form has not been confirmed, we should not show it.
        if (not formLink.form.confirmed):
          return response.Response(False)

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
