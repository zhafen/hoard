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
        client_credential_file,
    ):
        '''Retrieve data from a google drive. This is hacked together from examples so... no guarantees it works.

        Args:
            target_dir (str) : Directory to save the data at.
        '''


        # Make the target directory
        utilities.make_dir( target_dir )

        # Setup the Drive v3 API
        SCOPES = 'https://www.googleapis.com/auth/drive'
        store = oauth2client.file.Storage('credentials.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = oauth2client.client.flow_from_clientsecrets(client_credential_file, SCOPES)
            creds = oauth2client.tools.run_flow(flow, store)
        service = api_discovery.build('drive', 'v3', http=creds.authorize(httplib2.Http()))

        # Call the Drive v3 API
        # results = service.files().list(
        #     pageSize=10, fields="nextPageToken, files(id, name)").execute()
        # items = results.get('files', [])
        # if not items:
        #     print('No files found.')
        # else:
        #     for item in items:
        #         if item['name'] == drive_dir_name:
        #             print('{0} ({1})'.format(item['name'], item['id']))

        #             file_name = item['name']
        #             file_id = item['id']

        def export_spreadsheet( file_id, export_dir, export_name ):
            request = service.files().export_media(
                fileId=file_id,
                mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            )

            utilities.make_dir( export_dir )
            export_path = os.path.join( export_dir, export_name )
            fh = io.FileIO( export_path, 'wb' )

            downloader = api_http.MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print "Download %d%%." % int(status.progress() * 100)

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
        filename = os.path.join( target_dir, 'settings.xlsx' )
        export_spreadsheet( settings['id'], filename )

        #DEBUG
        import pdb; pdb.set_trace()


        
