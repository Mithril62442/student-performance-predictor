import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, r2_score


# --------------------------------
# 1. Load dataset
# --------------------------------

df = pd.read_csv("data/student-mat.csv", sep=";")


# --------------------------------
# 2. Select our 16 features
# --------------------------------

features = [
    "traveltime",
    "studytime",
    "failures",
    "famsup",
    "paid",
    "activities",
    "nursery",
    "higher",
    "internet",
    "absences",
    "G1",
    "G2",
    "famrel",
    "freetime",
    "goout",
    "health"
]

X = df[features]
y = df["G3"]


# --------------------------------
# 3. Categorical features
# --------------------------------

categorical_features = [
    "famsup",
    "paid",
    "activities",
    "nursery",
    "higher",
    "internet"
]


# --------------------------------
# 4. Preprocessing
# --------------------------------

preprocessor = ColumnTransformer(
    transformers=[
        (
            "cat",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        )
    ],
    remainder="passthrough"
)


# --------------------------------
# 5. Create model
# --------------------------------

model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        (
            "regressor",
            RandomForestRegressor(
                n_estimators=200,
                max_depth=10,
                random_state=42
            )
        )
    ]
)


# --------------------------------
# 6. Split data
# --------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# --------------------------------
# 7. Train
# --------------------------------

model.fit(X_train, y_train)


# --------------------------------
# 8. Evaluate
# --------------------------------

predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("--------------------------------")
print("MODEL TRAINING COMPLETE")
print("--------------------------------")
print(f"MAE: {mae:.2f}")
print(f"R² Score: {r2:.2f}")


# --------------------------------
# 9. Save model
# --------------------------------

joblib.dump(
    model,
    "student_performance_model.pkl"
)

print("--------------------------------")
print("MODEL SAVED SUCCESSFULLY")
print("--------------------------------")