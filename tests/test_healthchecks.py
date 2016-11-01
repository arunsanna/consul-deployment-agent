# Copyright (c) Trainline Limited, 2016. All rights reserved. See LICENSE.txt in the project root for license information.

import unittest
from mock import MagicMock, Mock

from .context import agent
from agent import key_naming_convention
from agent.deployment_stages import RegisterConsulHealthChecks, DeploymentError

healthchecks = {
    'check_failing': {
        'type': 'script'
    },
    'check_2': {
        'type': 'http'
    }
}

class MockLogger:
  def __init__(self):
    self.info = Mock()
    self.error = Mock()
    self.debug = Mock()

class MockDeployment:
    def __init__(self):
        self.logger = MockLogger()
        self.archive_dir = ''
        self.appspec = {
            'healthchecks': healthchecks
        }
    def set_check(self, check_id, check):
        self.appspec = {
            'consul_healthchecks': {
                check_id: check
            }
        }


class TestHealthChecks(unittest.TestCase):
    def setUp(self):
        self.deployment = MockDeployment()
        self.tested_fn = RegisterConsulHealthChecks()
        
    def test_failing_check(self):
        check = {
            'type': 'unknown'
        }
        self.deployment.set_check('check_failing', check)
        with self.assertRaisesRegexp(DeploymentError, 'only.*check types are supported'):
            self.tested_fn._run(self.deployment)

    def test_missing_name_field(self):
        check = {
            'type': 'http'
        }
        self.deployment.set_check('check_failing', check)
        with self.assertRaisesRegexp(DeploymentError, 'is missing field'):
            self.tested_fn._run(self.deployment)

    def test_missing_http_field(self):
        check = {
            'type': 'http',
            'name': 'Missing http'
        }
        self.deployment.set_check('check_failing', check)
        with self.assertRaisesRegexp(DeploymentError, 'is missing field \'http\''):
            self.tested_fn._run(self.deployment)



