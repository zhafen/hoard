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
import oauth2client
import os

import hoard.utils.utilities as utilities

########################################################################
########################################################################

class Settings( object ):

    @utilities.store_parameters
    def __init__(
        self,
        username,
    ):
        pass

    ########################################################################

    def retrieve_google_drive_data(
        self,
        drive_dir_name,
        target_dir,
        client_secret_file,
    ):
        '''Retrieve data from a google drive. This is hacked together from examples so... no guarantees it works.

        Args:

            drive_dir_name (str) : Name of the google drive folder to get data from.

            target_dir (str) : Directory to save the data at.

            client_secret_file (str) : client_secrets.json filepath
        '''


        # Make the target directory
        utilities.make_dir( target_dir )

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

        # Find the target_dir
        query = "name='{}'".format( drive_dir_name )
        drive_dir = get_file( query )

        # Download the settings
        query = "parents='{}' and name='settings'".format( drive_dir['id'] )
        settings = get_file( query )
        export_spreadsheet( settings['id'], target_dir, 'settings.xlsx' )

        # Get the user data
        query = "parents='{}' and name='users'".format( drive_dir['id'] )
        user_data_folder = get_file( query )
        query = "parents='{}'".format( user_data_folder['id'] )
        user_data = service.files().list( q=query ).execute()
        for specific_user_data in user_data['files']:

            # Get the save dir
            save_dir = os.path.join( target_dir, 'users', specific_user_data['name'] )

            # Save each file
            query = "parents='{}'".format( specific_user_data['id'] )
            user_files = service.files().list( q=query ).execute()['files']
            for user_file in user_files:

                if user_file['mimeType'] == 'application/vnd.google-apps.spreadsheet':
                    save_name = '{}.xlsx'.format( user_file['name'] )
                    export_spreadsheet( user_file['id'], save_dir, save_name )
