""" Email Crednential Handler

    This is used when OAuth2 is not used

"""

import os
import dotenv

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