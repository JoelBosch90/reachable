# Import dependenices.
from django.core.mail import send_mail
from forms.serializers import (
  FormConfirmationLinkSerializer, FormDisableLinkSerializer
)


class FormConfirmationMail:
    """
    Helper class to send a single email to confirm that the owner of the email
    address wants to start accepting submissions for a new form.

    We want to send an email to confirm this to make sure that we don't start
    sending unwanted emails.
    """

    def send(self, user, link):
        """
        Method to send the confirmation email.
        """

        # Create a new confirmation link for this form.
        confirmationLinkSerializer = FormConfirmationLinkSerializer(data={
            'formLink': link.key,
        })

        # Check if this link is valid.
        confirmationLinkSerializer.is_valid(raise_exception=True)

        # Save the serializer to get the confirmation link.
        confirmationURL= confirmationLinkSerializer.save().url()

        # Create a new disable link for this form.
        disableLinkSerializer = FormDisableLinkSerializer(data={
            'formLink': link.key,
        })

        # Check if this link is valid.
        disableLinkSerializer.is_valid(raise_exception=True)

        # Save the serializer to get the disabled link.
        disableURL = disableLinkSerializer.save().url()

        # Construct the message.
        message = "Congratulations on creating your new form!\n\nClick" \
                  " here to start accepting new submissions for the" \
                  f" '{link.form.name}' form.\n\nVisit the following link to" \
                  " confirm your email address and activate this form:\n" \
                  f"{confirmationURL}\n\nEnjoy your form!"

        # Add a closing greeting to the mail.
        message += "\n\nGreetings,\nYour friends @ Reachable"

        # We don't want to spam users, so we always add an option for the
        # receive to disable the form.
        message += "\n\nP.S. No longer want to receive responses from this" \
                   " form? You can disable this form by clicking the" \
                   f" following link:\n{disableURL}"

        send_mail(

            # Construct a confirmation message.
            subject=f"Confirm your '{link.form.name}' form.",
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

    def send(self, link, inputs):
        """
        Method to send the response email.
        """

        # Create a new disable link for this form.
        disableLinkSerializer = FormDisableLinkSerializer(data={
            'formLink': link.key,
        })

        # Check if this link is valid.
        disableLinkSerializer.is_valid(raise_exception=True)

        # Save the serializer to get the disabled link.
        disableURL = disableLinkSerializer.save().url()

        # Add an introduction to the message.
        message = "Hey there, form builder!\n\nYou just received a new" \
                  f" submission for your '{link.form.name}' form:\n\n"

        # Now list out the name and submission text for every input.
        message += "\n\n".join(f"{name}\n{text}"
                               for name, text in inputs.items())

        # Add a closing greeting to the mail.
        message += "\n\nGreetings,\nYour friends @ Reachable"

        # We don't want to spam users, so we always add an option for the
        # receive to disable the form.
        message += "\n\nP.S. No longer want to receive responses from this" \
                   " form? You can disable this form by clicking the" \
                   f" following link:\n{disableURL}"

        send_mail(

            # Add a subject.
            subject=f"Form submission for the '{link.form.name}' form.",

            # Add our message.
            message=message,

            # Send a single email to the user.
            recipient_list=[link.form.user.email],

            # We can use the default FROM address.
            from_email=None,

            # We do want to know when sending fails.
            fail_silently=False,
        )
