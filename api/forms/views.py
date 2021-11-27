# Import dependencies.
import secrets
import json
from rest_framework import (
  generics, permissions, response
)
from tools.Mail import (
  FormConfirmationMail, FormResponseMail
)
from .models import (
  User, Form, Link, Input
)
from .serializers import (
  UserSerializer, FormSerializer, LinkSerializer, InputSerializer
)


class FormList(generics.CreateAPIView):
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
        user = User.objects.get(email=request.data['email'])

        # Create a new form.
        formSerializer = FormSerializer(data={
            'user': user.email,
            'name': request.data['name'],
            'description': request.data['description']
        })

        # Check that this is a valid form request.
        if formSerializer.is_valid():

            # Store the new form.
            form = formSerializer.save()

            # Add a message input to the form.
            inputSerializer = InputSerializer(data={
                'name': "Message",
                'title': "Add a message to send to the form's owner.",
                'form': form.id
            })

            # Check if the input is valid.
            if inputSerializer.is_valid():

                # If so, store it.
                inputSerializer.save()

            # We want to create a link with a unique key. We will keep trying
            # until we get one.
            while True:

                # Attempt to create a link.
                linkSerializer = LinkSerializer(data={
                    'form': form.id,

                    # We want to use the key in a URL, so it should be URL
                    # safe. It needs to be long enough to be hard to guess and
                    # short enough to be practical in a URL.
                    'key': secrets.token_urlsafe(secrets.choice(range(16,
                                                                      128)))
                })

                # If the link is valid that means the key is unique and we can
                # escape the loop.
                if linkSerializer.is_valid():

                    # Store the link.
                    link = linkSerializer.save()

                    # Send a confirmation email.
                    FormConfirmationMail().send(user, form)

                    # Store the link and send it back to the client.
                    return response.Response(link.key)

        # If it is not a valid form request, let the client know.
        else:
            return response.Response(formSerializer.errors)


class FormResponse(generics.CreateAPIView):
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
        form = Form.objects.get(id=request.data['form'])

        # Send the response to the owner of the form.
        FormResponseMail().send(form.user, form, request.data['inputs'])

        # Send back a success message.
        return response.Response(True)


class FormDetail(generics.RetrieveUpdateDestroyAPIView):
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


class LinkList(generics.ListCreateAPIView):
    """
    This is the endpoint that allows for listing and creating links.
    """

    # We're using the Link objects.
    queryset = Link.objects.all()

    # We're using the Link serializer.
    serializer_class = LinkSerializer

    # Only the user that owns them can list or create links.
    permission_classes = [permissions.IsAuthenticated]


class LinkDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    This is the endpoint that allows for retrieving, updating, and destroying
    individual links.
    """

    # We're using the Link objects.
    queryset = Link.objects.all()

    # We're using the Link serializer.
    serializer_class = LinkSerializer

    # Only the user that owns them can modify them.
    permission_classes = [permissions.IsAuthenticated]


class ConfirmationLink(generics.RetrieveAPIView):
    """
    This is the endpoint that allows for retrieving individual confirmation
    links.
    """

    # @todo: implement.
    pass


class FormLink(generics.RetrieveAPIView):
    """
    This is the endpoint that allows for retrieving individual form links.
    """

    # We're using the Link objects.
    queryset = Link.objects.all()

    # We're using the Link serializer.
    serializer_class = LinkSerializer

    # Everyone can view form links.
    permission_classes = [permissions.AllowAny]

    def get(self, request, key, format=None):
        """
        Get the details from a form link.
        """

        # Get the link object.
        link = Link.objects.get(key=key)

        # Construct the response object.
        result = {

            # We need to know which form needs to be submitted.
            'id': link.form.id,

            # Add the form's name.
            'name': link.form.name,

            # Add the form's description.
            'description': link.form.description,

            # We need to know all inputs.
            'inputs': [{
                'name': input.name,
                'title': input.title
            } for input in link.form.inputs.all()]
        }

        # Return the dictionary as a JSON object.
        return response.Response(json.dumps(result))


class InputList(generics.ListCreateAPIView):
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


class InputDetail(generics.RetrieveUpdateDestroyAPIView):
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
