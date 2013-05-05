#!/usr/bin/env python
#
# Copyright (c) 2012, Luke Southam <luke@devthe.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# - Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
#
# - Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in
#   the documentation and/or other materials provided with the
#   distribution.
#
# - Neither the name of the DEVTHE.COM LIMITED nor the names of its
#   contributors may be used to endorse or promote products derived
#   from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
# CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
# TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
# THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

import os

from xmlrpclib import ServerProxy
from urllib2 import urlopen

from getpass import getpass
import keyring

__doc__ = """
Dynamic DNS for WEBFACTION!
Update WebFaction domains to point to the IP of the local machine.

USAGE: python ddns.py [config_file]

    config_file        Default is 'ddns.config'.

    -h, --help         Print this message.

    --delete-password  Deletes the password from the keyring.

config_file:
    #          comments

    line 0     The first line that is not as comment must be the
                username for WebFaction.

    line 1+    The following lines must contain the domains to be update.

"""

__author__ = "Luke Southam <luke@devthe.com>"
__copyright__ = "Copyright 2013, DEVTHE.COM LIMITED"
__license__ = "The BSD 3-Clause License"
__status__ = "Development"

NAMESPACE = os.path.abspath(__file__)
API = 'https://api.webfaction.com/'
IP_FROM_URL = 'http://ip.catnapgames.com'

def readline(f):
    line = f.readline()
    return readline(f) if not line.strip() or line.startswith("#") else line.strip()

def read(f):
    return filter(lambda s: s and not s.startswith("#"), f.read().split('\n'))

def main(config):
    with file(config) as f:
        user = readline(f)
        password = get_password(user)
        domains = read(f)
    ip = get_ip()
    for domain in domains:
        print '%s --> %s' % (domain, ip)
        set_ip(domain, ip, user, password)


def get_password(user):
    password = keyring.get_password(NAMESPACE, user)
    if not password:
        p = getpass("Please enter %s's password: " % user)
        keyring.set_password(NAMESPACE, user, p)

        password = keyring.get_password(NAMESPACE, user)
        if not password:
            print "ERROR: COULD NOT GET PASSWORD!"
            exit(1)
    return password


def get_ip():
    return urlopen(IP_FROM_URL).read()


def set_ip(domain, ip, user, password):
    try:
        server = ServerProxy(API)
        session_id = server.login(user, password)[0]
        server.create_dns_override(session_id, domain, ip)
    except Exception as e:
        print "ERROR: clearing password."
        keyring.set_password(NAMESPACE, user, '')
        raise e

if __name__ == '__main__':
    from sys import argv
    if len(argv) < 2:
        import os
        main(os.path.join(os.path.dirname(NAMESPACE), 'ddns.config'))
    else:
        if any(arg in set(['-h', '--help']) for arg in argv):
            print __doc__
        elif '--delete-password' in argv:
            import sys 
            sys.stdout.write("Deleting the password ... ")
            sys.stdout.flush()
            with file(argv[2] if len(argv) > 2 else os.path.join(os.path.dirname(NAMESPACE), 'ddns.config')) as f:
                keyring.set_password(NAMESPACE, readline(f), '')
            sys.stdout.write("DONE!\n")
        else:
            main(argv[1])
