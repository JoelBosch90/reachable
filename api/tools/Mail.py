# Import dependencies.
import os
from html import escape
from django.core.mail import send_mail
from forms.serializers import (
    FormConfirmationLinkSerializer, FormDisableLinkSerializer
)
from tools.Template import (
    TransactionalTemplate
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
            'formLink': link.pk,
        })

        # Check if this link is valid.
        confirmationLinkSerializer.is_valid(raise_exception=True)

        # Save the serializer to get the confirmation link.
        confirmationURL = confirmationLinkSerializer.save().url()

        # Create a new disable link for this form.
        disableLinkSerializer = FormDisableLinkSerializer(data={
            'formLink': link.pk,
        })

        # Check if this link is valid.
        disableLinkSerializer.is_valid(raise_exception=True)

        # Save the serializer to get the disabled link.
        disableURL = disableLinkSerializer.save().url()

        # Make sure we escape the form's name.
        escapedName = escape(link.form.name)

        # Create a template for a transactional email.
        template = TransactionalTemplate()

        # Load all content into the template.
        template.replaceAll({
            'preheader': "Click the button to view your brand new form!",
            'title_text': "Express form delivery",
            'title_link': confirmationURL,
            'content': "Click the button to view your brand new form!" \
                       "<br/><br/>" \
                       "To make sure that you don't receive any" \
                       " unwanted responses, your form will only be" \
                       " activated once you click the button below. If you" \
                       " do no want to use this form you can simply ignore" \
                       " this email.",
            'button_text': "CONFIRM",
            'button_link': confirmationURL,
            'disable_link': disableURL,
            'home_link': os.getenv('CLIENT_URL')
        })

        # Construct the text version.
        text = "Visit the link to view your brand new form!\n\n" \
               "To make sure that you don't receive any" \
               " unwanted responses, your form will only be activated" \
               " once you visit the link below. If you do no want to use" \
               " this form you can simply ignore this email." \
               f"\n{confirmationURL}" \
               "\n\nEnjoy your form!\n\n" \
               "P.S. No longer want to receive responses from this form? You" \
               " can disable this form by visiting the following link:\n" \
               f"{disableURL}"

        send_mail(

            # Construct a confirmation message.
            subject=f"Express delivery of your new '{escapedName}' form.",

            # Add the text version.
            message=text,

            # Add the HTML version.
            html_message=template.html,

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

    def send(self, link, responses):
        """
        Method to send the response email.
        """

        # Create a new disable link for this form.
        disableLinkSerializer = FormDisableLinkSerializer(data={
            'formLink': link.pk,
        })

        # Check if this link is valid.
        disableLinkSerializer.is_valid(raise_exception=True)

        # Save the serializer to get the disabled link.
        disableURL = disableLinkSerializer.save().url()

        # Make sure we escape the form's name.
        escapedName = escape(link.form.name)

        # Get the label with each response. Make sure we escape these messages.
        labeled = [(link.form.inputs.filter(name=name).first().label, response)
                   for name, response in responses.items()]

        # Create the content message for the HTML email.
        escapedMessage = "<br/><br/>".join(f"<i>{escape(label)}</i>" \
                         f"<br/>{escape(text)}" for label, text in labeled)

        # Create a template for a transactional email.
        template = TransactionalTemplate()

        # Load all content into the template.
        template.replaceAll({
            'preheader': "You just received a new response for your" \
                         f" '{escapedName}' form!",
            'title_text': "Hey there, form builder!",
            'title_link': os.getenv('CLIENT_URL'),
            'content': "You just received a new response for your" \
                       f" '{escapedName}' form:<br/><br/>{escapedMessage}",
            'button_text': "TRY CUSTOM FORM",
            'button_link': f"{os.getenv('CLIENT_URL')}form/custom",
            'disable_link': disableURL,
            'home_link': os.getenv('CLIENT_URL')
        })

        # Add an introduction to the message.
        text = "Hey there, form builder!\n\nYou just received a new" \
               f" response for your '{escapedName}' form:\n\n"

        # Now list out the name and submission text for every input.
        text += "\n\n".join(f"{escape(label)}\n{escape(text)}"
            for label, text in labeled)

        # Add a closing greeting to the mail.
        text += "\n\nGreetings,\nYour friends @ Reachable"

        # We don't want to spam users, so we always add an option for the
        # receive to disable the form.
        text += "\n\nP.S. No longer want to receive responses from this" \
                " form? You can disable this form by clicking the" \
                f" following link:\n{disableURL}"

        send_mail(

            # Add a subject.
            subject=f"New response for the '{escapedName}' form.",

            # Add our message.
            message=text,

            # Add the HTML version.
            html_message=template.html,

            # Send a single email to the user.
            recipient_list=[link.form.user.email],

            # We can use the default FROM address.
            from_email=None,

            # We do want to know when sending fails.
            fail_silently=False,
        )
