import secrets
import os
from djongo import models
from django.utils import timezone
from datetime import timedelta


class Entity(models.Model):
    """
    Abstract base model that adds an ID primary key that every class should
    have.
    """

    # Add an automatic primary key.
    id = models.ObjectIdField(db_column="_id", primary_key=True)

    class Meta:
        """
        Make this an abstract class.
        """
        abstract = True


class TimeStamped(Entity):
    """
    Abstract model to add time stamps to models.
    """

    # Make sure that we always know when a timestamped model was created.
    created = models.DateTimeField(auto_now_add=True)

    # Make sure that we always know when a timestamped model was last updated.
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Make this an abstract class.
        """
        abstract = True


# Create your models here.
class User(TimeStamped):
    """
    This model represents a single user.
    """

    # Users are identified by their email address.
    email = models.CharField(max_length=320, unique=True)

    # Flag to record when (if ever) ownership of the email address was
    # verified.
    verified = models.DateTimeField(null=True)

    def __str__(self):
        """
        Converts the user model to a string representation.
        """

        # We can use the email address. It should be unique.
        return self.email


class Form(TimeStamped):
    """
    This model represents a single form.
    """

    # A form is always tied to a user.
    user = models.ForeignKey(User, related_name='forms',
                             on_delete=models.CASCADE)

    # A form is identified by a name, which is unique per user.
    name = models.CharField(max_length=256, default='Form')

    # Every form can have an optional description they can use to make a note
    # about the form to themselves.
    description = models.CharField(max_length=1024, blank=True, null=True)

    # Flag to record when (if ever) this form was confirmed by the user.
    confirmed = models.DateTimeField(null=True)

    # Flag to record if this form is disabled by the owner.
    disabled = models.BooleanField(default=False)

    class Meta:
        """
        Extra settings for the Form class.
        """

        # Make sure that the form's name is unique per user.
        unique_together = ['user', 'name']

    def __str__(self):
        """
        Converts the form model to a string representation.
        """

        # We can combine the form's name and the user, as this should be a
        # unique combination.
        return self.name + ':' + str(self.user)


class Link(TimeStamped):
    """
    This base model represents a link. This base class holds a unique URL-safe
    key that can be used to link to something. Typically, you'll use an
    extending class to link to something useful.
    """

    def generate_key():
        """
        Function to generate a unique key for this link.
        """

        # While unlikely, it is possible that the first key we create is not
        # unique. In such a case, we want to keep trying.
        while True:

            # We want to use the key in a URL, so it should be URL
            # safe. It needs to be long enough to be hard to guess and
            # short enough to be practical in a URL.
            key = secrets.token_urlsafe(secrets.choice(range(16, 128)))

            # Make sure that there is no other link that uses this key.
            if (not Link.objects.filter(key=key).exists()):
                return key

    # A link is identified by this key. Every link should be unique, regardless
    # of the form it is attached to. It should have a reasonable length to fit
    # a URL.
    key = models.CharField(max_length=128, unique=True, default=generate_key)

    def default_expire_date():
        """
        Function to calculate the default expire date.
        """

        # By default, links should last about half a year.
        return timezone.now() + timedelta(180)

    # Always set an expire date on links. We shouldn't keep these forever.
    expires = models.DateTimeField(default=default_expire_date)

    def hasExpired(self):
        """
        Method to check if this link has already expired.
        """

        # If now is greater than or equal to the expiration date, this link is
        # still good.
        return self.expires < timezone.now()

    def __str__(self):
        """
        Converts a link to a string representation.
        """

        # The key should be unique, and is already a string.
        return self.key


class FormLink(Link):
    """
    This model represents a link to a form. This type of link is always tied to
    a single form, and is used to access that form. A single form could have
    multiple links to allow users to identify different types of traffic.
    """

    # A link is always tied to a single form.
    form = models.ForeignKey(Form, related_name='links',
                             on_delete=models.CASCADE)

    def url(self):
        """
        Method to generate a URL for this link.
        """

        # Link to the form.
        return f"{os.getenv('CLIENT_URL')}form/{self.key}"

    def shareUrl(self):
        """
        Method to generate a URL for this link.
        """

        # Link to the form's share page.
        return f"{os.getenv('CLIENT_URL')}form/share/{self.key}"

    def __str__(self):
        """
        Converts a form's link to a string representation.
        """

        # We can combine the link's key, which should be unique. For
        # convenience, we also add the form it links to.
        return super().__str__() + ':' + str(self.form)


class FormConfirmationLink(Link):
    """
    This link can be used to confirm a form. Because anyone can create a form
    for any email address, we should first make sure that the owner of the
    email address wants to receive the form's responses. We can do that by
    sending a unique form link to their email address. As soon as the receiver
    clicks this link, the form will be verified and activated.

    If this is a user's first form, the user will also be verified.
    """

    # A FormConfirmationLink is always linked to a specific form link that it
    # will redirect to if successful.
    formLink = models.ForeignKey(FormLink, on_delete=models.CASCADE)

    def url(self):
        """
        Method to generate a URL for the confirmation link.
        """

        # Create the link that will confirm the link to confirm the form.
        return f"{os.getenv('API_URL')}forms/confirm/{self.key}"

    def __str__(self):
        """
        Converts a confirmation link to a string representation.
        """

        # We can combine the link's key, which should be unique. For
        # convenience, we also add the form it links to.
        return super().__str__() + ':' + str(self.formLink.form)


class FormDisableLink(Link):
    """
    No matter the reason, we should always provide the owner of the inbox with
    the ability to disable a form and prevent further emails from it. We can do
    this by adding a special link to the confirmation email and each response
    with which the owner can disable the form.
    """

    # A FormDisableLink is always linked to a specific FormLink.
    formLink = models.ForeignKey(FormLink, on_delete=models.CASCADE)

    def url(self):
        """
        Method to generate a URL for the disable link.
        """

        # Create the link that will disable the form.
        return f"{os.getenv('API_URL')}forms/disable/{self.key}"

    def __str__(self):
        """
        Converts a confirmation link to a string representation.
        """

        # We can combine the link's key, which should be unique. For
        # convenience, we also add the form it disables.
        return super().__str__() + ':' + str(self.formLink.form)


class Input(TimeStamped):
    """
    This model represents a user.
    """

    # An input is always tied to a single form.
    form = models.ForeignKey(Form, related_name='inputs',
                             on_delete=models.CASCADE)

    # An input is identified by a name that is unique for each form.
    name = models.CharField(max_length=256)

    # Optionally, an input can be labeled.
    label = models.CharField(max_length=256, blank=True, null=True)

    # Optionally, we can define a tooltip attribute.
    hint = models.CharField(max_length=512, blank=True, null=True)

    # Optionally, we can make an input field required.
    required = models.BooleanField(default=False)

    # Optionally, we can set an input type.
    type = models.CharField(max_length=256, default='text')

    class Meta:
        """
        Extra settings for the Input class.
        """

        # Make sure that the input's name is unique per form.
        unique_together = ['form', 'name']

    def __str__(self):
        """
        Converts the input model to a string representation.
        """

        # We can combine the input's name and the form, as this should be a
        # unique combination.
        return self.name + ':' + str(self.form)
