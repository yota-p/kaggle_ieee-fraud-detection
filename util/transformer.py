import pandas as pd
from feature.feature_factory import FeatureFactory
from logging import getLogger
logger = getLogger('main')
from pathlib import Path

from util.mylog import timer
from util.islatest import is_latest


class Transformer:

    @classmethod
    @timer
    def run(cls,
            features,
            use_small_data,
            out_train_path,
            out_test_path,
            ):
        '''
        Create features and return datas for training
        '''
        # check if output exists, read from file
        if is_latest([Path(out_train_path), Path(out_test_path)]):
            logger.debug('All files existed. Skip transforming.')
            train = pd.read_pickle(str(out_train_path))
            test = pd.read_pickle(str(out_test_path))
            logger.debug(f'Loaded train.shape: {train.shape}')
            logger.debug(f'Loaded test.shape:  {test.shape}')
            return train, test

        # Get key columns
        factory = FeatureFactory()
        raw = factory.create('raw')
        train_raw, test_raw = raw.create_feature()
        train = train_raw[['TransactionID']]
        test = test_raw[['TransactionID']]

        # For column: create features
        for namespace in features:
            feature = factory.create(namespace)
            train_feature, test_feature = feature.create_feature()

            # check if row # match before merge
            if not len(train.index) == len(train_feature.index):
                raise TypeError(f'Unable to merge: length of train and feature_train does not match.')
            if not len(test.index) == len(test_feature.index):
                raise TypeError(f'Unable to merge: length of test and feature_test does not match.')

            train = pd.merge(train, train_feature, how='left', on='TransactionID')
            test = pd.merge(test, test_feature, how='left', on='TransactionID')
            del feature, train_feature, test_feature

        train = train.sort_values(by=['TransactionDT'])
        test = test.sort_values(by=['TransactionDT'])

        if use_small_data:
            frac = 0.001
            train = train.sample(frac=frac, random_state=42)
            test = test.sample(frac=frac, random_state=42)
            logger.debug(f'use_small_data is {use_small_data}. Using {frac*100} % of data.')
        else:
            logger.debug(f'use_small_data is {use_small_data}. Using all data.')

        # save processed data
        train.to_pickle(out_train_path)
        test.to_pickle(out_test_path)

        logger.debug(f'Created {out_train_path} shape: {train.shape}')
        logger.debug(f'Created {out_test_path} shape: {test.shape}')

        return train, test
