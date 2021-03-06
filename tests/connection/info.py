# Copyright 2017 Cisco Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

host = "ucscentral"


def custom_setup():
    try:
        import ConfigParser
    except:
        import configparser as ConfigParser

    import os
    from ucscsdk.ucschandle import UcscHandle

    config = ConfigParser.RawConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), '..', 'connection',
                             'connection.cfg'))

    hostname = config.get(host, "hostname")
    username = config.get(host, "username")
    password = config.get(host, "password")
    try:
        port = config.get(host, "port")
    except:
        port = 443
    handle = UcscHandle(hostname, username, password, port=port)
    handle.login()
    return handle


def custom_teardown(handle):
    handle.logout()
