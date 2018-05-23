#!/usr/bin/env python
'''General utilities

@author: Zach Hafen
@contact: zachary.h.hafen@gmail.com
@status: Development
'''

import errno
import functools
import inspect
import os

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

        self.stored_parameters = parameters_to_store.keys()

        result = constructor( self, *args, **kwargs )

    return wrapped_constructor

def make_dir( dir ):

    # Make sure the output directory exists
    try:
        os.makedirs( dir )
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir( dir ):
            pass
        else:
            raise
