import smtplib

from email.mime.text import MIMEText

from pygor.settings import LOGFILE, EMAIL_TEMPLATES, PYGOR_EMAIL

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

        if machine.get_error():
            return "error"

        if machine._ran:
            return "success"

        return None

    def get_email(self, logfile=LOGFILE, msg_template=EMAIL_TEMPLATES, from_mail=PYGOR_EMAIL):
        """Return an email object of the email to be sent. Dont actually send
        anything.

        """

        context = dict(logfile=logfile)
        context.update(self.machine.get_error())

        if self.mail_type() is None:
            return None

        mt = self.mail_type()
        msg = MIMEText(msg_template[mt]['body'] % context)

        msg['Subject'] = msg_template[mt]['subject'] % context
        msg['From'] = from_mail
        msg['To'] = ','.join(self.spamtargets)
        return msg

    def send_email(self, msg_template=EMAIL_TEMPLATES, from_mail=PYGOR_EMAIL):
        s = smtplib.SMTP('localhost')
        msg = self.get_email(logfile, msg_template, from_mail)
        sender = 'localhost'
        recipients = msg['To'].split(',')
        s.sendmail(sender, recipients, msg.as_string())
