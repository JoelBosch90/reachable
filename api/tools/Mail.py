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
      subject="Confirm your form.",
      message="Congratulations on creating your new form!\n\nClick here to start accepting new submissions for the form '" + form.name + "'.\n\nEnjoy your form!",
      from_email='reachable@joelbosch.nl',
      recipient_list=[user.email],
      fail_silently=False,
    )