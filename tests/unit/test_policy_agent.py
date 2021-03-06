# Copyright 2015 Metaswitch Networks
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import unittest

from mock import patch, MagicMock, ANY, call
from nose.tools import assert_equal, assert_false, assert_raises
from nose_parameterized import parameterized
from pycalico.datastore_datatypes import Rule, Rules
from pycalico.datastore import DatastoreClient

from policy_agent import *


class PolicyAgentTest(unittest.TestCase):
    """
    Test class for the policy agent.
    """
    def setUp(self):
        self.agent = PolicyAgent()
        self.agent._client = MagicMock(spec=DatastoreClient)

    def test_read_updates(self):
        # Mock out processing of the update to fail.
        self.agent._process_update = MagicMock(spec=self.agent._process_update)
        err = Exception()
        self.agent._process_update.side_effect = err 

        # Add to the event queue.
        event = ("event_type", "resource_type", {})
        self.agent._event_queue.put(event)

        try:
            # Will throw exception - needed to escape infinite loop.
            self.agent.read_updates()
        except Exception, e:
            if err is e:
                pass
            else:
                raise
