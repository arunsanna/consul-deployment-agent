# Copyright (c) Trainline Limited, 2016. All rights reserved. See LICENSE.txt in the project root for license information.

import json

class Service:
    def __init__(self, definition, installation_info={}):
        self.address = definition.get('Address')
        self.installation = {
            'timeout':installation_info.get('InstallationTimeout', 60) * 60,
            'package_bucket':installation_info.get('PackageBucket'),
            'package_key':installation_info.get('PackageKey')
        }
        self.id = definition.get('ID')
        self.name = definition.get('Name')
        if self.name is None:
            self.name = definition.get('Service')
        self.port = int(definition.get('Port', 0))
        self.tags = definition.get('Tags', [])
        self.deployment_id = self._extract_tag_with_prefix('deployment_id:')
        self.slice = self._extract_tag_with_prefix('slice:')
        self.version = self._extract_tag_with_prefix('version:')
        self._validate()

    def __eq__(self, other):
        return self.id == other.id and self.deployment_id == other.deployment_id

    def __str__(self):
        return json.dumps(
            {'id': self.id, 'name': self.name, 'port': self.port,
             'slice': self.slice, 'version': self.version, 'tags': self.tags})

    def _extract_tag_with_prefix(self, prefix):
        tag = next((tag for tag in self.tags if tag.startswith(prefix)), None)
        if tag is not None:
            return tag[len(prefix):]
        return None

    def _validate(self):
        if self.address is None:
            raise ValueError('Service address must be specified.')
        if self.id is None:
            raise ValueError('Service ID must be specified.')
        if self.name is None:
            raise ValueError('Service name must be specified.')

    def tag(self, prefix, value):
        self.tags = [tag for tag in self.tags if not tag.startswith(prefix)]
        self.tags.append('{0}{1}'.format(prefix, value))
