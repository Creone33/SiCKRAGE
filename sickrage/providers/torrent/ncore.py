# coding=utf-8
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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SickRage. If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function, unicode_literals

import re

from requests.utils import dict_from_cookiejar

import sickrage
from sickrage.core.caches.tv_cache import TVCache
from sickrage.core.helpers import convert_size
from sickrage.providers import TorrentProvider


class NcoreProvider(TorrentProvider):
    def __init__(self):
        super(NcoreProvider, self).__init__('nCore', 'https://ncore.cc', True)

        self.username = None
        self.password = None
        self.minseed = None
        self.minleech = None

        categories = [
            'xvidser_hun', 'xvidser',
            'dvd_hun', 'dvd',
            'dvd9_hun', 'dvd9',
            'hd_hun', 'hd'
        ]

        categories = '&'.join(['kivalasztott_tipus[]=' + x for x in categories])

        self.urls.update({
            'login': '{base_url}/login.php'.format(**self.urls),
            'search': ('{base_url}/torrents.php?{cats}&mire=%s&miben=name'
                       '&tipus=kivalasztottak_kozott&submit.x=0&submit.y=0&submit=Ok'
                       '&tags=&searchedfrompotato=true&jsons=true').format(cats=categories, **self.urls),
        })

        self.cache = TVCache(self)

    def login(self):
        if any(dict_from_cookiejar(self.session.cookies).values()):
            return True

        login_params = {
            'nev': self.username,
            'pass': self.password,
            'submitted': '1',
        }

        try:
            response = self.session.post(self.urls["login"], data=login_params).text
        except Exception:
            sickrage.app.log.warning("Unable to connect to provider")
            return False

        if re.search('images/warning.png', response):
            sickrage.app.log.warning("Invalid username or password. Check your settings")
            return False

        return True

    def search(self, search_strings, age=0, ep_obj=None):
        results = []

        if not self.login():
            return results

        for mode in search_strings:

            sickrage.app.log.debug("Search Mode: {0}".format(mode))

            for search_string in search_strings[mode]:
                if mode != "RSS":
                    sickrage.app.log.debug("Search string: {0}".format(search_string))

                try:
                    data = self.session.get(self.urls['search'] % search_string).json()
                    results += self.parse(data, mode)
                except Exception:
                    sickrage.app.log.debug("No data returned from provider")

        return results

    def parse(self, data, mode):
        """
        Parse search results from data
        :param data: response data
        :param mode: search mode
        :return: search results
        """

        results = []

        if not isinstance(data, dict):
            return results

        torrent_results = data['total_results']
        if not torrent_results:
            return results

        sickrage.app.log.debug('Number of torrents found on nCore = ' + str(torrent_results))

        for item in data['results']:
            try:
                title = item.pop("release_name")
                download_url = item.pop("download_url")
                if not all([title, download_url]):
                    continue

                seeders = item.pop("seeders")
                leechers = item.pop("leechers")
                torrent_size = item.pop("size", -1)
                size = convert_size(torrent_size, -1)

                if mode != "RSS":
                    sickrage.app.log.debug("Found result: {}".format(title))

                results += [
                    {'title': title, 'link': download_url, 'size': size, 'seeders': seeders, 'leechers': leechers}
                ]

                if mode != 'RSS':
                    sickrage.app.log.debug("Found result: {}".format(title))
            except Exception:
                sickrage.app.log.error("Failed parsing provider")

        return results