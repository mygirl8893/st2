# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import mock

from st2common.content import utils as content_utils
from st2common.bootstrap.configsregistrar import ConfigsRegistrar
from st2common.persistence.pack import Pack
from st2common.persistence.pack import Config

from st2tests import DbTestCase
from st2tests import fixturesloader


__all__ = [
    'ConfigsRegistrarTestCase'
]

PACK_PATH = os.path.join(fixturesloader.get_fixtures_packs_base_path(), 'dummy_pack_1')


class ConfigsRegistrarTestCase(DbTestCase):
    def test_register_configs_for_all_packs(self):
        # Verify DB is empty
        pack_dbs = Pack.get_all()
        config_dbs = Config.get_all()

        self.assertEqual(len(pack_dbs), 0)
        self.assertEqual(len(config_dbs), 0)

        registrar = ConfigsRegistrar(use_pack_cache=False)
        registrar._pack_loader.get_packs = mock.Mock()
        registrar._pack_loader.get_packs.return_value = {'dummy_pack_1': PACK_PATH}
        packs_base_paths = content_utils.get_packs_base_paths()
        registrar.register_configs_for_all_packs(base_dirs=packs_base_paths)

        # Verify pack and schema have been registered
        pack_dbs = Pack.get_all()
        config_dbs = Config.get_all()

        self.assertEqual(len(pack_dbs), 1)
        self.assertEqual(len(config_dbs), 1)

        config_db = config_dbs[0]
        self.assertEqual(config_db.values['api_key'], '{{user.api_key}}')
        self.assertEqual(config_db.values['api_secret'], '{{user.api_secret}}')
        self.assertEqual(config_db.values['region'], 'us-west-1')
