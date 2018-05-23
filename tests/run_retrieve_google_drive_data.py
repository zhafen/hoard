#!/usr/bin/env python
'''Script for retrieving google drive data. Used primarily in testing

@author: Zach Hafen
@contact: zachary.h.hafen@gmail.com
@status: Development
'''

import hoard.settings as hoard_settings

settings = hoard_settings.Settings( 'steven' )

settings.retrieve_google_drive_data(
    'test_hoard_data',
    './tests/data/test_google_drive_data',
    './tests/data/client_secret.json',
)
