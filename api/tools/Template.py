# Import dependencies.
import re


class TransactionalTemplate:
    """
    Class to configure a transactional HTML email template.
    """

    # Set the HTML property as an empty string by default.
    html = ''

    # Try to load the transactional HTML template.
    with open('templates/transactional.html', 'r') as file:
        html = file.read()

    def replace(self, placeholder, replacement):
        """
        Method to replace a single placeholder inside the HTML template with
        content.
        """

        # All placeholders in the email template will look like {{PLACEHOLDER}}
        # and we can find and replace them using a regular expression.
        self.html = re.sub(rf'{{{{{placeholder}}}}}', replacement, self.html,
                           flags=re.IGNORECASE)

    def replaceAll(self, replacemenents):
        """
        Method to replace many placeholders inside the HTML template with
        content. This requires a dictionary that maps placeholders to their
        replacements.
        """

        # Simply call our replace method for each placeholder/replacement pair
        # in the dictionary.
        for placeholder, replacement in replacemenents.items():
            self.replace(placeholder, replacement)