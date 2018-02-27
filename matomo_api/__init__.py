#!/usr/bin/env python3

# Copyright (c) 2018, Stadt Karlsruhe (www.karlsruhe.de)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

'''
Low-level Python wrapper for the Matomo (formerly Piwik) API.
'''

import html

import requests


__version__ = '0.1.0'


class MatomoException(Exception):
    pass


class _Element:
    def __init__(self, matomo, name):
        self._name = name
        self._matomo = matomo

    def __getattr__(self, s):
        name = '{}.{}'.format(self._name, s)
        return _Element(self._matomo, name)

    def __call__(self, **kwargs):
        kwargs['module'] = 'API'
        kwargs['method'] = self._name
        return self._matomo._request(**kwargs)

    def __repr__(self):
        return '<Matomo API "{}">'.format(self.name)


class Matomo:
    '''
    Matomo API wrapper.
    '''
    def __init__(self, url, **kwargs):
        self.url = url
        self.default_params = kwargs

    def __getattr__(self, s):
        return _Element(self, s)

    def _request(self, **kwargs):
        params = dict(self.default_params)
        params.update(kwargs)
        params['format'] = 'json'
        r = requests.get(self.url, params=params)
        r.raise_for_status()
        data = r.json()
        try:
            status = data['result']
        except (TypeError, KeyError):
            # No status information, everything is fine
            pass
        else:
            if status == 'error':
                raise MatomoException(html.unescape(data['message']))
        return data

