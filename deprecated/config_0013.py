config = {
    'features': ['magic'],

    'model': {
        # https://lightgbm.readthedocs.io/en/latest/Parameters.html
        'type': 'lgb',
        'params': {'boosting_type': 'gbdt',
                   'num_leaves': 491,
                   'max_depth': -1,
                   'learning_rate': 0.006883242363721497,
                   'objective': 'binary',
                   'min_child_weight': 0.03454472573214212,
                   'reg_alpha': 0.3899927210061127,
                   'reg_lambda': 0.6485237330340494,
                   'random_state': 47,
                   'feature_fraction': 0.3797454081646243,
                   'bagging_fraction': 0.4181193142567742,
                   'min_data_in_leaf': 106,
                   'bagging_seed': 11,
                   'metric': 'auc',
                   'verbosity': -1,
                   'max_bin': 255,
                   }
        },

    'train': {
        'n_splits': 5,
        'num_boost_round': 5000,
        'early_stopping_rounds': 100
        }
}
