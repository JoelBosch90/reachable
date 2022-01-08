from rest_framework import serializers
from .models import (
  TimeStamped, User, Form, FormConfirmationLink, Link, FormLink, Input
)


class UserSerializer(serializers.ModelSerializer):
    """
    This serializer knows how to construct a User object.
    """

    # List the forms that are connected to this user.
    forms = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name',
    )

    class Meta:
        """
        Specification of how the User model is serialized.
        """

        model = User
        fields = [
            "email",
            "forms",
            "verified",
        ]


class FormSerializer(serializers.ModelSerializer):
    """
    This serializer knows how to construct a Form object.
    """

    # List the inputs and links that are connected to this user.
    inputs = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name',
    )
    links = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='key',
    )

    class Meta:
        """
        Specification of how the Form model is serialized.
        """

        model = Form
        fields = [
            "id",
            "user",
            "name",
            "description",
            "inputs",
            "links",
            "confirmed",
        ]
        extra_kwargs = {
            "description": {"required": False},
        }


class FormLinkSerializer(serializers.ModelSerializer):
    """
    This serializer knows how to construct a FormLink object.
    """

    class Meta:
        """
        Specification of how the FormLink model is serialized.
        """

        model = FormLink
        fields = [
            "form",
            "key",
        ]


class FormConfirmationLinkSerializer(serializers.ModelSerializer):
    """
    This serializer knows how to construct a FormConfirmationLink object.
    """

    class Meta:
        """
        Specification of how the FormConfirmationLink model is serialized.
        """

        model = FormConfirmationLink
        fields = [
            "formLink",
            "key",
        ]


class InputSerializer(serializers.ModelSerializer):
    """
    This serializer knows how to construct an Input object.
    """

    class Meta:
        """
        Specification of how the Input model is serialized.
        """

        model = Input
        fields = [
            "form",
            "name",
            "title",
        ]
        extra_kwargs = {
            "title": {"required": False},
        }
