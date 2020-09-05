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
        Fit the transformed data against random forest classifier (try other classifiers)
        Wrap the steps into a pipeline
        Don't worry about train/test split. (Our model will be cheating)
    Special Notes
        Code should just work. Make sure to lint it! No Jupyter Notebooks!
        Work outside of your master branch and make a PR
        Buddy should review PR, after reviewed, send it to me
"""
# this script will work for any csv file that has 5 columns and is related data points gouped into 2:2:1 eg. IRIS data has 2 values for Sepal, 2 values for Petal and 1 value for class
#**** search 'chg' for locations to change names for your information ****#
import pandas as pd
import numpy as np
from sklearn import datasets
import plotly.graph_objects as go
import plotly.express as px
from ipywidgets import widgets
# define the columns of the data to be imported since we know the data does not have lables. Also allows for change to columns for differnet data via variable.
data_col = ['sepal length in cm','sepal width in cm','petal length in cm','petal width in cm','class'] #chg
# SKlearn has iris dataset included but for instructional pourposes we are gettgin the data set from a file.
filename = input("what is the filename? ")
file_data = pd.read_csv(filename, names=data_col)
# Example of DataFrame
file_data.head()
np.mean(file_data)
np.min(file_data)
np.max(file_data)
np.var(file_data)
# plotting
# overview plot
fig = px.scatter_matrix(file_data, dimensions=data_col, color=file_data.columns[4],width=1600, height=800)
fig.update_traces(diagonal_visible=True)
fig.update_layout(title_text='Iris Data')#chg
fig.show()
#Violin
var1 = file_data.columns[0]
var2 = file_data.columns[1]
fig2 = px.violin(file_data, y=file_data.columns[0], x=file_data.columns[1], color=file_data.columns[4],
                violinmode='overlay', hover_data=file_data.columns)
fig2.update_layout(title_text=f'{var1} vs. {var2}')
fig2.show()
var1 = file_data.columns[2]
var2 = file_data.columns[3]
fig3 = px.violin(file_data, y=file_data.columns[2], x=file_data.columns[3], color=file_data.columns[4],
                violinmode='overlay', hover_data=file_data.columns)
fig3.update_layout(title_text=f'{var1} vs. {var2}')
fig3.show()
#3D scatter with color
fig4 = px.scatter_3d(file_data, x=file_data.columns[0], y=file_data.columns[1], z=file_data.columns[2],
                    color=file_data.columns[3], symbol=file_data.columns[4],width=1600, height=800)
fig4.show()
#parallel cats
fig5 = px.parallel_categories(file_data)
fig5.show()
