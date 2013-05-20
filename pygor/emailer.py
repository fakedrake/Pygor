import os
import smtplib
from email.mime.text import MIMEText

from pygor.settings import LOGFILE, EMAIL_TEMPLATES, PYGOR_EMAIL
from pygor.logger import Logger

class Emailer(Logger):
    """Sends emails for good or for bad. This is more of a minion.

    """

    def __init__(self, spamtargets, machine):
        """Mark the recipients and the machine.

        """
        self.spamtargets = spamtargets
        self.machine = machine

    def mail_type(self):
        """ Querry what kind of email is to be sent. Possible return values are

        - None :: no mail is to be sent.
        - "error"
        - "success"

        """

        if self.machine.get_error():
            return "error"

        if self.machine._ran:
            return "success"

        return None

    def get_email(self, logfile=LOGFILE, msg_template=EMAIL_TEMPLATES, from_mail=PYGOR_EMAIL):
        """Return an email object of the email to be sent. Dont actually send
        anything.

        """

        context = dict(logfile=os.path.abspath(logfile))
        context.update(self.machine.get_error())

        if self.mail_type() is None:
            return None

        mt = self.mail_type()
        msg = MIMEText(msg_template[mt]['body'] % context)

        msg['Subject'] = msg_template[mt]['subject'] % context
        msg['From'] = from_mail
        msg['To'] = ','.join(self.spamtargets)
        return msg

    def send_email(self, smtp_config, msg_template=EMAIL_TEMPLATES, logfile=LOGFILE):
        """smtp_config is mandatory really. You will need 'server', 'port',
        'user' (this is the email), 'password' in there.

        """
        s = smtplib.SMTP()
        s.set_debuglevel(0)
        exit_code, exit_message = s.connect(smtp_config['server'], smtp_config['port'])
        if exit_code != 220:
            raise ValueError("Could not connect to the smtp server")

        s.login(smtp_config['user'], smtp_config['password'])

        msg = self.get_email(logfile, msg_template, smtp_config['user'])
        sender = smtp_config['user']
        recipients = msg['To'].split(',')
        s.sendmail(sender, recipients, msg.as_string())
