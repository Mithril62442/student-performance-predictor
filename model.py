import pandas as pd

data = pd.read_csv("data/student-mat.csv", sep=";")

print(data.head())
print(data.shape)
print(data.columns)

X = data.drop("G3", axis=1)
y = data["G3"]

print(X.shape)
print(y.shape)

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(X_train.shape)
print(X_test.shape)

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

categorical_columns = X.select_dtypes(include=["object"]).columns

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_columns)
    ],
    remainder="passthrough"
)

from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline

model = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", LinearRegression())
])

model.fit(X_train, y_train)

print("Model trained successfully!")

y_pred = model.predict(X_test)

print(y_pred[:5])

from sklearn.metrics import mean_absolute_error

mae = mean_absolute_error(y_test, y_pred)

print("Mean Absolute Error:", mae)

baseline_prediction = y_train.mean()

baseline_mae = mean_absolute_error(
    y_test,
    [baseline_prediction] * len(y_test)
)

print("Baseline MAE:", baseline_mae)

from sklearn.metrics import r2_score

r2 = r2_score(y_test, y_pred)

print("R² Score:", r2)

from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

rf_model = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", rf)
])

rf_model.fit(X_train, y_train)
rf_pred = rf_model.predict(X_test)

rf_mae = mean_absolute_error(y_test, rf_pred)

print("Random Forest MAE:", rf_mae)

rf_r2 = r2_score(y_test, rf_pred)

print("Random Forest R²:", rf_r2)

rf_train_pred = rf_model.predict(X_train)

rf_train_mae = mean_absolute_error(y_train, rf_train_pred)

print("Random Forest Training MAE:", rf_train_mae)
from sklearn.model_selection import GridSearchCV
param_grid = {
    "regressor__n_estimators": [100, 200, 300],
    "regressor__max_depth": [None, 5, 10, 15]
}
grid_search = GridSearchCV(
    rf_model,
    param_grid,
    cv=5,
    scoring="neg_mean_absolute_error",
    n_jobs=1
)
grid_search.fit(X_train, y_train)
print("Best Parameters:", grid_search.best_params_)
best_model = grid_search.best_estimator_
best_pred = best_model.predict(X_test)
best_mae = mean_absolute_error(y_test, best_pred)

print("Tuned Random Forest MAE:", best_mae)
import joblib

joblib.dump(best_model, "student_performance_model.pkl")

print("Model saved successfully!")