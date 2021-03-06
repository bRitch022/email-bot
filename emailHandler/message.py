import base64
from email.mime.text import MIMEText

# TODO (BAR): import VERSION
VERSION = "v0.2"

class message(object):
    def __init__(self):
        
        self.encoded_data = None
        self.data = None
        self.parts = None

        self.contents = {
            'id' : "",
            'date' : "",
            'string_date' : '',
            'labelIds' : "",
            'sender' : "",
            'recipient' : "",
            'subject' : "",
            'body' : ""
        }


    def consume_json(self, json):
        self.contents['id'] = json['id']
        self.contents['labelIds'] = json['labelIds']
        self.contents['date'] = json['internalDate'][0:10] # epoch time only 10 digits. Cut off the remaining characters
        payload = json['payload']
        headers = payload['headers']

        for header in headers:
            try:
                if header['name'] == 'to':
                    self.contents['recipient'] = header['value']
                    # print("Consumed ['to']:{}".format(self.contents['recipient']))
                elif header['name'] == 'from':
                    self.contents['sender'] = header['value']
                    # print("Consumed ['from']:{}".format(self.contents['sender']))
                elif header['name'] == 'subject':
                    self.contents['subject'] = header['value']
                    # print("Consumed ['subject']:{}".format(self.contents['subject']))
                elif header['name'] == "date":
                    self.contents['string_date'] = header['value']
                    # print("Consumed ['date']:{}".format(self.contents['string_date']))
                else:
                    pass

            except KeyError as e:
                print(e)
                pass

            self.parts = payload.get('body')
            # print("Consumed ['body']:{}".format(self.parts))
            self.data = self.parts.get('data')
            # print("Consumed ['data']:{}".format(self.data))

            if(self.data != None):
                try:
                    decoded_data = base64.b64decode(self.data)
                except:
                    return

                try:
                    self.contents['body'] = decoded_data.decode()
                    # print("Consumed ['body']:{}".format(self.contents['body']))
                except UnicodeDecodeError as e:
                    print(e)
                

    def encode_msg(self):
        """Encode a message object into a url safe message"""
        message = MIMEText(self.contents['body'])
        message['to'] = self.contents['recipient']
        message['from'] = self.contents['sender']
        message['subject'] = self.contents['subject']
        string_message = message.as_string()
        b64 = base64.urlsafe_b64encode(string_message.encode('utf-8'))

        self.encoded_data = {
            'raw' : b64.decode('utf-8')
        }

    def decode_msg(self):
        decoded_data = base64.b64decode(self.encoded_data)
        self.contents['body'] = decoded_data.decode()

    def create_reply(self, reply_msg):
        # Save off the previous body to put into the reply
        orig_body = self.contents['body']

        self.contents['body'] = reply_msg
        self.contents['body'] += "\n\n\nPowered by Email-Bot {}".format(VERSION)
        self.contents['body'] += ("\n\n")
        self.contents['body'] += ("-------- Original message --------\n")
        self.contents['body'] += ("From: {}\n".format(self.contents['sender']))
        self.contents['body'] += ("Sent: {}\n".format(self.contents['string_date']))
        self.contents['body'] += ("To: {}\n".format(self.contents['recipient']))
        self.contents['body'] += ("Subject: {}\n".format(self.contents['subject']))
        self.contents['body'] += ("\n{}\n".format(orig_body))

        orig_to = self.contents['recipient']
        self.contents['recipient'] = self.contents['sender']
        self.contents['sender'] = orig_to

        orig_subject = self.contents['subject']
        self.contents['subject'] = "RE: " + str(orig_subject)

        self.encode_msg()

        return self.encoded_data

    




        







    

    

            