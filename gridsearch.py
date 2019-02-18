#CODE FROM:
#https://machinelearningmastery.com/how-to-grid-search-sarima-model-hyperparameters-for-time-series-forecasting-in-python/

# grid search sarima hyperparameters
import sys
from math import sqrt
from multiprocessing import cpu_count
from joblib import Parallel
from joblib import delayed
from warnings import catch_warnings
from warnings import filterwarnings
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error
from pandas import read_csv

# one-step sarima forecast
def sarima_forecast(history, config):
	order, sorder, trend = config
	# define model
	model = SARIMAX(history, order=order, seasonal_order=sorder, trend=trend, enforce_stationarity=False, enforce_invertibility=False)
	# fit model
	model_fit = model.fit(disp=False)
	# make one step forecast
	yhat = model_fit.predict(len(history), len(history))
	return yhat[0]

# root mean squared error or rmse
def measure_rmse(actual, predicted):
	return sqrt(mean_squared_error(actual, predicted))

# split a univariate dataset into train/test sets
def train_test_split(data, n_test):
	return data[:-n_test], data[-n_test:]

# walk-forward validation for univariate data
def walk_forward_validation(data, n_test, cfg):
	predictions = list()
	# split dataset
	train, test = train_test_split(data, n_test)
	# seed history with training dataset
	history = [x for x in train]
	# step over each time-step in the test set
	for i in range(len(test)):
		# fit model and make forecast for history
		yhat = sarima_forecast(history, cfg)
		# store forecast in list of predictions
		predictions.append(yhat)
		# add actual observation to history for the next loop
		history.append(test[i])
	# estimate prediction error
	error = measure_rmse(test, predictions)
	return error

# score a model, return None on failure
def score_model(data, n_test, cfg, debug=False):
	result = None
	# convert config to a key
	key = str(cfg)
	# show all warnings and fail on exception if debugging
	if debug:
		result = walk_forward_validation(data, n_test, cfg)
	else:
		# one failure during model validation suggests an unstable config
		try:
			# never show warnings when grid searching, too noisy
			with catch_warnings():
				filterwarnings("ignore")
				result = walk_forward_validation(data, n_test, cfg)
		except:
			error = None
	# check for an interesting result
	if result is not None:
		print(' > Model[%s] %.3f' % (key, result))
	return (key, result)

# grid search configs
def grid_search(data, cfg_list, n_test, parallel=True):
	scores = None
	if parallel:
		# execute configs in parallel
    #n_jobs=cpu_count() will lag your computer
		executor = Parallel(n_jobs=4, backend='multiprocessing')
		tasks = (delayed(score_model)(data, n_test, cfg) for cfg in cfg_list)
		scores = executor(tasks)
	else:
		scores = [score_model(data, n_test, cfg) for cfg in cfg_list]
	# remove empty results
	scores = [r for r in scores if r[1] != None]
	# sort configs by error, asc
	scores.sort(key=lambda tup: tup[1])
	return scores

# create a set of sarima configs to try
def sarima_configs(seasonal=[0], trend=['n','c','t','ct'],p_params = [0, 1, 2],q_params = [0, 1, 2],
                  P_params = [0, 1, 2], Q_params = [0, 1, 2]):
	models = list()
	# define config lists
	p_params = p_params
	d_params = [0, 1]
	q_params = q_params
	t_params = trend
	P_params = P_params
	D_params = [0, 1]
	Q_params = Q_params
	m_params = seasonal
	# create config instances
	for p in p_params:
		for d in d_params:
			for q in q_params:
				for t in t_params:
					for P in P_params:
						for D in D_params:
							for Q in Q_params:
								for m in m_params:
									cfg = [(p,d,q), (P,D,Q,m), t]
									models.append(cfg)
	return models

if __name__ == '__main__':

  n_test = 12*6

  filename = sys.argv[1] 
  
  if filename == 'anomalyrange.csv':
    
    data = read_csv('gridsearch_data/anomalyrange.csv').anomaly.values

    cfg_list = sarima_configs(seasonal=[0], trend=['c'], p_params = [0, 1, 2],q_params = [0, 1, 2],
                              P_params = [0, 1, 2], Q_params = [0, 1, 2])

    scores = grid_search(data, cfg_list, n_test)

    print(scores)

    print('Best for co2range')

    for cfg, error in scores[:3]:
	    print(cfg, error)

  elif filename == 'co2range.csv':

    data = read_csv('gridsearch_data/co2range.csv').CO2filled.values

    cfg_list = sarima_configs(seasonal=[12], trend=['ct'], p_params = [0, 1, 2],q_params = [0, 1, 2],
                              P_params = [0, 1, 2], Q_params = [0, 1, 2])

    scores = grid_search(data, cfg_list, n_test)

    print(scores)

    print('Best for co2range')

    for cfg, error in scores[:3]:
	    print(cfg, error)
  
  elif filename == 'ensorange.csv':

    data = read_csv('gridsearch_data/ensorange.csv').ANOM.values

    cfg_list = sarima_configs(seasonal=[0], trend=['n'], p_params = [0, 1, 2],q_params = [0, 1, 2])

    scores = grid_search(data, cfg_list, n_test)

    print(scores)

    print('Best for ensorange')

    for cfg, error in scores[:3]:
	    print(cfg, error)
  
  elif filename == 'spotsrange.csv':

    data = read_csv('gridsearch_data/spotsrange.csv').SNvalue.values

    cfg_list = sarima_configs(seasonal=[0], trend=['n'], p_params = [0, 1, 2],q_params = [0, 1, 2])

    scores = grid_search(data, cfg_list, n_test)

    print(scores)

    print('Best for spotsrange')

    for cfg, error in scores[:3]:
	    print(cfg, error)

  else:
    print("No file found")

