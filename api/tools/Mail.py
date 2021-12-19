# Import dependenices.
from django.core.mail import send_mail
from forms.models import (
  User, Form, FormLink
)
from forms.serializers import (
  FormLinkSerializer
)


class MailException(Exception):
    """
    Exception class for mail related errors.
    """
    pass


class FormConfirmationMail:
    """
    Helper class to send a single email to confirm that the owner of the email
    address wants to start accepting submissions for a new form.

    We want to send an email to confirm this to make sure that we don't start
    sending unwanted emails.
    """

    def send(self, user, form):
        """
        Method to send the confirmation email.
        """

        # Create a new confirmation link for this form.
        formLinkSerializer = FormLinkSerializer(data={
            'form': form.id,
            'confirmation': True,
        })

        # Check if this link is valid.
        if not formLinkSerializer.is_valid():
            raise MailException('Could not generate confirmation link.')

        # Save the serializer to get the confirmation link.
        confirmationLink = formLinkSerializer.save().url()

        message = "Congratulations on creating your new form!\n\nClick" \
                  " here to start accepting new submissions for the" \
                  f"'{form.name} form'.\n\nVisit the following link to" \
                  " confirm your email address and activate this form:\n" \
                  f"{confirmationLink}\n\nEnjoy your form!" \
                  "\n\nGreetings,\nYour friends @ Reachable"

        send_mail(

            # Construct a confirmation message.
            subject=f"Confirm your '{form.name}' form.",
            message=message,

            # Send a single email to the user.
            recipient_list=[user.email],

            # We can use the default FROM address.
            from_email=None,

            # We do want to know when sending fails.
            fail_silently=False,
        )


class FormResponseMail:
    """
    Helper class to send a single response email with a form submission to the
    owner of the form.
    """

    def send(self, user, form, inputs):
        """
        Method to send the response email.
        """

        # Add an introduction to the message.
        message = "Hey there, form builder!\n\nYou just received a new" \
                  f" submission for your '{form.name}' form:\n\n"

        # Now list out the name and submission text for every input.
        message += "\n\n".join(f"{name}\n{text}"
                               for name, text in inputs.items())

        # Add a closing greeting to the mail.
        message += "\n\nGreetings,\nYour friends @ Reachable"

        send_mail(

            # Add a subject.
            subject=f"Form submission for the '{form.name}' form.",

            # Add our message.
            message=message,

            # Send a single email to the user.
            recipient_list=[user.email],

            # We can use the default FROM address.
            from_email=None,

            # We do want to know when sending fails.
            fail_silently=False,
        )
