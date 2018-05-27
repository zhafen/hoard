#!/usr/bin/env python
'''Object for managing settings, e.g. for treasure chest drop rate,
gold conversion rate, etc.

@author: Zach Hafen
@contact: zachary.h.hafen@gmail.com
@status: Development
'''

import apiclient.discovery as api_discovery
import apiclient.http as api_http
import httplib2
import io
import math
import oauth2client
import os
import pandas as pd

import hoard.utils.utilities as utilities
import hoard.config as hoard_config

########################################################################
########################################################################

class Settings( object ):

    @utilities.store_parameters
    def __init__(
        self,
        username,
        data_dir,
        import_data_on_startup = False,
    ):
        pass

        if import_data_on_startup:
            self.retrieve_google_drive_data(
                hoard_config.DRIVE_FOLDER_NAME,
                hoard_config.CLIENT_SECRET_FILEPATH,
            )

    ########################################################################

    @property
    def settings_table( self ):
        '''Open and store the table containing overall settings.
        '''

        if not hasattr( self, '_settings_table' ):
            filepath = os.path.join(
                self.data_dir, 'settings.xlsx' )
            full_settings_table = pd.read_excel( filepath, index_col=0 )

            self._settings_table = full_settings_table.loc[self.username]

        return self._settings_table

    ########################################################################

    @property
    def loot_table( self ):
        '''Open and store the loot table for the user.
        The loot table contains different item types, and their probability to drop.
        '''

        if not hasattr( self, '_loot_table' ):
            filepath = os.path.join(
                self.data_dir, 'loot_tables', self.username, 'loot_table.xlsx' )
            self._loot_table = pd.read_excel( filepath )

        return self._loot_table

    ########################################################################

    @property
    def loot_probabilities( self ):
        '''Get the probability for different loot types to drop. The reason this
        isn't pulled straight from the table is because the probability might not
        be normalized.
        '''

        loot_probabilities = self.loot_table['Likelihood'].values
        return loot_probabilities/loot_probabilities.sum()

    ########################################################################

    @property
    def loot_expected_values( self ):
        '''Get the expected value out for each item category.
        '''

        if not hasattr( self, '_loot_expected_values' ):

            self._loot_expected_values = []
            for item_table in self.item_tables:

                expected_value = item_table['Value'].mean()

                self._loot_expected_values.append( expected_value )

        return self._loot_expected_values

    ########################################################################

    @property
    def item_tables( self ):
        '''Get detailed information about items can drop, for a given category.
        '''

        if not hasattr( self, '_item_tables' ):
            
            self._item_tables = []
            for item_type in self.loot_table['Item Type']:

                item_type_name = item_type.lower().replace( ' ', '_' )
                itype_table_filename = 'itype_{}.xlsx'.format( item_type_name )
                table_filepath = os.path.join(
                    self.data_dir,
                    'loot_tables',
                    self.username,
                    itype_table_filename,
                )

                self._item_tables.append( pd.read_excel( table_filepath ) )

        return self._item_tables

    ########################################################################

    @property
    def average_token_value( self ):
        '''Get the total average value of a token.'''

        total_value = self.settings_table['Loot Value'] + self.settings_table['Gold Value']
        return float( total_value ) / self.settings_table['Total Tokens']

    ########################################################################

    @property
    def average_token_loot_value( self ):
        '''Get the average value of a token that is reward.'''

        return float( self.settings_table['Loot Value'] ) / self.settings_table['Total Tokens']

    ########################################################################

    @property
    def p_gold( self ):
        '''Get the probability of returning gold when spending a token.'''

        average_treasure_value = ( self.loot_probabilities * self.loot_expected_values ).sum()

        return 1. - self.average_token_loot_value / average_treasure_value

    ########################################################################

    def time_to_tokens( self, time ):
        '''Get the amount of tokens equivalent to spending some amount of time on things.

        Args:
            time (float) : time in hours spent.

        Returns:
            n_tokens (int) : equivalent number of tokens.
        '''

        return int( math.ceil( time*self.settings_table['Tokens Per Hour'] ) )

    ########################################################################

    def retrieve_google_drive_data(
        self,
        drive_dir_name,
        client_secret_file,
    ):
        '''Retrieve data from a google drive. This is hacked together from examples so... no guarantees it works.
        There is a test for it.

        Args:

            drive_dir_name (str) : Name of the google drive folder to get data from.

            client_secret_file (str) : client_secrets.json filepath
        '''


        # Make the target directory
        utilities.make_dir( self.data_dir )

        # Setup the Drive v3 API
        SCOPES = 'https://www.googleapis.com/auth/drive'
        store = oauth2client.file.Storage('credentials.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = oauth2client.client.flow_from_clientsecrets(client_secret_file, SCOPES)
            creds = oauth2client.tools.run_flow(flow, store)
        service = api_discovery.build('drive', 'v3', http=creds.authorize(httplib2.Http()))

        def export_spreadsheet( file_id, export_dir, export_name ):

            # Make the request
            request = service.files().export_media(
                fileId=file_id,
                mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            )

            # Make the save dir available
            utilities.make_dir( export_dir )
            export_path = os.path.join( export_dir, export_name )
            print( "Retrieving {}".format( export_path ) )
            fh = io.FileIO( export_path, 'wb' )

            # Download the file
            downloader = api_http.MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()

        def get_file( query ):
            '''Get a particular file that matches the given query. If multiple files match rais an Error.'''

            potential_files = service.files().list( q=query ).execute()
            assert len( potential_files['files'] ) == 1, "Multiple possible folders detected."
            return potential_files['files'][0]

        # Find the Drive dir
        query = "name='{}'".format( drive_dir_name )
        drive_dir = get_file( query )

        # Download the settings
        query = "parents='{}' and name='settings'".format( drive_dir['id'] )
        settings = get_file( query )
        export_spreadsheet( settings['id'], self.data_dir, 'settings.xlsx' )

        # Get the user data
        query = "parents='{}' and name='loot_tables'".format( drive_dir['id'] )
        user_data_folder = get_file( query )
        query = "parents='{}'".format( user_data_folder['id'] )
        user_data = service.files().list( q=query ).execute()
        for specific_user_data in user_data['files']:

            # Get the save dir
            save_dir = os.path.join( self.data_dir, 'loot_tables', specific_user_data['name'] )

            # Save each file
            query = "parents='{}'".format( specific_user_data['id'] )
            user_files = service.files().list( q=query ).execute()['files']
            for user_file in user_files:

                if user_file['mimeType'] == 'application/vnd.google-apps.spreadsheet':
                    save_name = '{}.xlsx'.format( user_file['name'] )
                    export_spreadsheet( user_file['id'], save_dir, save_name )
