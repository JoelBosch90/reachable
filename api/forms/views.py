# Import dependencies.
import secrets
from tools.Mail import FormConfirmation
from rest_framework import generics, permissions, response
from .models import User, Form, Link, Input
from .serializers import UserSerializer, FormSerializer, LinkSerializer, InputSerializer


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

    # If the serializer is valid, that means that a user with this email address
    # does not yet exist.
    if userSerializer.is_valid():

      # We should create the user if we don't have it yet.
      userSerializer.save()

    # Get access to the user object.
    user = User(email=request.data['email'])

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
        'name': 'Message',
        'form': form.id
      })

      # Check if the input is valid.
      if inputSerializer.is_valid():

        # If so, store it.
        inputSerializer.save()

      # We want to create a link with a unique key. We will keep trying until we
      # get one.
      while True:

        # Attempt to create a link.
        linkSerializer = LinkSerializer(data={
          'form': form.id,

          # We want to use the key in a URL, so it should be URL safe. It needs
          # to be long enough to be hard to guess and short enough to be
          # practical in a URL.
          'key': secrets.token_urlsafe(secrets.choice(range(16, 128)))
        })

        # If the link is valid that means the key is unique and we can escape
        # the loop.
        if linkSerializer.is_valid():

          # Store the link.
          link = linkSerializer.save()

          # Send a confirmation email.
          FormConfirmation().send(user, form)

          # Store the link and send it back to the client.
          return response.Response(link.key)

    # If it is not a valid form request, let the client know.
    else:
      return response.Response(formSerializer.errors)


class FormDetail(generics.RetrieveUpdateDestroyAPIView):
  """
  This is the endpoint that allows for retrieving, updating, and destroying
  individual forms.
  """

  # We're using the Form objects.
  queryset = Form.objects.all()

  # We're using the Form serializer.
  serializer_class = FormSerializer

  # Everyone can view forms, but only the user that owns them can modify them.
  permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class LinkList(generics.ListCreateAPIView):
  """
  This is the endpoint that allows for listing and creating links.
  """

  # We're using the Link objects.
  queryset = Link.objects.all()

  # We're using the Link serializer.
  serializer_class = LinkSerializer

  # Everyone can view links, but only the user that owns them can modify them.
  permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class LinkDetail(generics.RetrieveUpdateDestroyAPIView):
  """
  This is the endpoint that allows for retrieving, updating, and destroying
  individual links.
  """

  # We're using the Link objects.
  queryset = Link.objects.all()

  # We're using the Link serializer.
  serializer_class = LinkSerializer

  # Everyone can view links, but only the user that owns them can modify them.
  permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class InputList(generics.ListCreateAPIView):
  """
  This is the endpoint that allows for listing and creating inputs.
  """

  # We're using the Input objects.
  queryset = Input.objects.all()

  # We're using the Input serializer.
  serializer_class = InputSerializer

  # Everyone can view inputs, but only the user that owns them can modify them.
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

  # Everyone can view inputs, but only the user that owns them can modify them.
  permission_classes = [permissions.IsAuthenticatedOrReadOnly]