import emailHandler.emailHandler as eHandler
import emailHandler.message as m
from googleapiclient import errors
import time

class emailBot:
    def __init__(self):
        self.userAccount = None
        self.tokenName = None                   # Will be used to track a particular token
        self.criteria = {}                      # Email search criteria
        self.list_message_requests = 0          # For metrics tracking
        self.quota_units = 0                    # For quota (API call limit) tracking
        self.time_since_sent_requirement = 10   # 10 second default # A value to react to messages in the past.
                                                # This value is in seconds and is subtracted from the current time
                                                # to determine whether an email should be responded to or not.
                                                # This is important because we don't want to respond to messages that
                                                # are too old, such as greater than 10 seconds old.
        self.g_handler = None                   # Gmail API Handler
        self.g_service = None                   # Gmail API Service

    @property
    def userAccount(self):
        return self._userAccount

    @property
    def tokenName(self):
        return self._tokenName

    @property
    def criteria(self):
        return self._criteria

    @property
    def list_message_requests(self):
        self.userAccount = "testemail@gmail.com"
        self.criteria['from'] = "from:testemail@gmail.com is:unread"
        self.criteria['subject'] = "Test subject"
        self.reply = "Hey tester, \n" + \
                     "Just replying to your message. Have a great day. \n" +  \
                     " -B"
        return self._list_message_requests

    @property
    def quota_units(self):
        return self._quota_units

    @property
    def time_since_sent_requirement(self):
        return self._time_since_sent_requirement

    @property
    def g_handler(self):
        return self._g_handler

    @property
    def g_service(self):
        return self._g_service

    @userAccount.setter
    def userAccount(self, value):
        self._userAccount = value

    @tokenName.setter
    def tokenName(self, value):
        self._tokenName = value

    def set_tokenName(self):
        self.tokenName = str(self.userAccount[0:5]) + ".pickle"

    @list_message_requests.setter
    def list_message_requests(self, value):
        self._list_message_requests = value

    @quota_units.setter
    def quota_units(self, value):
        self._quota_units = value

    @criteria.setter
    def criteria(self, value):
        self._criteria = value

    @time_since_sent_requirement.setter
    def time_since_sent_requirement(self, value):
        self._time_since_sent_requirement = value

    @g_handler.setter
    def g_handler(self, value):
        self._g_handler = value

    @g_service.setter
    def g_service(self, value):
        self._g_service = value

    def package_criteria(self, criteria):
        result = "is:unread -RE:" # ignore unread and RE: emails
        for term in criteria:
            result += " " + str(criteria[term])
        return result

    def ACTION(self):
        packaged_criteria = self.package_criteria(self.criteria)
        processed = [] # Should be kept in a file

        while(True):
            try:
                result = self.g_handler.list_messages(criteria=packaged_criteria)
                # print("\n\nresult: {}".format(result))

                self.list_message_requests += 1
                self.quota_units += 5

                resultSize = result.get('resultSizeEstimate')

                if(resultSize >= 1):
                    print("{} Email(s) found! Responding".format(resultSize))

                    # Assume one message for now
                    messages = result.get('messages')
                    print("Result: {}".format(result))

                    for msg in messages:
                        if msg['id'] in processed:
                            print("skipping {}".format(msg['id']))
                            break

                        # TODO (BAR): print if config.debug is set. Parse debug options as argv
                        # print("\n\nmsg: {}".format(msg))
                        # print("\n\nmessages: {}".format(messages))

                        message_id = msg['id']
                        # print("\n\nmessage_id: {}".format(message_id))

                        content = self.g_handler.get_message(message_id)
                        print("\n\ncontent: {}".format(content))

                        new_message = m.message()
                        new_message.consume_json(content)
                        print("\n\nnew_message: {}".format(new_message.contents))

                        # time_since_sent = int(time.time()) - int(new_message.contents['date'])
                        time_now = int(time.time())
                        time_sent = int(new_message.contents['date'])
                        time_since_sent = time_now - time_sent
                        print("\n\n\n\ntime_now:{}  time_sent:{} time_since_sent:{}".format(time_now, time_sent, time_since_sent))

                        if(time_since_sent < self.time_since_sent_requirement):
                            createdReply = new_message.create_reply(self.reply)
                            print("\n\ncreatedReply: {}".format(createdReply))

                            self.g_handler.send_message(
                                self.g_service,
                                self.userAccount,
                                createdReply
                            )
                            print("\n\nResponse sent!")
                            self.quota_units += 100
                            self.g_handler.mark_as_read(message_id)

                        processed.append(content['id'])

                else:
                    print("Waiting for message")

                print("Requests: {}\nQuota units: {}".format(self.list_message_requests, self.quota_units))

            except errors.HttpError as error:
                print("An HTTP error occurred: {}".format(error))
                break

class emailBot_CommandLine(emailBot):
    def __init__(self):
        super().__init__()

        # self.account_prompt()
        self.criteria_prompt()
        # self.reply_prompt()
        self.time_since_sent_prompt()

        self.userAccount = "testemail@gmail.com"
        # self.criteria['from'] = "from:testemail@gmail.com is:unread"
        # self.criteria['subject'] = "Test subject"
        self.reply = "Hey, \n" + \
                     "Just replying to your message. Have a great day. \n" +  \
                     " -B"

        self.g_handler = eHandler.gmailHandler(self.userAccount)

        self.g_service = self.g_handler.get_service()

    def account_prompt(self):
        self.userAccount = input("Enter your gmail user account: ")

    def from_prompt(self):
        criteria = input("From: ")
        self.criteria['from'] = "from:" + str(criteria)

        print("From Criteria: {}".format(self.criteria['from'][5:]))

    def subject_prompt(self):
        criteria = input("Subject containing: ")
        self.criteria['subject'] = "subject:" + str(criteria)

        print("Subject Criteria: {}".format(self.criteria['subject']))

    def message_body_prompt(self):
        criteria = input("Message body containing: ")
        self.criteria['message_body'] = str(criteria)

        print("Containing '{}' in the message body".format(self.criteria['message_body']))

    def time_since_sent_prompt(self):
        self.time_since_sent_requirement = int(input("Time since sent requirement: "))

        print("All emails later than {} will be ignored".format(int(time.time()) - self.time_since_sent_requirement))

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
        self.reply = input("Reply Message: ")

        print("Reply will be: {}".format(self.reply))

if __name__ == '__main__':
    bot = emailBot_CommandLine()
    bot.ACTION()

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
