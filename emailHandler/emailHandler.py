
import poplib
import base64
import logging
import mimetypes
import os
import os.path
import pickle
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient import errors
from googleapiclient.discovery import build
        
class emailHandler_API:
    """ A class to handle emails to a from a particular API """
    def __init__(self):

        # # Class enforcement. This MUST be overwritten by child classes
        self.service = None
        self.creds = None
        self.user=None

    def get_service(self):
        raise NotImplementedError # Class enforcement

    def send_message(self, service, sender, message):
        raise NotImplementedError # Class enforcement

    def create_message(self, sender, to, subject, message_text):
        raise NotImplementedError # Class enforcement

class gmailHandler(emailHandler_API):
    """ Gmail OAth2 Handler 
    Author: Steve Gore
    Date: August 5, 2019
    URL: https://stackoverflow.com/questions/25944883/how-to-send-an-email-through-gmail-without-enabling-insecure-access

    Modified by: Bryan Ritchie
    Date: June 2021
    """

    def __init__(self, user):
        super().__init__()
        self.user = user

    def get_service(self):
        """Gets an authorized Gmail API service instance.

        Returns:
            An authorized Gmail API service instance..
        """    

        # If modifying these scopes, delete the file token.pickle.
        SCOPES = [
            'https://www.googleapis.com/auth/gmail.readonly',
            'https://www.googleapis.com/auth/gmail.send',
        ]

        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

        self.service = build('gmail', 'v1', credentials=self.creds)
        return self.service

    def send_message(self, service, sender, message):
        """Send an email message.

        Args:
            service: Authorized Gmail API service instance.
            user_id: User's email address. The special value "me"
            can be used to indicate the authenticated user.
            message: Message to be sent.

        Returns:
            Sent Message.
        """
        try:
            sent_message = (service.users().messages().send(userId=sender, body=message)
                    .execute())
            logging.info('Message Id: %s', sent_message['id'])
            return sent_message
        except errors.HttpError as error:
            logging.error('An HTTP error occurred: %s', error)

    def create_message(self, sender, to, subject, message_text):
        """Create a message for an email.

        Args:
            sender: Email address of the sender.
            to: Email address of the receiver.
            subject: The subject of the email message.
            message_text: The text of the email message.

        Returns:
            An object containing a base64url encoded email object.
        """
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        s = message.as_string()
        b = base64.urlsafe_b64encode(s.encode('utf-8'))
        return {'raw': b.decode('utf-8')}

    def list_messages(self, includeSpamTrash=None, maxResults=None, criteria=None):
        """List messages in an email account.

        Args:
            includeSpamTrash: boolean, Include messages from `SPAM` and `TRASH` in the results.
            maxResults: integer, Maximum number of messages to return.
            criteria: string, Only return messages matching the specified query. Supports the same query format as the Gmail search box. 
                      For example, `"from:someuser@example.com rfc822msgid: is:unread"`. 
                      Parameter cannot be used when accessing the api using the gmail.metadata scope.

        Returns:
            An object of the format detailed in https://googleapis.github.io/google-api-python-client/docs/dyn/gmail_v1.users.messages.html#list
        """

        if self.service is None:
            self.service = self.get_service()
            
        try:
            messages = (self.service.users().messages().list(\
                    userId=self.user,\
                    includeSpamTrash=includeSpamTrash,\
                    labelIds=None,\
                    pageToken=None,\
                    q=criteria).execute())
        except errors.HttpError as error:
            logging.error('An HTTP error occurred: %s', error)

        return messages

    def get_message(self, message_id, format="full", metadataHeaders=None):
        """Get a specified message in an email account.
        
        Args:
            message_id: string, The ID of the message to retrieve
            format: string, The format to return the message in
                Allowed values
                minimal - Returns only email message ID and labels; does not return the email headers, body, or payload.
                full - Returns the full email message data with body content parsed in the `payload` field; the `raw` field is not used. Format cannot be used when accessing the api using the gmail.metadata scope.
                raw - Returns the full email message data with body content in the `raw` field as a base64url encoded string; the `payload` field is not used. Format cannot be used when accessing the api using the gmail.metadata scope.
                metadata - Returns only email message ID, labels, and email headers
            metadataHeaders: string, When given and format is `METADATA`, only include headers specified.

        Returns:
            An object of the form detailed in https://googleapis.github.io/google-api-python-client/docs/dyn/gmail_v1.users.messages.html#get
            """

        if self.service is None:
            self.service = self.get_service()

        try:
            message = (self.service.users().messages().get(\
                userId=self.user,\
                id=message_id,\
                format=format,\
                metadataHeaders=metadataHeaders).execute())
        except errors.HttpError as error:
            logging.error('An HTTP error occurred: %s', error)

        return message


class POP3Handler(emailHandler_API):
    """ A class to handle emails to and from a POP3 server
        Currently, only gmail is being supported
    """

    def __init__(self, emailCreds, server='gmail'):
        # if server is 'gmail':
        try:
            self.session = poplib.POP3_SSL('pop.gmail.com')
        except poplib.error_proto as e:
            print({}.format(e))
            return
        # else if ...

        self.session.user(emailCreds.get_USER())
        self.session.pass_(emailCreds.get_PASS())

    def get_mail(self):
        return len(self.session.list()[1])

def testGmailHandler_send():
    sender = "bryan.ritchie2@gmail.com"
    to = "bryan.ritchie2@gmail.com"
    subject = "Test subject"
    message_text = "Test body"

    print("Default Sender: {}\nDefault Recipient: {}\nDefault Subject: {}\nDefault Message: {}\n".format(sender, to, subject, message_text))

    g_handler = gmailHandler(sender)

    logging.basicConfig(
        format="[%(levelname)s] %(message)s",
        level=logging.INFO
    )

    try:
        service = g_handler.get_service()
        message = g_handler.create_message(sender, to, subject, message_text)
        g_handler.send_message(service, sender, message)

    except Exception as e:
        logging.error(e)
        raise

def testGmailHandler_read():
    """ Reading emails from Gmail using Gmail API in Python
    Author: devansh07
    Date: October 1, 2020
    URL: https://www.geeksforgeeks.org/how-to-read-emails-from-gmail-using-gmail-api-in-python/

    Modified by: Bryan Ritchie
    Date: June 2021
    """

    user = "bryan.ritchie2@gmail.com"
    criteria = "from:bryan.ritchie2@gmail.com is:unread subject:Test Subject"

    g_handler = gmailHandler(user)

    logging.basicConfig(
        format="[%(levelname)s] %(message)s",
        level=logging.INFO
    )

    try:
        service = g_handler.get_service()
        result = g_handler.list_messages(criteria=criteria)

    except Exception as e:
        logging.error(e)
        raise

    print("Found messages: {}".format(result["resultSizeEstimate"]))
    messages=result.get('messages')

    for msg in messages:
        sender=None
        subject=None

        # Capture message id
        msg_id = msg['id']
        print("Getting {}".format(msg_id))

        # Get the content
        content = g_handler.get_message(msg_id)

        try:
            # Parse the content
            internalDate = content['internalDate']
            payload = content['payload']
            headers = payload['headers']

            # Parse headers
            for header in headers:
                match header['name']:
                    case "to":
                        receiver = header['value']
                    case "from":
                        sender = header['value']
                    case "subject":
                        subject = header['value']
                    case "Date":
                        date = header['value']
                    case _:
                        pass

            parts = payload.get('body')
            data = parts.get('data')
            decoded_data = base64.b64decode(data)
            body = decoded_data.decode()
        
            print("From: {}".format(sender))
            print("To: {}".format(receiver))
            print("Subject: {}".format(subject))
            print("Date: {}".format(date))
            print("Epoch: {}".format(internalDate))
            print("\nBody: {}\n\n".format(body))

        except KeyError as e:
            print(e)
            pass



    
    