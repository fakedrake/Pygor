import os
import unittest
import smtplib

from pygor.emailer import Emailer
from pygor.bigmachine import BigMachine
from pygor.procedure import Procedure

SPAMTARGETS = ['darksaga2006@gmail.com']

PYGOR_EMAIL = "hubot@example.com"

SMTP_CONFIG = dict(server="mail.example.com",
                   port=25,
                   user=PYGOR_EMAIL,
                   password="password")

smtp=None
inbox=[]

class Message(object):
    def __init__(self,from_address,to_address,fullmessage):
        self.from_address=from_address
        self.to_address=to_address
        self.fullmessage=fullmessage

class MockSMTP(object):
    def __init__(self):
        global smtp
        smtp=self

    def set_debuglevel(self, dbglvl):
        """ Doesnt really matter
        """
        pass

    def connect(self, server, port):
        self.server = server
        self.port = port

        if server == SMTP_CONFIG['server'] and port == SMTP_CONFIG['port']:
            return (220, "Good job!")

    def login(self,username,password):
        self.username=username
        self.password=password

    def sendmail(self,from_address,to_address,fullmessage):
        global inbox
        inbox.append(Message(from_address,to_address,fullmessage))
        return []

    def quit(self):
        self.has_quit=True

# Monkey patch
smtplib.SMTP=MockSMTP

class TestEmailer(unittest.TestCase):

    def setUp(self):
        self.machine = BigMachine()
        spamtargets = SPAMTARGETS

        self.emailer = Emailer(spamtargets, self.machine)

    def produce_exit(self, code):
        """ Make machine produce an error.
        """
        self.machine.reset(procedures=True)
        self.machine.add_test(Procedure("exit %d" % code))
        self.machine.run()


    def test_type(self):

        self.assertEquals(self.emailer.mail_type(), None)

        # Empty run
        self.produce_exit(0)
        self.assertEquals(self.emailer.mail_type(), "success")

        # Set to fail
        self.produce_exit(10)
        self.assertEquals(self.emailer.mail_type(), "error")

    def test_error(self):
        self.produce_exit(10)
        self.assertIn("exit 10", self.emailer.get_email().as_string())

    def test_sending(self):
        self.produce_exit(10)
        self.emailer.send_email(SMTP_CONFIG)

        self.assertEquals(len(inbox), 1)
        self.assertEquals(inbox[0].fullmessage, self.emailer.get_email(from_mail=PYGOR_EMAIL).as_string())
