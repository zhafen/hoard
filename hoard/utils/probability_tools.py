#!/usr/bin/env python
'''Tools for sampling probability distributions

@author: Zach Hafen
@contact: zachary.h.hafen@gmail.com
@status: Development
'''

import numpy as np

########################################################################
########################################################################

def sample_discrete_probabilities( ps, normalize_ps=True ):
    '''Given a list of event probabilities, find the event that occured.

    Args:
        ps (np.ndarray) : Event probabilities.

        normalize_ps (bool) :
            If the probabilities do not sum to one, make sure they do.

    Returns:
        event_ind (int) : Index of event.
    '''

    if normalize_ps:
        ps /= ps.sum()

    # Set up the cumulative probabilities
    cumulatives = ps.cumsum()
    cumulatives = np.insert( cumulatives, 0, 0. )

    x = np.random.uniform() > cumulatives

    return np.argmin( x ) - 1


    

