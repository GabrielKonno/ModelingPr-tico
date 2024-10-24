# -*- coding: utf-8 -*-
"""Modeling Prática

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1uAf9SbA4BMeQos-XM1-3K6oQemUNyWaD
"""

from sklearn import datasets
import pandas as pd

housing = datasets.fetch_california_housing() #importando dataset

print(housing)

df = pd.DataFrame(housing.data, columns=housing.feature_names) #Transformando em DF

housing.keys() #Vendo as keys

print(housing.DESCR)

df.head()

print(housing.target)

df['MedValue'] = housing.target

df.head()

x = housing.data # Características Casas
y = housing.target # Preço das Casas

"""# Modeling Techniques
1. Regressão Linear SKlearn <https://scikit-learn.org/dev/modules/generated/sklearn.linear_model.LinearRegression.html#sklearn.linear_model.LinearRegression>

2. SVR <https://scikit-learn.org/dev/modules/generated/sklearn.svm.SVR.html#sklearn.svm.SVR>

3. Decision Tree Regression - XGBoost <https://xgboost.readthedocs.io/en/stable/tutorials/index.html>


## Modeling Assumptions:

Apenas variáveis numéricas

## Métricas de Avaliação do Modelo:
### Para penalizar erros grandes:
1. MSE
2. RMSE
<https://scikit-learn.org/dev/api/sklearn.metrics.html>

# Teste Design
## Dataset split:

Separação Train-Test de 20% para teste por método SKlearn
"""

# Técnica 1. Regressão Linear

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
import numpy as np

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

regLin = LinearRegression()

regLin = regLin.fit(x_train, y_train)

yPredLin = regLin.predict(x_test)

MSE = mean_squared_error(y_test, yPredLin)
RMSE = np.sqrt(MSE)

print("LINEAR MSE:", MSE)
print("LINEAR RMSE:", RMSE)

# Técnica 2. SVR

from sklearn.svm import SVR

regSVR = SVR().fit(x_train, y_train)

yPredSVR = regSVR.predict(x_test)

MSESVR = mean_squared_error(y_test, yPredSVR)
RMSESVR = np.sqrt(MSESVR)

print("SVR MSESVR:", MSESVR)
print("SVR RMSE:", RMSESVR)

# Técnica 3. Decision Tree Regression (XGBoost)

from xgboost import XGBRegressor

regXGB = XGBRegressor().fit(x_train, y_train)

yPredXGB = regXGB.predict(x_test)

MSEXGB = mean_squared_error(y_test, yPredXGB)
RMSEXGB = np.sqrt(MSEXGB)

print("XGB MSE:", MSEXGB)
print("XGB RMSE:", RMSEXGB)

"""# Interpretando os resultados:

1. Modelo Linear (Regressão Linear):
MSE: 0.5559
RMSE: 0.7456
A regressão linear tem um MSE de 0.5559, o que indica que o modelo está errando, em média, aproximadamente $74.560 (SQR(0.5559) × 100.000) ao prever os valores das casas. Esse erro não é insignificante, mas pode ser aceitável dependendo do contexto do mercado de imóveis e dos valores em questão.

2. Modelo SVR (Support Vector Regressor):
MSE: 1.3320
RMSE: 1.1541
O modelo SVR apresentou um MSE de 1.3320, indicando um desempenho significativamente pior em relação ao modelo linear. O RMSE de 1.1541 mostra que o erro médio nas previsões é de $115.410 (SQR(1.3320)×100.000), o que pode ser considerado um erro muito alto para o seu objetivo. O SVR claramente não se ajustou bem aos dados, sugerindo que ele não é a melhor escolha para esse problema em específico.

3. Modelo XGBoost (Árvore de Decisão de Regressão):
MSE: 0.2226
RMSE: 0.4718
O XGBoost foi o que teve o melhor desempenho entre os três modelos, com um MSE de 0.2226 e um RMSE de 0.4718. Isso indica que, em média, o erro nas previsões é de $47.180 (0.2226×100.000), um valor consideravelmente menor em comparação aos outros modelos. Este é o modelo mais preciso e ajustado aos dados, de acordo com essa métrica.

##Conclusão e Comparação:

### XGBoost:
Este modelo apresentou o menor MSE e RMSE, o que sugere que ele oferece as previsões mais precisas entre os três. O erro médio de $47.180 é substancialmente menor do que os erros nos outros dois modelos.

### Regressão Linear:
Embora o modelo linear tenha apresentado resultados razoáveis, com um erro médio de $74.560, ele ainda é inferior ao XGBoost. Pode ser uma opção viável se você busca simplicidade no modelo, mas não oferece a mesma precisão.

### SVR:
O SVR teve um desempenho consideravelmente pior, com um erro médio de $115.410. Este modelo parece inadequado para esse problema, pelo menos com os parâmetros testados.

#Otimização de Hiperparâmetros

Utilizando GridSearchCV do SKlearn

<https://scikit-learn.org/dev/modules/generated/sklearn.model_selection.GridSearchCV.html#sklearn.model_selection.GridSearchCV>
"""

from sklearn.model_selection import GridSearchCV

regXGB.get_params().keys()

params = {
    'max_depth':[5, 6, 7],
    'learning_rate': [0.1, 0.2, 0.3],
    'objective' : ['reg:squarederror'],
    'booster' : ['gbtree'],
    'n_jobs' : [5],
    'gamma' : [0, 1],
    'min_child_weight' : [1, 3],
    'max_delta_step' : [0, 1],
    'subsample' : [0.5, 1]
}

xgbGrid = GridSearchCV(XGBRegressor(), params, refit = 'neg_mean_square_error', verbose = True) # Verbose narra o que tá acontecendo

xgbGridModel = xgbGrid.fit(x_train, y_train)

xgbGridModel.best_params_ # best_params_ lista a melhor combinação de parâmetros

yGrid = xgbGridModel.predict(x_test)

MSEGrid = mean_squared_error(y_test, yGrid)
RMSEGrid = np.sqrt(MSEGrid)

print("XGB Grid MSE:", MSEGrid)
print("XGB Grid RMSE:", RMSEGrid)

"""# Conclusão

Temos, ao fim, o MSE e RMSE com os melhores parâmetros encontrados pelo GridSearch entre as variações dadas.

"""

