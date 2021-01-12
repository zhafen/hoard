#!/usr/bin/env python
'''Testing for probability distribution tools.

@author: Zach Hafen
@contact: zachary.h.hafen@gmail.com
@status: Development
'''

import numpy as np
import numpy.testing as npt
import unittest

import hoard.utils.probability_tools as prob_tools

########################################################################
########################################################################

class TestSampleDiscreteProbabilities( unittest.TestCase ):

    ########################################################################

    def test_sample_discrete_probabilities( self ):

        # Setup a seed
        np.random.seed( 1234 )

        ps = np.array([ 0.1, 0.3, 0.6 ])

        n_sample = 10000

        expected = ps*n_sample

        # Get the sample out
        inds = []
        for i in range( n_sample ):
            ind = prob_tools.sample_discrete_probabilities( ps )
            inds.append( ind )
        inds = np.array( inds )

        # Count up the sample
        actual = []
        for i in range( ps.size ):
            n_i = ( inds == i ).sum()
            actual.append( n_i )

        npt.assert_allclose( expected, actual, atol=np.sqrt( n_sample ) )

    ########################################################################

    def test_sample_discrete_probabilities_norm_ps( self ):
        '''Test that the normalize_ps functionality works.
        '''

        # Setup a seed
        np.random.seed( 1234 )

        original_ps = np.array([ 0.1, 0.3, 0.6 ])
        ps = 10. * original_ps

        n_sample = 10000

        expected = original_ps*n_sample

        # Get the sample out
        inds = []
        for i in range( n_sample ):
            ind = prob_tools.sample_discrete_probabilities( ps )
            inds.append( ind )
        inds = np.array( inds )

        # Count up the sample
        actual = []
        for i in range( ps.size ):
            n_i = ( inds == i ).sum()
            actual.append( n_i )

        npt.assert_allclose( expected, actual, atol=np.sqrt( n_sample ) )


