""" A script to unit test the emailData.py file """

from emailData import emailCreds, emailHandler

if __name__ == '__main__':
    creds = emailCreds()
    print("Using {}:{}".format(creds.get_USER(), creds.get_PASS()))
    handle = emailHandler(creds)