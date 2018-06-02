#!/usr/bin/env python
'''Treausre objects, e.g. TreasureChests

@author: Zach Hafen
@contact: zachary.h.hafen@gmail.com
@status: Development
'''

import numpy as np
import os
import pandas as pd

import hoard.utils.utilities as utilities

########################################################################
########################################################################

class Bank( object ):

    @utilities.store_parameters
    def __init__(
        self,
        settings,
    ):
        pass

    ########################################################################

    @property
    def gold_record( self ):
        '''Record of all gold transactions.'''

        if not hasattr( self, '_gold_record' ):
            filepath = os.path.join(
                self.settings.data_dir,
                'loot_tables',
                self.settings.username,
                'gold_record.xlsx',
            )
            self._gold_record = pd.read_excel( filepath )

        return self._gold_record

    @gold_record.setter
    def gold_record( self, value ):
        self._gold_record = value

        filepath = os.path.join(
            self.settings.data_dir,
            'loot_tables',
            self.settings.username,
            'gold_record.xlsx',
        )
        self._gold_record.to_excel( filepath )

    ########################################################################

    @property
    def gold( self ):
        '''Current gold balance.'''

        return self.gold_record['Balance'].values[-1]

    ########################################################################

    @property
    def item_record( self ):
        '''Record of all gold transactions.'''

        if not hasattr( self, '_item_record' ):
            filepath = os.path.join(
                self.settings.data_dir,
                'loot_tables',
                self.settings.username,
                'item_record.xlsx',
            )
            self._item_record = pd.read_excel( filepath )

        return self._item_record

    @item_record.setter
    def item_record( self, value ):
        self._item_record = value

        filepath = os.path.join(
            self.settings.data_dir,
            'loot_tables',
            self.settings.username,
            'item_record.xlsx',
        )
        self._item_record.to_excel( filepath )

    ########################################################################

    def deposit( self, chest ):
        '''Store the contents of a chest in the bank.'''

        self.deposit_gold( chest )

        self.deposit_items( chest )

        # Print results
        print( "Chest deposited! Current balance is {} gold.".format( self.gold ) )

    ########################################################################

    def deposit_gold( self, chest ):
        '''Store all the gold in a chest in the bank.'''

        assert chest.id not in self.gold_record['Chest ID'].values, \
            "Chest ID already stored in bank! Cannot double deposit!"

        # Construct series to deposit
        values = {
            'Deposit/Withdrawal' : chest.gold,
            'Balance' : chest.gold + self.gold,
            'Time' : pd.Timestamp.now(),
            'Chest ID' : chest.id,
        }
        series = pd.Series( values )

        # Make the deposit
        self.gold_record = self.gold_record.append( series, ignore_index=True )

    ########################################################################

    def deposit_items( self, chest ):
        '''Store all the items in a chest in the bank.'''

        self.item_record = self.item_record.append( chest.items, ignore_index=True )
