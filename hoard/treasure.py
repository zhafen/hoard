#!/usr/bin/env python
'''Treausre objects, e.g. TreasureChests

@author: Zach Hafen
@contact: zachary.h.hafen@gmail.com
@status: Development
'''

########################################################################
########################################################################

class TreasureChest( object ):

    def __init__(
        self,
        user,
        data_location,
    ):

    ########################################################################

    def generate_item( self ):

        # Figure out if the item is just gold
        gold_ps = np.array([ self.p_gold, 1. - self.p_gold ])
        gold_ind = prob_tools.sample_discrete_probabilities( gold_ps )
        is_gold = gold_ind == 0

        # If we got gold, exit early
        if is_gold:
            self.contained_gold += np.random.randint( self.settings['gold_low'], self.settings['gold_high'] )

            return

        # Determine what item type dropped
        item_type_ind = prob_tools.sample_discrete_probabilities( self.item_type_ps )

        # Determine what item of the item types dropped.

        # Append to the list of items

    ########################################################################

    def generate_contents( self, n_items ):

        for i in range( n_items ):
            self.generate_item()

