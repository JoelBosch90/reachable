import secrets
import os
from djongo import models
from django.utils import timezone
from datetime import timedelta


class TimeStamped(models.Model):
    """
    Abstract base class to add time stamps to models.
    """

    class Meta:
        """
        Extra settings for the TimeStamped class.
        """

        # Indicate that this is an abstract class that is to be used for
        # inheritance only. It should never exist on its own.
        abstract = True

    # Make sure we always have a timestamp for when this object was created.
    created = models.DateTimeField(auto_now_add=True)

    # Add a timestamp for when the object was last modified.
    updated = models.DateTimeField(auto_now=True)


# Create your models here.
class User(TimeStamped):
    """
    This model represents a single user.
    """

    def __str__(self):
        """
        Converts the user model to a string representation.
        """

        # We can use the email address. It should be unique.
        return self.email

    # Users are identified by their email address.
    email = models.CharField(max_length=320, unique=True, primary_key=True)

    # Flag to record when (if ever) ownership of the email address was
    # verified.
    verified = models.DateTimeField(null=True)


class Form(TimeStamped):
    """
    This model represents a single form.
    """

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


class Link(TimeStamped):
    """
    This base model represents a link. This base class holds a unique URL-safe
    key that can be used to link to something. Typically, you'll use an
    extending class to link to something useful.
    """

    def generate_key():
        """
        Method to generate a unique key for this link.
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

    def __str__(self):
        """
        Converts a link to a string representation.
        """

        # The key should be unique, and is already a string.
        return self.key

    # A link is identified by this key. Every link should be unique, regardless
    # of the form it is attached to. It should have a reasonable length to fit
    # a URL.
    key = models.CharField(max_length=128, unique=True, default=generate_key)


class FormLink(Link):
    """
    This model represents a link to a form. This type of link is always tied to
    a single form, and is used to access that form. A single form can have
    multiple links to allow users to identify different types of traffic.

    Optionally, this link can be used to confirm the form and the user. Because
    anyone can create a form for any email address, we should first make sure
    that the owner of the email address wants to receive the form's responses.
    We can do that by sending a unique form link with the confirmation flag set
    to True to their email address. As soon as the receiver clicks this link,
    both the form and the user will be verified and activated.
    """

    def url(self):
        """
        Method to generate a URL using this link's key to link to the form it is
        associated with.
        """

        # Construct a URL with the key for this link.
        return f"{os.getenv('CLIENT_URL')}form/{self.key}"

    def default_expire_date():
      """
      Method to calculate the default expiration date.
      """

      # By default, links should last about half a year.
      return timezone.now() + timedelta(180)

    def __str__(self):
        """
        Converts a form's link to a string representation.
        """

        # We can combine the link's key, which should be unique. For
        # convenience, we also add the form it links to.
        return super().__str__() + ':' + str(self.form)

    # Always set an expire date on form links. We shouldn't keep these forever.
    expires = models.DateTimeField(default=default_expire_date)

    # A link is always tied to a single form.
    form = models.ForeignKey(Form, related_name='links',
                             on_delete=models.CASCADE)

    # Should this link be used to confirm the associated form and user?
    confirmation = models.BooleanField(default=False)


class LoginLink(Link):
    """
    This is link that users can click to authenticate. This is a link that gets
    sent to an email address. The user can click this link to authenticate and
    get access to user specific parts of the application.
    """

    def default_expire_date():
      """
      Overriding the default expiration date to calculate a much shorter
      expiration date for the login link.
      """

      # By default, login links should expire in half an hour.
      return timezone.now() + timedelta(1//48)

    def url(self):
        """
        Method to generate a URL for the page that a user can visit to
        authenticate.
        """

        # Construct a URL with the key for this link.
        return f"{os.getenv('CLIENT_URL')}authenticated/{self.key}"

    def __str__(self):
        """
        Converts a login link to a string representation.
        """

        # We can combine the link's key, which should be unique. For
        # convenience, we also add the user it links to.
        return super().__str__() + ':' + str(self.user)

    # Set an altered expiration date for the login link as these should not
    # keep too long.
    expires = models.DateTimeField(default=default_expire_date)

    # A login link is always tied to a user.
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Input(TimeStamped):
    """
    This model represents a user.
    """

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

    # An input is always tied to a single form.
    form = models.ForeignKey(Form, related_name='inputs',
                             on_delete=models.CASCADE)

    # An input is identified by a name that is unique for each form.
    name = models.CharField(max_length=256)

    # Optionally, we can define a tooltip attribute.
    title = models.CharField(max_length=512, blank=True, null=True)
