# modules/tuner.py
import optuna
import xgboost as xgb
from sklearn.metrics import accuracy_score

def objective(trial, X_train, y_train, X_test, y_test):
    param = {
        'verbosity': 0,
        'objective': 'binary:logistic',
        'n_estimators': 1000,
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.1, log=True),
        'max_depth': trial.suggest_int('max_depth', 3, 10),
        'subsample': trial.suggest_float('subsample', 0.5, 1.0),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.5, 1.0),
        'reg_alpha': trial.suggest_float('reg_alpha', 1e-3, 10.0, log=True),
        'reg_lambda': trial.suggest_float('reg_lambda', 1e-3, 10.0, log=True)
    }
    
    model = xgb.XGBClassifier(**param, n_jobs=-1)
    model.fit(X_train, y_train, eval_set=[(X_test, y_test)], early_stopping_rounds=50, verbose=False)
    
    preds = model.predict(X_test)
    return accuracy_score(y_test, preds)

def tune_xgboost(X_train, y_train, X_test, y_test):
    study = optuna.create_study(direction='maximize')
    study.optimize(lambda trial: objective(trial, X_train, y_train, X_test, y_test), n_trials=50)
    return study.best_params
