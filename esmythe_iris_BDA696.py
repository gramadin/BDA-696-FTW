"""
Created by Ed Smythe Sept 2020
BDA 696 @ SDSU
Homework - Assignment 1 - Due Sept 8
    Classic Fisher's Iris dataset (source)
        Data, Description
    Load the above data into a Pandas DataFrame
    Get some simple summary statistics (mean, min, max, quartiles) using numpy
    Plot the different classes against one another (try 5 different plots)
        Scatter, Violin, ...
        Try to see visual differences between them
    Analyze and build models - Use scikit-learn
        Use the normalizer transformer
        Fit the transformed data against random forest classifier
        (try other classifiers)
        Wrap the steps into a pipeline
        Don't worry about train/test split. (Our model will be cheating)
    Special Notes
        Code should just work. Make sure to lint it! No Jupyter Notebooks!
        Work outside of your master branch and make a PR
        Buddy should review PR, after reviewed, send it to me
"""
# script works for any "csv" that: 
# has 5 columns related data points gouped into 2:2:1
# eg. IRIS data has 2 Sepal, 2 Petal and 1 class

#**** search 'chg' for locations to change names for your information ****#

import importlib
import numpy as np
import pandas as pd
import pip
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

# Libraries needed
modules = ["pandas", "numpy", "plotly", "sklearn"]
# taken from https://bit.ly/3bCtuhO

for modname in modules:
    try:
        # try to import the module normally and put it in globals
        globals()[modname] = importlib.import_module(modname)
    except ImportError as e:
        result = pip.main(["install", modname])
        if result != 0:  # if pip could not install it reraise the error
            raise
        else:
            # if the install was sucessful, put modname in globals
            globals()[modname] = importlib.import_module(modname)
#
def main():
# define columns of data to be imported since we know the data does not have lables.
# Also allows for change to columns for differnet data via variable.
    data_col = [
    "sepal length in cm",
    "sepal width in cm",
    "petal length in cm",
    "petal width in cm",
    "class",
    ] #chg
# SKlearn has iris dataset included but for instructional pourposes we use file.
    filename = input("what is the filename? [default:iris.data]") or "iris.data"
    file_data = pd.read_csv(filename, names=data_col)
# Example of DataFrame
    print("Sample:\n***************")
    print(file_data.head())
# Simple stats
    print("\nMean:\n***************")
    print(np.mean(file_data))
    print("\nMin:\n***************")
    print(np.min(file_data))
    print("\nMax:\n***************")
    print(np.max(file_data))
    print("\nVariance:\n***************")
    print(np.var(file_data))
# Plotting
# overview plot
    fig = px.scatter_matrix(
        file_data, dimensions=data_col, color=file_data.columns[4], width=1600, height=800
    )

    fig.update_traces(diagonal_visible=True)

    fig.update_layout(title_text="Iris Data")  # chg

    fig.show()

#Violin
    var1 = file_data.columns[0]
    var2 = file_data.columns[1]

    fig2 = px.violin(
        file_data,
        y=file_data.columns[0],
        x=file_data.columns[1],
        color=file_data.columns[4],
        violinmode="overlay",
        hover_data=file_data.columns,
    )
    fig2.update_layout(title_text=f"{var1} vs. {var2}")
    fig2.show()

    var1 = file_data.columns[2]
    var2 = file_data.columns[3]
    fig3 = px.violin(
        file_data,
        y=file_data.columns[2],
        x=file_data.columns[3],
        color=file_data.columns[4],
        violinmode="overlay",
        hover_data=file_data.columns,
    )
    fig3.update_layout(title_text=f"{var1} vs. {var2}")
    fig3.show()

#3D scatter with color
    fig4 = px.scatter_3d(
        file_data,
        x=file_data.columns[0],
        y=file_data.columns[1],
        z=file_data.columns[2],
        color=file_data.columns[3],
        symbol=file_data.columns[4],
        width=1600,
        height=1000,
    )
    fig4.show()
# parallel cats
    fig5 = px.parallel_categories(file_data)
    fig5.show()

# Normalizer
    Col1=file_data.columns[0]
    Col2=file_data.columns[1]
    Col3=file_data.columns[2]
    Col4=file_data.columns[3]
    Col5=file_data.columns[4]

    x_orig = file_data[[Col1,Col2,Col3,Col4]].values
#x_orig
    y = file_data[Col5].values
    one_hot_encoder= OneHotEncoder()
    one_hot_encoder.fit(x_orig)
    X = one_hot_encoder.transform(x_orig)

# Random Forest
    random_forest = RandomForestClassifier(random_state=1234)
    random_forest.fit(X,y)
    test_df = file_data[[Col1,Col2,Col3,Col4]]

    print(test_df)
 
    X_test_orig = test_df.values
    X_test = one_hot_encoder.transform(X_test_orig)
    prediction = random_forest.predict(X_test)
    probability = random_forest.predict_proba(X_test)

    print(f"Classes: {random_forest.classes_}")
    print(f"Probability: {probability}")
    print(f"Predictions: {prediction}")

# Pipeline for above
    pipeline = Pipeline(
        [
            ("OneHotEncode", OneHotEncoder()),
            ("RandomForest", RandomForestClassifier(random_state=1234)),
        ]
    )
    pipeline.fit(x_orig, y)

    probability = pipeline.predict_proba(X_test_orig)
    prediction = pipeline.predict(X_test_orig)
    print(f"Probability: {probability}")
    print(f"Predictions: {prediction}")
main()
