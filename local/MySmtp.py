#! /usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib
import ssl
from email.mime.text import MIMEText


class EmailBackend():
    """
    A wrapper that manages the SMTP network connection.
    """
    def __init__(self, host=None, port=None, username=None, password=None,
                 use_tls=False):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.use_tls = use_tls
        self.connection = None

    def open(self):
        """
        Ensures we have a connection to the email server. Returns whether or
        not a new connection was required (True or False).
        """
        if self.connection:
            # Nothing to do if the connection is already open.
            return False
        try:
            # If local_hostname is not specified, socket.getfqdn() gets used.
            # For performance, we use the cached FQDN for local_hostname.
            self.connection = smtplib.SMTP(self.host, self.port)
            if self.use_tls:
                self.connection.ehlo()
                self.connection.starttls()
                self.connection.ehlo()
            if self.username and self.password:
                self.connection.login(self.username, self.password)
            return True
        except:
            return False

    def close(self):
        """Closes the connection to the email server."""
        if self.connection is None:
            return
        try:
            try:
                self.connection.quit()
            except (ssl.SSLError, smtplib.SMTPServerDisconnected):
                # This happens when calling quit() on a TLS connection
                # sometimes, or when the connection was already disconnected
                # by the server.
                self.connection.close()
            except:
                return
        finally:
            self.connection = None

    def send_messages(self, to_addrs, subject, msg_content):
        """
        Sends one or more EmailMessage objects and returns the number of email
        messages sent.
        """
        send_ok = False
        new_conn_created = self.open()
        if not self.connection:
            return send_ok
        msg = MIMEText(msg_content)
        msg['Subject'] = subject
        msg['From'] = self.username
        msg['To'] = to_addrs
        try:
            self.connection.sendmail(self.username,[to_addrs],msg.as_string())
        except:
            send_ok = False
        else:
            send_ok = True
        finally:
            if new_conn_created:
                self.close()
        return send_ok