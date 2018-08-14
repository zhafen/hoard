#!/usr/bin/env python
'''Tools for sampling probability distributions

@author: Zach Hafen
@contact: zachary.h.hafen@gmail.com
@status: Development
'''

import copy
import numpy as np

########################################################################
########################################################################

def sample_discrete_probabilities( ps, normalize=True ):
    '''Given a list of event probabilities, find the event that occured.

    Args:
        ps (np.ndarray) : Event probabilities.

        normalize (bool) :
            If the probabilities do not sum to one, make sure they do.

    Returns:
        event_ind (int) : Index of event.
    '''

    ps = copy.copy( ps ).astype( float )

    if normalize:
        ps /= ps.sum()

    # Set up the cumulative probabilities
    cumulatives = ps.cumsum()
    cumulatives = np.insert( cumulatives, 0, 0. )

    x = np.random.uniform() > cumulatives

    return np.argmin( x ) - 1
