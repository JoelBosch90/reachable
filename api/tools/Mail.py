# Import dependenices.
from django.core.mail import send_mail

class FormConfirmation:
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
      subject="Confirm your form.",
      message="Congratulations on creating your new form!\n\nClick here to start accepting new submissions for the form '" + form.name + "'.\n\nEnjoy your form!",

      # Send a single email to the user.
      recipient_list=[user.email],

      # We can use the default FROM address.
      from_email=None,

      # We do want to know when sending fails.
      fail_silently=False,
    )