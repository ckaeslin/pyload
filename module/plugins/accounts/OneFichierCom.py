# -*- coding: utf-8 -*-

import re
import time

import pycurl

from module.plugins.internal.Account import Account


class OneFichierCom(Account):
    __name__    = "OneFichierCom"
    __type__    = "account"
    __version__ = "0.20"
    __status__  = "testing"

    __description__ = """1fichier.com account plugin"""
    __license__     = "GPLv3"
    __authors__     = [("Elrick69", "elrick69[AT]rocketmail[DOT]com"),
                       ("Walter Purcaro", "vuolter@gmail.com")]


    VALID_UNTIL_PATTERN = r'Your subscription will end the (\d+\-\d+\-\d+)'


    def grab_info(self, user, password, data):
        validuntil = None
        trafficleft = -1
        premium = None

        html = self.load("https://1fichier.com/console/abo.pl")

        m = re.search(self.VALID_UNTIL_PATTERN, html)
        if m is not None:
            expiredate = m.group(1)
            self.log_debug("Expire date: " + expiredate)

            try:
                validuntil = time.mktime(time.strptime(expiredate, "%Y-%m-%d"))

            except Exception, e:
                self.log_error(e, trace=True)

            else:
                premium = True

        return {'validuntil': validuntil, 'trafficleft': trafficleft, 'premium': premium or False}


    def signin(self, user, password, data):
        self.req.http.c.setopt(pycurl.REFERER, "https://1fichier.com/login.pl?lg=en")

        html = self.load("https://1fichier.com/login.pl?lg=en",
                         post={'mail'   : user,
                               'pass'   : password,
                               'It'     : "on",
                               'purge'  : "off",
                               'valider': "Send"})

        if '>Invalid email address' in html or '>Invalid password' in html:
            self.fail_login()
