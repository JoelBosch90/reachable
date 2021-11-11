from rest_framework import generics, permissions
from .models import User, Form, Link, Input
from .serializers import UserSerializer, FormSerializer, LinkSerializer, InputSerializer


class FormList(generics.ListCreateAPIView):
  """
  This is the endpoint that allows for listing and creating forms.
  """

  # We're using the Form objects.
  queryset = Form.objects.all()

  # We're using the Form serializer.
  serializer_class = FormSerializer

  # Everyone can view forms, but only the user that owns them can modify them.
  permission_classes = [permissions.IsAuthenticatedOrReadOnly]


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