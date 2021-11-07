from rest_framework import serializers
from .models import User, Form, Link, Input

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = [
      "email",
    ]

class FormSerializer(serializers.ModelSerializer):
  class Meta:
    model = Form
    fields = [
      "user",
      "name",
      "description",
    ]
    extra_kwargs = {
      "description": {"required": False}
    }

class LinkSerializer(serializers.ModelSerializer):
  class Meta:
    model = Link
    fields = [
      "form",
      "key",
    ]

class InputSerializer(serializers.ModelSerializer):
  class Meta:
    model = Input
    fields = [
      "form",
      "name",
      "title",
    ]
    extra_kwargs = {
      "title": {"required": False}
    }