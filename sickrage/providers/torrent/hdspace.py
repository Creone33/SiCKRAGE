# Author: Idan Gutman
# Modified by jkaberg, https://github.com/jkaberg for SceneAccess
# Modified by 7ca for HDSpace
# URL: https://sickrage.ca
#
# This file is part of SickRage.
#
# SickRage is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SickRage is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SickRage.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

import re
import urllib

from requests.utils import dict_from_cookiejar

import sickrage
from sickrage.core.caches.tv_cache import TVCache
from sickrage.core.helpers import bs4_parser, convert_size
from sickrage.providers import TorrentProvider


class HDSpaceProvider(TorrentProvider):
    def __init__(self):
        super(HDSpaceProvider, self).__init__("HDSpace", 'https://hd-space.org', True)

        self.urls.update({
            'login': '{base_url}/index.php?page=login'.format(**self.urls),
            'search': '{base_url}/index.php?page=torrents&search=%s&active=1&options=0&category='.format(**self.urls),
            'rss': '{base_url}/rss_torrents.php?feed=dl'.format(**self.urls)
        })

        self.username = None
        self.password = None

        self.minseed = None
        self.minleech = None

        self.categories = [15, 21, 22, 24, 25, 40]  # HDTV/DOC 1080/720, bluray, remux
        for cat in self.categories:
            self.urls['search'] += str(cat) + '%%3B'
            self.urls['rss'] += '&cat[]=' + str(cat)

        self.urls['search'] = self.urls['search'][:-4]  # remove extra %%3B

        self.cache = TVCache(self, min_time=10)

    def _check_auth(self):
        if not self.username or not self.password:
            sickrage.app.log.warning(
                "Invalid username or password. Check your settings".format(self.name))

        return True

    def login(self):
        if any(dict_from_cookiejar(self.session.cookies).values()):
            return True

        if 'pass' in dict_from_cookiejar(self.session.cookies):
            return True

        login_params = {'uid': self.username,
                        'pwd': self.password}

        try:
            response = self.session.post(self.urls['login'], data=login_params, timeout=30).text
        except Exception:
            sickrage.app.log.warning("Unable to connect to provider".format(self.name))
            return False

        if re.search('Password Incorrect', response):
            sickrage.app.log.warning(
                "Invalid username or password. Check your settings".format(self.name))
            return False

        return True

    def search(self, search_strings, age=0, ep_obj=None):
        results = []

        if not self.login():
            return results

        for mode in search_strings.keys():
            sickrage.app.log.debug("Search Mode: %s" % mode)
            for search_string in search_strings[mode]:

                if mode != 'RSS':
                    sickrage.app.log.debug("Search string: %s" % search_string)
                    searchURL = self.urls['search'] % (urllib.quote_plus(search_string.replace('.', ' ')),)
                else:
                    searchURL = self.urls['search'] % ''

                try:
                    data = self.session.get(searchURL).text
                    results += self.parse(data, mode)
                except Exception:
                    sickrage.app.log.debug("No data returned from provider")
                    continue

        return results

    def parse(self, data, mode):
        """
        Parse search results from data
        :param data: response data
        :param mode: search mode
        :return: search results
        """

        results = []

        try:
            data = data.split('<div id="information"></div>')[1]
        except ValueError:
            sickrage.app.log.error("Could not find main torrent table")
            return results

        with bs4_parser(data[data.index('<table'):]) as html:
            torrents = html.findAll('tr')
            if not torrents:
                return results

            # Skip column headers
            for result in torrents[1:]:
                if len(result.contents) < 10:
                    # skip extraneous rows at the end
                    continue

                try:
                    dl_href = result.find('a', attrs={'href': re.compile(r'download.php.*')})['href']
                    title = re.search('f=(.*).torrent', dl_href).group(1).replace('+', '.')
                    download_url = self.urls['base_url'] + dl_href
                    seeders = int(result.find('span', attrs={'class': 'seedy'}).find('a').text)
                    leechers = int(result.find('span', attrs={'class': 'leechy'}).find('a').text)
                    size = convert_size(result, -1)

                    if not all([title, download_url]):
                        continue

                    results += [
                        {'title': title, 'link': download_url, 'size': size, 'seeders': seeders, 'leechers': leechers}
                    ]

                    if mode != 'RSS':
                        sickrage.app.log.debug("Found result: {}".format(title))
                except Exception:
                    sickrage.app.log.error("Failed parsing provider")

        return results
