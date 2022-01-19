from rest_framework import serializers
from .models import (
  Entity, TimeStamped, User, Form, Link, FormLink, FormConfirmationLink,
  FormDisableLink, Input
)

class EntitySerializer(serializers.ModelSerializer):
    """
    Serializer to build a base Entity model.
    """

    class Meta:
        """
        Specification of how a base Entity model is serialized.
        """

        model = Entity
        fields = [
            "id"
        ]


class TimeStampedSerializer(EntitySerializer):
    """
    Serializer to build a TimeStamped model.
    """

    class Meta(EntitySerializer.Meta):
        """
        Specification of how a TimeStamped model is serialized.
        """

        model = TimeStamped
        fields = EntitySerializer.Meta.fields + [
            "created",
            "updated"
        ]


class UserSerializer(TimeStampedSerializer):
    """
    Serializer to build a User model.
    """

    # List the forms that are connected to this user.
    forms = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name',
    )

    class Meta(TimeStampedSerializer.Meta):
        """
        Specification of how a User model is serialized.
        """

        model = User
        fields = TimeStampedSerializer.Meta.fields + [
            "email",
            "forms",
            "verified",
        ]


class FormSerializer(TimeStampedSerializer):
    """
    Serializer to build a Form model.
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

    class Meta(TimeStampedSerializer.Meta):
        """
        Specification of how a Form model is serialized.
        """

        model = Form
        fields = TimeStampedSerializer.Meta.fields + [
            "user",
            "name",
            "description",
            "inputs",
            "links",
            "confirmed",
            "disabled"
        ]
        extra_kwargs = {
            "description": { "required": False },
        }


class LinkSerializer(TimeStampedSerializer):
    """
    Serializer to build a Link model.
    """

    class Meta(TimeStampedSerializer.Meta):
        """
        Specification of how a Link model is serialized.
        """

        model = Link
        fields = TimeStampedSerializer.Meta.fields + [
            "key"
        ]


class FormLinkSerializer(LinkSerializer):
    """
    Serializer to build a FormLink model.
    """

    class Meta(LinkSerializer.Meta):
        """
        Specification of how a FormLink model is serialized.
        """

        model = FormLink
        fields = LinkSerializer.Meta.fields + [
            "form",
        ]


class FormConfirmationLinkSerializer(LinkSerializer):
    """
    Serializer to build a FormConfirmationLink model.
    """

    class Meta(LinkSerializer.Meta):
        """
        Specification of how a FormConfirmationLink model is serialized.
        """

        model = FormConfirmationLink
        fields = LinkSerializer.Meta.fields + [
            "formLink",
        ]


class FormDisableLinkSerializer(LinkSerializer):
    """
    Serializer to build a FormDisableLink model.
    """

    class Meta(LinkSerializer.Meta):
        """
        Specification of how a FormDisableLink model is serialized.
        """

        model = FormDisableLink
        fields = LinkSerializer.Meta.fields + [
            "formLink",
        ]


class InputSerializer(TimeStampedSerializer):
    """
    Serializer to build a Input model.
    """

    class Meta(TimeStampedSerializer.Meta):
        """
        Specification of how a Input model is serialized.
        """

        model = Input
        fields = TimeStampedSerializer.Meta.fields + [
            "form",
            "name",
            "label",
            "hint",
            "required",
            "type",
        ]
        extra_kwargs = {
            "label": { "required": False },
            "hint": { "required": False },
            "required": { "required": False },
            "type": { "required": False },
        }
