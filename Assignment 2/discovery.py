import pandas as pd

df = pd.read_csv("data/data.csv", skipinitialspace=True)

df = df.replace("?", pd.NA).dropna()

print(df.head())
print(df.info())


import pandas as pd
from pycaret.classification import *

# Load
df = pd.read_csv("data/data.csv", skipinitialspace=True)

# Clean
df = df.replace("?", pd.NA).dropna()

# PyCaret
exp = setup(
    data=df,
    target="income",
    session_id=123
)

top3 = compare_models(n_select=3)
best_model = top3[0]

print("Top 3 models:")
for model in top3:
    print(model)

plot_model(best_model, plot="confusion_matrix", save=True)

save_model(best_model, "best_pipeline")


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv("data/data.csv")
df = df.replace("?", pd.NA)

X = df.drop("income", axis=1)
Y = df["income"]

categorical_cols = X.select_dtypes(include=["object"]).columns.tolist()
numeric_cols = X.select_dtypes(exclude=["object"]).columns.tolist()

numeric_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer(transformers=[
    ("num", numeric_transformer, numeric_cols),
    ("cat", categorical_transformer, categorical_cols)
])

model = RandomForestClassifier(random_state=123)

clf = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", model)
])

X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.2, random_state=123, stratify=Y
)

clf.fit(X_train, Y_train)
Y_pred = clf.predict(X_test)

print(classification_report(Y_test, Y_pred))




"""
I compared a low code machine learning workflow using PyCaret with a manual workflow using scikit-learn.
PyCaret ended up being the more efficient model because it automates prepocessing, model selection and evaluation. 
The PyCaret model only uses a few lines of code whereas the Scikit used more lines of code just for PyCaret to be
more efficient. Scikit requires more lines of code because you need to manually split the data, handle preprocessing
and then build the pipeline step by step.

Even though they produce similar results, they may have some slight differences because PyCaret automatically
handles preprocessing, cross-validation, etc. And of course variations in how data is split and different random seeds can impact results. 

Overall PyCaret is the better model, its faster and more convienient because it automates so much. Scikit provides more control
over each step, but also requires more work to get to the same results as PyCaret.  


"""