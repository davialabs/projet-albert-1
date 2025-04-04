class Mail:

    To : str
    From : str
    Content : str
    Header : str

    def __init__(self, To, From, Content, Header):
        self.To = To
        self.From = From
        self.Content = Content
        self.Header = Header

    def create_mail(To, From, Content, Header):
        """
        Function: create_email

Description: Creates an email draft without automatically sending it.

Parameters:
- from_address (string): The sender's email address (e.g., "your.name@example.com")
- to_address (string): The recipient's email address (e.g., "townhall@city.gov")
- subject (string): The email subject line that summarizes the purpose of the email
- body (string): The complete content of the email, including greeting, main message, questions, and signature

Returns:
- email_object: A structured email object that can be reviewed before sending

Note: This function only prepares the email. No email will be sent automatically. You must explicitly call a separate send function if you wish to transmit the email.

Example usage:
create_email(
    from_address="john.smith@gmail.com",
    to_address="mairie@paris.fr",
    subject="Request for Information About Business Permits",
    body="Dear Sir/Madam,\n\nI am writing to inquire about the procedure for obtaining a business permit in your municipality...\n\nThank you for your assistance.\n\nSincerely,\nJohn Smith\nPhone: 06 12 34 56 78"
)
        """
        email = Mail(To, From, Content, Header)
        return email