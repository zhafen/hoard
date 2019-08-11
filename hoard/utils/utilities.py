#!/usr/bin/env python
'''General utilities

@author: Zach Hafen
@contact: zachary.h.hafen@gmail.com
@status: Development
'''

import copy
import errno
import functools
import inspect
import os
import pandas as pd

########################################################################
########################################################################

def store_parameters( constructor ):
    '''Decorator for automatically storing arguments passed to a constructor.
    I.e. any args passed to constructor via
    test_object = TestObject( *args, **kwargs )
    will be stored in test_object, e.g. test_object.args

    Args:
        constructor (function) : Constructor to wrap.
    '''

    @functools.wraps( constructor )
    def wrapped_constructor( self, *args, **kwargs ):

        parameters_to_store = inspect.getcallargs( constructor, self, *args, **kwargs )

        # Make sure we don't accidentally try to save the self argument
        del parameters_to_store['self']

        for parameter in parameters_to_store.keys():
            setattr( self, parameter, parameters_to_store[parameter] )

        self.stored_parameters = list( parameters_to_store.keys() )

        result = constructor( self, *args, **kwargs )

    return wrapped_constructor

########################################################################

def make_dir( dir ):

    # Make sure the output directory exists
    try:
        os.makedirs( dir )
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir( dir ):
            pass
        else:
            raise

########################################################################

def generic_table_getter(
    instance,
    property_name,
    root_folder,
    subfolders=[],
    filetype = 'xlsx',
    index_col = None,
):
    '''Generic property for loading in an excel file in a subdirectory.'''

    hidden_attr = '_{}'.format( property_name )

    if not hasattr( instance, hidden_attr ):

        # Set up the subfolders
        used_subfolders = copy.copy( subfolders )
        used_subfolders.append( '{}.{}'.format( property_name, filetype ) )

        filepath = os.path.join( root_folder, *used_subfolders )

        df = pd.read_excel( filepath, index_col=index_col )

        setattr( instance, hidden_attr, df )

    return getattr( instance, hidden_attr )

########################################################################

def generic_table_setter(
    instance,
    property_name,
    value,
    root_folder,
    subfolders=[],
    filetype = 'xlsx',
):
    '''Generic property for saving a table when it's updated.'''

    hidden_attr = '_{}'.format( property_name )

    setattr( instance, hidden_attr, value )

    # Set up the subfolders
    make_dir( os.path.join( root_folder, *subfolders ) )
    used_subfolders = copy.copy( subfolders )
    used_subfolders.append( '{}.{}'.format( property_name, filetype ) )
    filepath = os.path.join( root_folder, *used_subfolders )

    value.to_excel( filepath )
