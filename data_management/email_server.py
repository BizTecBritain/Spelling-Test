__all__ = ['EmailServer']
__version__ = '5.1.6'
__author__ = 'Alexander Bisland'

import base64
import json
import smtplib
import urllib.parse
import urllib.request
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import lxml.html
from typing import Tuple
from threading import Thread

from data_management.config import Config


class EmailServer:
    GOOGLE_ACCOUNTS_BASE_URL = 'https://accounts.google.com'
    REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    CERT_PROVIDER = "https://www.googleapis.com/oauth2/v1/certs"
    AUTH_URI = "https://accounts.google.com/o/oauth2/auth"
    TOKEN_URI = "https://oauth2.googleapis.com/token"
    MAIL_SCOPE = "https://mail.google.com/"

    def __init__(self, config_file: str = "../local_storage/server.ini") -> None:
        """
        Description: Constructor sets up attributes including objects
        :param config_file: the config file to read
        :return: void
        """
        self.parser = Config()
        self.parser.load(config_file)

        self.GOOGLE_CLIENT_ID = self.parser.read_tag("EMAILCONFIG", "id")
        self.GOOGLE_CLIENT_SECRET = self.parser.read_tag("EMAILCONFIG", "secret")
        self.GOOGLE_PROJECT_ID = self.parser.read_tag("EMAILCONFIG", "project_id")
        self.token_exists = False
        try:
            self.GOOGLE_REFRESH_TOKEN = self.parser.read_tag("TOKENCONFIG", "refresh_token")
            self.token_exists = True  # if the token already exists this line will be reached
        except KeyError:
            pass
        if not self.token_exists:
            print('No refresh token found, obtaining one')
            self.GOOGLE_REFRESH_TOKEN, access_token, expires_in = self.__get_authorization()
            if not self.token_exists:
                self.parser.append_section("TOKENCONFIG", {"refresh_token": self.GOOGLE_REFRESH_TOKEN})

    def __get_authorization(self) -> Tuple[str, str, str]:
        """
        Description: Function to authorise the user
        :return: tuple[str, str, str] - refresh_token, access_token, expires_in
        """
        url = '{0}/o/oauth2/auth?'.format(EmailServer.GOOGLE_ACCOUNTS_BASE_URL)
        params = {'client_id': self.GOOGLE_CLIENT_ID,
                  'redirect_uri': EmailServer.REDIRECT_URI,
                  'scope': EmailServer.MAIL_SCOPE,
                  'response_type': 'code'}
        param_fragments = []
        for param in sorted(params.items(), key=lambda x: x[0]):
            param_fragments.append('{0}={1}'.format(param[0], urllib.parse.quote(param[1], safe='~-._')))
        url += '&'.join(param_fragments)  # generates url to navigate to to authenticate user
        print('Navigate to the following URL:', url)
        auth_code = input('Enter verification code: ')
        params = {'client_id': self.GOOGLE_CLIENT_ID,
                  'client_secret': self.GOOGLE_CLIENT_SECRET,
                  'code': auth_code,
                  'redirect_uri': EmailServer.REDIRECT_URI,
                  'grant_type': 'authorization_code'}
        request_url = '{0}/o/oauth2/token'.format(EmailServer.GOOGLE_ACCOUNTS_BASE_URL)
        response = urllib.request.urlopen(request_url, urllib.parse.urlencode(params).encode('UTF-8')).read().decode(
            'UTF-8')  # gets the neccessary information from the auth_code
        response = json.loads(response)
        return response['refresh_token'], response['access_token'], response['expires_in']

    def send_mail(self, fromaddr: str, toaddr: str, subject: str, message: str) -> None:
        """
        Description: Function to start a thread to send an email
        :param fromaddr: the email address to send from
        :param toaddr: the email address to send to
        :param subject: the subject of the message
        :param message: the message
        :return: void
        """
        send_thread = Thread(target=self.__send_mail, args=(fromaddr, toaddr, subject, message))
        send_thread.start()

    def __send_mail(self, fromaddr: str, toaddr: str, subject: str, message: str):
        """
        Description: Function to send an email
        :param fromaddr: the email address to send from
        :param toaddr: the email address to send to
        :param subject: the subject of the message
        :param message: the message
        :return: void
        """
        params = {'client_id': self.GOOGLE_CLIENT_ID,
                  'client_secret': self.GOOGLE_CLIENT_SECRET,
                  'refresh_token': self.GOOGLE_REFRESH_TOKEN,
                  'grant_type': 'refresh_token'}
        request_url = '{0}/o/oauth2/token'.format(EmailServer.GOOGLE_ACCOUNTS_BASE_URL)
        response = urllib.request.urlopen(request_url, urllib.parse.urlencode(params)
                                          .encode('UTF-8')).read().decode('UTF-8')
        response = json.loads(response)
        access_token = response['access_token']
        auth_string = 'user={0}\1auth=Bearer {1}\1\1'.format(fromaddr, access_token)
        auth_string = base64.b64encode(auth_string.encode('ascii')).decode('ascii')
        msg = MIMEMultipart('related')
        msg['Subject'] = subject
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg.preamble = 'This is a multi-part message in MIME format.'
        msg_alternative = MIMEMultipart('alternative')
        msg.attach(msg_alternative)
        part_text = MIMEText(lxml.html.fromstring(message).text_content().encode('utf-8'), 'plain', _charset='utf-8')
        part_html = MIMEText(message, 'html', _charset='utf-8')
        msg_alternative.attach(part_text)
        msg_alternative.attach(part_html)
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo(self.GOOGLE_CLIENT_ID)
        server.starttls()
        server.docmd('AUTH', 'XOAUTH2 ' + auth_string)
        server.sendmail(fromaddr, toaddr, msg.as_string())
        server.quit()


if __name__ == '__main__':
    email_server = EmailServer()
    email_server.send_mail('biztecbritain@gmail.com', 'biztecbritain@gmail.com',
                           'Hello',
                           '<b>A mail from Biz</b><br><br>' +
                           'Shuuuuuuuush')
