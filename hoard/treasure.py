#!/usr/bin/env python
'''Treasure objects, e.g. TreasureChests

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
        settings = None,
        n_tokens = None,
        time = None,
        bonus_factor = 1.,
        *args, **kwargs
    ):

        self.id = np.random.randint( 1e12 )

        if self.settings is None:
            self.settings = hoard_settings.Settings(
                *args, **kwargs
            )

        n_tokens_used = 0

        if n_tokens is not None:
            n_tokens_used += n_tokens

        if time is not None:
            n_tokens_used += self.settings.time_to_tokens( time )

        n_tokens_used = int( n_tokens_used * bonus_factor )

        self.generate_contents( n_tokens_used )

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
        item_type_ps = self.settings.loot_table['Likelihood'].values.astype( float )
        item_type_ind = prob_tools.sample_discrete_probabilities( item_type_ps )

        # Determine what item of the item types dropped.
        itype_table = self.settings.item_tables[item_type_ind]
        item = itype_table.loc[np.random.randint( len( itype_table ) )]

        # Add extra information
        item.set_value( 'Item Type', self.settings.loot_table['Item Type'].loc[item_type_ind] )
        item.set_value( 'Identified', self.settings.loot_table['Identified'].loc[item_type_ind] )
        item.set_value( 'Chest ID', self.id )

        # Append to the list of items
        self.items.append( item )

    ########################################################################

    def generate_contents( self, n_tokens ):
        '''Generate the contents of the chest.'''

        # Initial values
        self.gold = 0
        self.items = []

        for i in range( n_tokens ):
            self.generate_item()

        # Format the items
        if len( self.items ) == 0:
            self.items = None
        else:
            self.items = pd.concat( self.items, axis=1, ignore_index=True )
            self.items = self.items.transpose()

    ########################################################################

    def open( self ):
        '''Print the contents of the chest.'''

        print( "You open a chest! In the chest you find..." )

        if self.items is not None:
            for i in self.items.index:
                
                item = self.items.loc[i]

                if item['Identified']:
                    print( "a {},".format( item['Name'] ) )
                else:
                    print( "an unidentified {},".format( item['Item Type'] ) )

            print( "and {} gold!".format( self.gold ) )

        else:
            print( "{} gold!".format( self.gold ) )


