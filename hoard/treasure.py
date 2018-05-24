#!/usr/bin/env python
'''Treausre objects, e.g. TreasureChests

@author: Zach Hafen
@contact: zachary.h.hafen@gmail.com
@status: Development
'''

import numpy as np
import pandas as pd

import hoard.settings as hoard_settings

import hoard.utils.probability_tools as prob_tools
import hoard.utils.utilities as utilities

########################################################################
########################################################################

class TreasureChest( object ):

    @utilities.store_parameters
    def __init__(
        self,
        username,
        data_location,
        n_tokens,
    ):

        self.settings = hoard_settings.Settings(
            username,
            data_location,
        )

        # Initial values
        self.gold = 0
        self.items = []

        self.generate_contents( n_tokens )

        # Format the items
        if len( self.items ) == 0:
            self.items = None
        else:
            self.items = pd.concat( self.items, axis=1, ignore_index=True )
            self.items = self.items.transpose()

    ########################################################################

    def generate_item( self ):
        '''Generate an item to store in the chest.'''

        # Figure out if the item is just gold
        gold_ps = np.array([ self.settings.p_gold, 1. - self.settings.p_gold ])
        gold_ind = prob_tools.sample_discrete_probabilities( gold_ps )
        is_gold = gold_ind == 0

        # If we got gold, exit early
        if is_gold:
            self.gold += np.random.randint( 1, 10 )

            return

        # Determine what item type dropped
        item_type_ps = self.settings.loot_table['Probability'].values
        item_type_ind = prob_tools.sample_discrete_probabilities( item_type_ps )

        # Determine what item of the item types dropped.
        itype_table = self.settings.item_tables[item_type_ind]
        item = itype_table.loc[np.random.randint( len( itype_table ) )]

        # Append to the list of items
        self.items.append( item )

    ########################################################################

    def generate_contents( self, n_tokens ):
        '''Generate the contents of the chest.'''

        for i in range( n_tokens ):
            self.generate_item()

