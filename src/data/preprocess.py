import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import gc
from utils import pickleWrapper as pw
from config import project
import luigi
from luigi.util import requires


class TaskPickleRawData(luigi.Task):

    def output(self):
        return luigi.run(['TaskPreprocess', '--workers', '1', '--local-scheduler'])


def output():
    dir = project.rootdir + 'data/raw/'
    out_files = ['train_identity.pickle',
                 'train_transaction.pickle',
                 'test_identity.pickle',
                 'train_transaction.pickle',
                 'train_identity.pickle']
    for file in out_files:
        out_data = dir + file
    return out_data


def pickle_raw_data():
    dir = project.rootdir + 'data/raw/'

    train_identity = pd.read_csv(f'{dir}train_identity.csv')
    train_transaction = pd.read_csv(f'{dir}train_transaction.csv')
    test_identity = pd.read_csv(f'{dir}test_identity.csv')
    test_transaction = pd.read_csv(f'{dir}test_transaction.csv')
    sample_submission = pd.read_csv(f'{dir}sample_submission.csv')

    pw.dump(train_identity,    f'{dir}train_identity.pickle',    'wb')
    pw.dump(train_transaction, f'{dir}train_transaction.pickle', 'wb')
    pw.dump(test_identity,     f'{dir}test_identity.pickle',     'wb')
    pw.dump(test_transaction,  f'{dir}test_transaction.pickle',  'wb')
    pw.dump(sample_submission, f'{dir}sample_submission.pickle',    'wb')


def run():

    pickle_raw_data()

    # load raw data
    dir = project.rootdir + 'data/raw/'
    train_identity = pw.load(f'{dir}train_identity.pickle', 'wb')
    train_transaction = pw.load(f'{dir}train_transaction.pickle', 'wb')
    test_identity = pw.load(f'{dir}test_identity.pickle', 'wb')
    test_transaction = pw.load(f'{dir}test_transaction.pickle', 'wb')

    '''
    # let's combine the data and work with the whole dataset
    train = pd.merge(train_transaction, train_identity, on='TransactionID', how='left')
    test = pd.merge(test_transaction, test_identity, on='TransactionID', how='left')
    # no longer needed
    del train_identity, train_transaction, test_identity, test_transaction

    one_value_cols = [col for col in train.columns if train[col].nunique() <= 1]
    one_value_cols_test = [col for col in test.columns if test[col].nunique() <= 1]

    # Featre engineering
    train['TransactionAmt_to_mean_card1'] = train['TransactionAmt'] / \
        train.groupby(['card1'])['TransactionAmt'].transform('mean')
    train['TransactionAmt_to_mean_card4'] = train['TransactionAmt'] / \
        train.groupby(['card4'])['TransactionAmt'].transform('mean')
    train['TransactionAmt_to_std_card1'] = train['TransactionAmt'] / \
        train.groupby(['card1'])['TransactionAmt'].transform('std')
    train['TransactionAmt_to_std_card4'] = train['TransactionAmt'] / \
        train.groupby(['card4'])['TransactionAmt'].transform('std')

    test['TransactionAmt_to_mean_card1'] = test['TransactionAmt'] / \
        test.groupby(['card1'])['TransactionAmt'].transform('mean')
    test['TransactionAmt_to_mean_card4'] = test['TransactionAmt'] / \
        test.groupby(['card4'])['TransactionAmt'].transform('mean')
    test['TransactionAmt_to_std_card1'] = test['TransactionAmt'] / \
        test.groupby(['card1'])['TransactionAmt'].transform('std')
    test['TransactionAmt_to_std_card4'] = test['TransactionAmt'] / \
        test.groupby(['card4'])['TransactionAmt'].transform('std')

    train['id_02_to_mean_card1'] = train['id_02'] / train.groupby(['card1'])['id_02'].transform('mean')
    train['id_02_to_mean_card4'] = train['id_02'] / train.groupby(['card4'])['id_02'].transform('mean')
    train['id_02_to_std_card1'] = train['id_02'] / train.groupby(['card1'])['id_02'].transform('std')
    train['id_02_to_std_card4'] = train['id_02'] / train.groupby(['card4'])['id_02'].transform('std')

    test['id_02_to_mean_card1'] = test['id_02'] / test.groupby(['card1'])['id_02'].transform('mean')
    test['id_02_to_mean_card4'] = test['id_02'] / test.groupby(['card4'])['id_02'].transform('mean')
    test['id_02_to_std_card1'] = test['id_02'] / test.groupby(['card1'])['id_02'].transform('std')
    test['id_02_to_std_card4'] = test['id_02'] / test.groupby(['card4'])['id_02'].transform('std')

    train['D15_to_mean_card1'] = train['D15'] / train.groupby(['card1'])['D15'].transform('mean')
    train['D15_to_mean_card4'] = train['D15'] / train.groupby(['card4'])['D15'].transform('mean')
    train['D15_to_std_card1'] = train['D15'] / train.groupby(['card1'])['D15'].transform('std')
    train['D15_to_std_card4'] = train['D15'] / train.groupby(['card4'])['D15'].transform('std')

    test['D15_to_mean_card1'] = test['D15'] / test.groupby(['card1'])['D15'].transform('mean')
    test['D15_to_mean_card4'] = test['D15'] / test.groupby(['card4'])['D15'].transform('mean')
    test['D15_to_std_card1'] = test['D15'] / test.groupby(['card1'])['D15'].transform('std')
    test['D15_to_std_card4'] = test['D15'] / test.groupby(['card4'])['D15'].transform('std')

    train['D15_to_mean_addr1'] = train['D15'] / train.groupby(['addr1'])['D15'].transform('mean')
    train['D15_to_mean_addr2'] = train['D15'] / train.groupby(['addr2'])['D15'].transform('mean')
    train['D15_to_std_addr1'] = train['D15'] / train.groupby(['addr1'])['D15'].transform('std')
    train['D15_to_std_addr2'] = train['D15'] / train.groupby(['addr2'])['D15'].transform('std')

    test['D15_to_mean_addr1'] = test['D15'] / test.groupby(['addr1'])['D15'].transform('mean')
    test['D15_to_mean_addr2'] = test['D15'] / test.groupby(['addr2'])['D15'].transform('mean')
    test['D15_to_std_addr1'] = test['D15'] / test.groupby(['addr1'])['D15'].transform('std')
    test['D15_to_std_addr2'] = test['D15'] / test.groupby(['addr2'])['D15'].transform('std')

    train[['P_emaildomain_1', 'P_emaildomain_2', 'P_emaildomain_3']
          ] = train['P_emaildomain'].str.split('.', expand=True)
    train[['R_emaildomain_1', 'R_emaildomain_2', 'R_emaildomain_3']
          ] = train['R_emaildomain'].str.split('.', expand=True)
    test[['P_emaildomain_1', 'P_emaildomain_2', 'P_emaildomain_3']] = test['P_emaildomain'].str.split('.', expand=True)
    test[['R_emaildomain_1', 'R_emaildomain_2', 'R_emaildomain_3']] = test['R_emaildomain'].str.split('.', expand=True)

    # Prepare data for modelling
    many_null_cols = [col for col in train.columns if train[col].isnull().sum() / train.shape[0] > 0.9]
    many_null_cols_test = [col for col in test.columns if test[col].isnull().sum() / test.shape[0] > 0.9]

    big_top_value_cols = [col for col in train.columns if train[col].value_counts(
        dropna=False, normalize=True).values[0] > 0.9]
    big_top_value_cols_test = [col for col in test.columns if test[col].value_counts(
        dropna=False, normalize=True).values[0] > 0.9]

    cols_to_drop = list(set(many_null_cols + many_null_cols_test + big_top_value_cols
                            + big_top_value_cols_test + one_value_cols + one_value_cols_test))
    cols_to_drop.remove('isFraud')
    len(cols_to_drop)

    train = train.drop(cols_to_drop, axis=1)
    test = test.drop(cols_to_drop, axis=1)

    cat_cols = ['id_12', 'id_13', 'id_14', 'id_15', 'id_16', 'id_17', 'id_18', 'id_19', 'id_20', 'id_21', 'id_22', 'id_23', 'id_24', 'id_25', 'id_26', 'id_27', 'id_28', 'id_29',
                'id_30', 'id_31', 'id_32', 'id_33', 'id_34', 'id_35', 'id_36', 'id_37', 'id_38', 'DeviceType', 'DeviceInfo', 'ProductCD', 'card4', 'card6', 'M4', 'P_emaildomain',
                'R_emaildomain', 'card1', 'card2', 'card3',  'card5', 'addr1', 'addr2', 'M1', 'M2', 'M3', 'M5', 'M6', 'M7', 'M8', 'M9',
                'P_emaildomain_1', 'P_emaildomain_2', 'P_emaildomain_3', 'R_emaildomain_1', 'R_emaildomain_2', 'R_emaildomain_3']
    for col in cat_cols:
        if col in train.columns:
            le = LabelEncoder()
            le.fit(list(train[col].astype(str).values) + list(test[col].astype(str).values))
            train[col] = le.transform(list(train[col].astype(str).values))
            test[col] = le.transform(list(test[col].astype(str).values))

    X = train.sort_values('TransactionDT').drop(['isFraud', 'TransactionDT', 'TransactionID'], axis=1)
    y = train.sort_values('TransactionDT')['isFraud']
    # X_test = test.sort_values('TransactionDT').drop(['TransactionDT', 'TransactionID'], axis=1)
    X_test = test.drop(['TransactionDT', 'TransactionID'], axis=1)
    del train
    test = test[["TransactionDT", 'TransactionID']]

    # by https://www.kaggle.com/dimartinot
    def clean_inf_nan(df):
        return df.replace([np.inf, -np.inf], np.nan)

    # Cleaning infinite values to NaN
    X = clean_inf_nan(X)
    X_test = clean_inf_nan(X_test)

    return X, X_test

    gc.collect()
    '''


if __name__ == '__main__':
    run()
