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

    ########################################################################

    def test_retrieve_google_drive_data( self ):

        os.system( 'python ./tests/run_retrieve_google_drive_data.py' )

        assert os.path.isdir( data_dir )
        assert os.path.isfile( os.path.join( data_dir, 'settings.xlsx' ) )
        assert os.path.isfile(
            os.path.join( data_dir, 'loot_tables', 'steven', 'loot_table.xlsx' )
        )
        assert os.path.isfile(
            os.path.join( data_dir, 'loot_tables', 'steven', 'itype_donut.xlsx' )
        )


