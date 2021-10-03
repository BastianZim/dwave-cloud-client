# Copyright 2021 D-Wave Systems Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import uuid
import unittest

import requests
import requests_mock

from dwave.cloud.api import exceptions
from dwave.cloud.api.client import SAPIClient
from dwave.cloud.package_info import __packagename__, __version__


class TestConfig(unittest.TestCase):
    """Session is initiated from config."""

    def test_defaults(self):
        client = SAPIClient()

        self.assertEqual(client.config, SAPIClient.DEFAULTS)
        self.assertIsInstance(client.session, requests.Session)

        # verify Retry object config
        retry = client.session.get_adapter('https://').max_retries
        conf = SAPIClient.DEFAULTS['retry']
        self.assertEqual(retry.total, conf['total'])

    def test_init(self):
        config = dict(endpoint='https://test.com/path/',
                      token=str(uuid.uuid4()),
                      timeout=1,
                      retry=dict(total=3),
                      headers={'Custom': 'Field 123'},
                      verify=False,
                      proxies={'https': 'http://proxy.com'})

        client = SAPIClient(**config)

        session = client.session
        self.assertIsInstance(session, requests.Session)

        self.assertEqual(session.base_url, config['endpoint'])
        self.assertEqual(session.cert, None)
        self.assertEqual(session.headers['X-Auth-Token'], config['token'])
        self.assertEqual(session.headers['Custom'], config['headers']['Custom'])
        self.assertIn(__packagename__, session.headers['User-Agent'])
        self.assertIn(__version__, session.headers['User-Agent'])
        self.assertEqual(session.verify, config['verify'])
        self.assertEqual(session.proxies, config['proxies'])

        # verify Retry object config
        retry = session.get_adapter('https://').max_retries
        self.assertEqual(retry.total, config['retry']['total'])


class TestResponseParsing(unittest.TestCase):

    @requests_mock.Mocker()
    def test_request(self, m):
        """Config options are respected when making requests."""

        config = dict(endpoint='https://test.com/path/',
                      token=str(uuid.uuid4()),
                      headers={'Custom': 'Field 123'})

        auth_headers = {'X-Auth-Token': config['token']}
        data = dict(answer=123)

        m.get(requests_mock.ANY, status_code=401)
        m.get(requests_mock.ANY, status_code=404, request_headers=auth_headers)
        m.get(config['endpoint'], json=data, request_headers=config['headers'])

        client = SAPIClient(**config)

        self.assertEqual(client.session.get('').json(), data)

    @requests_mock.Mocker()
    def test_non_json(self, m):
        """Non-JSON OK response is unexpected."""

        m.get(requests_mock.ANY, text='text', status_code=200)

        client = SAPIClient()

        with self.assertRaises(exceptions.ResourceBadResponseError) as exc:
            client.session.get('test')

    @requests_mock.Mocker()
    def test_structured_error_response(self, m):
        """Error response dict correctly initializes exc."""

        error_msg = "I looked, but couldn't find."
        error_code = 404
        error = dict(error_msg=error_msg, error_code=error_code)

        m.get(requests_mock.ANY, json=error, status_code=error_code)

        client = SAPIClient()

        with self.assertRaisesRegex(exceptions.ResourceNotFoundError, error_msg) as exc:
            client.session.get('test')

            self.assertEqual(exc.error_msg, error_msg)
            self.assertEqual(exc.error_code, error_code)

    @requests_mock.Mocker()
    def test_plain_text_error(self, m):
        """Error messages in plain text/body correctly initialize exc."""

        error_msg = "I looked, but couldn't find."
        error_code = 404

        m.get(requests_mock.ANY, text=error_msg, status_code=error_code)

        client = SAPIClient()

        with self.assertRaisesRegex(exceptions.ResourceNotFoundError, error_msg) as exc:
            client.session.get('test')

            self.assertEqual(exc.error_msg, error_msg)
            self.assertEqual(exc.error_code, error_code)

    @requests_mock.Mocker()
    def test_unknown_errors(self, m):
        """Unknown status code with plain text msg raised as general req exc."""

        error_msg = "I'm a teapot"
        error_code = 418

        m.get(requests_mock.ANY, text=error_msg, status_code=error_code)

        client = SAPIClient()

        with self.assertRaisesRegex(exceptions.RequestError, error_msg) as exc:
            client.session.get('test')

            self.assertEqual(exc.error_msg, error_msg)
            self.assertEqual(exc.error_code, error_code)