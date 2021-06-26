

import os
import dotenv
import poplib

class emailCreds:
    """ A class to support environment variable username and password """

    def __init__(self):
        self.set_creds()

    def set_creds(self, filename='.env'):
        try:
            dotenv_file = dotenv.find_dotenv(filename, raise_error_if_not_found=True)
        except OSError as e:
            print("{}: {}".format(e, filename))
            return

        dotenv.load_dotenv(dotenv_file)
        self._USERNAME = os.environ['USERNAME']
        self._PASS = os.environ['PASS']

    def get_USER(self):
        return self._USERNAME

    def get_PASS(self):
        return self._PASS
        
class emailHandler:
    """ A class to handle emails to and from a particular server
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


