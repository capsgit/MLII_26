
from sklearn.datasets import load_breast_cancer
from sklearn.metrics import classification_report
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, MinMaxScaler

TEST_RATIO = 0.2 # 20% test vs 80% train
K = 3

data = load_breast_cancer()

X, y = data.data, data.target
# print("Shapes: ", "X\n", X.shape, "y \n", y.shape)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=TEST_RATIO,
    random_state=42,
    stratify=y,  # proportionale Klassenverteilung bleibt erhalten
)

model = Pipeline([("knn", KNeighborsClassifier(n_neighbors=K))])

# wir testen in jedem von den c Läufen 80% der X_train-Daten und 20% der X_train
# Daten. Model wurde intern 5 mal trainiert und wir können am Score sehen
score = cross_val_score(model, X_train, y_train, cv=5
                        #, scoring="f1"
                        )
# k scores [0.96703297 0.93406593 0.91208791 0.92307692 0.94505495]
print("\n Score:", score)
print("\n Durschnittsscore:", score.mean())  # mittelwert der scores

# model fitten und predicten
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print("\n CLASI_01 -> \n", classification_report(y_test, y_pred))


##################
data = load_breast_cancer()
X, y = data.data, data.target
print("\n names", data.target_names)
#####################


##########################################################
############  GRID SEARCH ###############################
##########################################################
param_grid = {"knn__n_neighbors": [1, 2, 7, 9]}
gs = GridSearchCV(model, param_grid, cv=5, scoring="accuracy")

gs.fit(X_train, y_train)

y_pred_gs = gs.predict(X_test)
print("\n CLASI_02 ->: \n", classification_report(y_test, y_pred_gs))
print("\n BEST params : \n", gs.best_params_)
print("\n BEST score : \n",gs.best_score_)


##########################################################
############  MIN / MAX SKYLER ##########################
##########################################################

# nueva pipeline con "minmax"
pipeline_scaler = Pipeline([("minmax", MinMaxScaler()), ("knn", KNeighborsClassifier(n_neighbors=K))])

# nueva param grid
param_grid_scaler = {"knn__n_neighbors": [1, 2, 7, 9], "knn__weights": ["uniform", "distance"]}
model_scaler = GridSearchCV(pipeline_scaler, param_grid_scaler, cv=5
                            #, scoring="accuracy"
                            )

# fit
model_scaler.fit(X_train, y_train)

# predict
y_pred_scaler = model_scaler.predict(X_test)
print("\n CLASI_03 ->: \n", classification_report(y_test, y_pred_scaler))


##########################################################
############  Standart SKYLER ##########################
##########################################################
