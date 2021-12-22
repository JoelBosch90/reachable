from rest_framework import serializers
from .models import User, Form, Link, LoginLink, FormLink, Input


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


class LinkSerializer(serializers.ModelSerializer):
    """
    This serializer knows how to construct a Link object.
    """

    class Meta:
        """
        Specification of how the Link model is serialized.
        """

        model = Link
        fields = [
            "id",
            "key",
        ]


class FormLinkSerializer(LinkSerializer):
    """
    This serializer knows how to construct a FormLink object.
    """

    class Meta:
        """
        Specification of how the FormLink model is serialized.
        """

        model = FormLink
        fields = [
            "id",
            "key",
            "form",
            "confirmation",
        ]


class LoginLinkSerializer(LinkSerializer):
    """
    This serializer knows how to construct a LoginLink object.
    """

    class Meta:
        """
        Specification of how the LoginLink model is serialized.
        """

        model = LoginLink
        fields = [
            "id",
            "key",
            "user",
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
            "id",
            "form",
            "name",
            "title",
        ]
        extra_kwargs = {
            "title": {"required": False},
        }
