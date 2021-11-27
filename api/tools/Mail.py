# Import dependenices.
from django.core.mail import send_mail


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

        send_mail(

            # Construct a confirmation message.
            # @todo: add links to both the form and the confirmation page.
            subject="Confirm your '" + form.name + "' form.",
            message="Congratulations on creating your new form!\n\nClick" \
                    " here to start accepting new submissions for the '" +
                    form.name + " form'. \n\nEnjoy your form!",

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
                  " submission for your '" + form.name + "' form:\n\n"

        # Now list out the name and submission text for every input.
        message += "\n\n".join(name + "\n" + text
                               for name, text in inputs.items())

        send_mail(

            # Add a subject.
            subject="Form submission for the '" + form.name + "' form.",

            # Add our message.
            message=message,

            # Send a single email to the user.
            recipient_list=[user.email],

            # We can use the default FROM address.
            from_email=None,

            # We do want to know when sending fails.
            fail_silently=False,
        )
