#!/usr/bin/env python
'''Testing for settings.py

@author: Zach Hafen
@contact: zachary.h.hafen@gmail.com
@status: Development
'''

import numpy as np
import numpy.testing as npt
import os
import shutil
import unittest

import hoard.settings as hoard_settings

########################################################################

data_dir = './tests/data/test_google_drive_data'

########################################################################
########################################################################

class TestRetrieveGoogleDriveData( unittest.TestCase ):

    def setUp( self ):

        if os.path.isdir( data_dir ):
            shutil.rmtree( data_dir )

        self.settings = hoard_settings.Settings(
            'steven',
        )

    ########################################################################

    def test_retrieve_google_drive_data( self ):

        # self.settings.retrieve_google_drive_data(
        #     data_dir,
        #     './tests/data/client_secret.json',
        # )
        os.system( './tests/run_retrieve_google_drive_data.py' )

        assert os.path.isdir( data_dir )
        assert os.path.is_file( os.path.join( data_dir, 'settings.xlsx' ) )
        assert os.path.is_file(
            os.path.join( data_dir, 'users', 'steven', 'loot_table.xlsx' )
        )
        assert os.path.is_file(
            os.path.join( data_dir, 'users', 'steven', 'itype_donut.xlsx' )
        )


