import emailHandler.emailHandler as eHandler
from googleapiclient import errors

class emailBot:
    def __init__(self):
        self.userAccount = None
        self.tokenName = None
        self.criteria = {}
        self.instances = 0
        self.list_message_requests = 0
        self.quota_units = 0

        self.account_prompt()
        self.criteria_prompt()
        self.reply_prompt()

        self.g_handler = eHandler.gmailHandler(self.userAccount)
        print(self.g_handler)
        self.service = self.g_handler.get_service()


    def account_prompt(self):
        self.userAccount = input("Enter your gmail user account: ")

    def from_prompt(self):
        criteria = input("From: ")
        self.criteria['from'] = "from:{}".format(criteria)

        print("From Criteria: {}".format(self.criteria['from']))

    def subject_prompt(self):
        criteria = input("Subject containing: ")
        self.criteria['subject'] = "subject:{}".format(criteria)
    
        print("Subject Criteria: {}".format(self.criteria['subject']))

    def message_body_prompt(self):
        criteria = input("Message body containing: ")
        self.criteria['message_body'] = "{}".format(criteria)
    
        print("Containing '{}' in the message body".format(self.criteria['subject']))

    def criteria_prompt(self):
        print("Criteria Search Options:\n" \
                "1: Sender\n" \
                "2: Subject\n" \
                "3: Message Body\n" \
                "4: Sender and Subject\n" \
                "5: Sender and Message Body\n" \
                "6: Subject and Message Body\n" \
                "7: Sender, Subject, and Message Body\n")
        selection = input("Selection:")
        print("Selection: {}".format(selection))

        if selection == '1':
            self.from_prompt()
        elif selection == '2':
            self.subject_prompt()
        elif selection == '3':
            self.message_body_prompt()
        elif selection == '4':
            self.from_prompt()
            self.subject_prompt()
        elif selection == '5':
            self.from_prompt()
            self.message_body_prompt()
        elif selection == '6':
            self.subject_prompt()
            self.message_body_prompt()
        elif selection == '7':
            self.from_prompt()
            self.subject_prompt()
            self.message_body_prompt()

    def reply_prompt(self):
        self.replySubject = input("Reply Subject: ")
        self.reply = input("Reply: ")

        print("Reply will be: {}:{}".format(self.replySubject, self.reply))

    def package_criteria(criteria):
        result = ""
        for term in criteria:
            result += str(term)

        print(result)
        return result

    def monitor(self):
        while(True):
            try:
                result = self.g_handler.list_messages(criteria=self.package_criteria(self.criteria))['resultSizeEstimate']
                self.list_message_requests += 1
                self.quota_units += 5
            except errors.HttpError as error:
                print("An HTTP error occurred: {}".format(error))
                break

            if(result != 0):
                print("Email found! Responding")
                reply = self.g_handler.create_message(
                    self.userAccount,
                    self.criteria['from'],

                )
                self.g_handler.send_message(
                    self.service,
                    self.userAccount,
                    self.reply
                )
                self.quota_units += 100
            else:
                print("Waiting for message")
                print("Requests: {}\nQuota units: {}".format(self.list_message_requests, self.quota_units))

        


if __name__ == '__main__':
    bot = emailBot()

# Prompt for user gmail account

# Prompt for type of criteria search
        #  # 1: Sender
        #  # 2: Subject
        #  # 3: Message Body
        #  # 4: Sender and Subject
        #  # 5: Sender and Message Body
        #  # 6: Subject and Message Body
        #  # 7: Sender, Subject, and Message Body

# Prompt for required criteria

# Prompt for return message