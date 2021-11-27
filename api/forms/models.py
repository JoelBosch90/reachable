from django.db import models


# Create your models here.
class User(models.Model):
    """
    This model represents a single user.
    """

    # Users are identified by their email address.
    email = models.CharField(max_length=320, unique=True, primary_key=True)

    def __str__(self):
        """
        Converts the user model to a string representation.
        """

        # We can use the email address. It should be unique.
        return self.email


class Form(models.Model):
    """
    This model represents a single form.
    """

    # Add an automatic primary key.
    id = models.AutoField(primary_key=True)

    # A form is always tied to a user.
    user = models.ForeignKey(User, related_name='forms',
                             on_delete=models.CASCADE)

    # A form is identified by a name, which is unique per user.
    name = models.CharField(max_length=256, default='Form')

    # Every form can have an optional description they can use to make a note
    # about the form to themselves.
    description = models.CharField(max_length=1024, blank=True, null=True)

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


class Link(models.Model):
    """
    This model represents a link. A link is always tied to a single form, and
    is used to access that form. A single form can have multiple links to allow
    users to identify.
    """

    # A link is always tied to a single form.
    form = models.ForeignKey(Form, related_name='links',
                             on_delete=models.CASCADE)

    # A link is identified by this key. Every link should be unique, regardless
    # of the form it is attached to. It should have a reasonable length to fit
    # a URL.
    key = models.CharField(max_length=128, primary_key=True)

    def __str__(self):
        """
        Converts the link model to a string representation.
        """

        # We can combine the link's key, which should be unique. For
        # convenience, we also add the form it links to.
        return self.key + ':' + str(self.form)


class Input(models.Model):
    """
    This model represents a user.
    """

    # An input is always tied to a single form.
    form = models.ForeignKey(Form, related_name='inputs',
                             on_delete=models.CASCADE)

    # An input is identified by a name that is unique for each form.
    name = models.CharField(max_length=256)

    # Optionally, we can define a tooltip attribute.
    title = models.CharField(max_length=512, blank=True, null=True)

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
