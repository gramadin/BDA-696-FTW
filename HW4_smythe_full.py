"""
Created by Ed Smythe Oct 2020
BDA 696 @ SDSU
Given a pandas dataframe
    Contains both a response and predictors
Given a list of predictors and the response columns
    Determine if response is continuous or boolean (don't worry about >2 category responses)
    Loop through each predictor column
        Determine if the predictor cat/cont
        Automatically generate the necessary plot(s) to inspect it
        Calculate the different ranking algos
        p-value & t-score along with it's plot
        Regression: Continuous response
        Logistic Regression: Boolean response
        Difference with mean of response along with it's plot (weighted and unweighted)
        Random Forest Variable importance ranking
        Generate a table with all the variables and their rankings
I'm going to grade this by giving it some random dataset and seeing if it outputs everything
Desire: html or excel based rankings report with links to the plots

    Recommendations for plots
    Predictor / Response type Dependant
        Response: Boolean / Categorical
            Predictor: Boolean / Categorical
                Heatplot
            Predictor: Continous
                Violin plot on predictor grouped by response
                Distribution plot on predictor grouped by response
        Response: Continuous
            Predictor: Boolean / Categorical
                Violin plot on response grouped by predictor
                Distribution plot on response grouped by predictor
            Predictor: Continuous
                Scatter plot with trendline
"""

import sys

import numpy as np
import pandas as pd
import plotly.express as px
import pydot
import statsmodels.api as sm
import webbrowser

from datetime import datetime
from io import StringIO
from pandas import DataFrame
from plotly import express as px
from plotly import figure_factory as ff
from plotly import graph_objects as go
from sklearn import datasets
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.utils.multiclass import type_of_target as tot


# PLOT Functions
def plot_cont_cont(to_plot):
    # Scatter plot with trendline
    # from class notes Week6
    user_db = to_plot
    X = user_db.data
    y = user_db.target
    for idx, column in enumerate(X.T):
        feature_name = user_db.feature_names[idx]
        predictor = sm.add_constant(column)
        linear_regression_model = sm.OLS(y, predictor)
        linear_regression_model_fitted = linear_regression_model.fit()
        print(f"Variable: {feature_name}")
        print(linear_regression_model_fitted.summary())

        # Get the stats
        t_value = round(linear_regression_model_fitted.tvalues[1], 6)
        p_value = "{:.6e}".format(linear_regression_model_fitted.pvalues[1])

        # Plot the figure
        fig = px.scatter(x=column, y=y, trendline="ols")
        fig.update_layout(
            title=f"Variable: {feature_name}: (t-value={t_value}) (p-value={p_value})",
            xaxis_title=f"Variable: {feature_name}",
            yaxis_title="y",
        )
        fig.show()
        fig.write_html(file=f"./HW4_lin_plot{idx}.html", include_plotlyjs="cdn")
    return


def plot_cont_cat(to_plot):
    # Violin plot on predictor grouped by response 
    user_db = to_plot
    X = user_db.data
    y = user_db.target
    #
    for idx, column in enumerate(X.T):
        feature_name = user_db.feature_names[idx]
        predictor = sm.add_constant(column)
        #
        logistic_regression_model = LogisticRegression(
            random_state=4622).fit(predictor, y)
        print(f"Variable: {feature_name}")
        print(logistic_regression_model.score(predictor, y))
        # Get the score
        the_score = logistic_regression_model.score(predictor, y)
        # Plot the figure
        fig = px.violin(x=y, y=column, color=y)
        fig.update_layout(
            title=f"Variable:{feature_name},Logistic Regression Score={the_score}",
            xaxis_title=f"Variable: {feature_name}",
            yaxis_title="y",
        )
        fig.show()
        fig.write_html(file=f"./HW4_cont_cat_violin_plot.html", include_plotlyjs="cdn")
    return


def plot_cat_cat(to_plot):
    # haven't figured out how to implement a z in a Heatplot here, using violin
    user_db = to_plot
    X = user_db.data
    y = user_db.target
    #
    for idx, column in enumerate(X.T):
        feature_name = user_db.feature_names[idx]
        predictor = sm.add_constant(column)
        #
        logistic_regression_model = LogisticRegression(
            random_state=4622).fit(predictor, y)
        print(f"Variable: {feature_name}")
        print(logistic_regression_model.score(predictor, y))
        # Get the score
        the_score = logistic_regression_model.score(predictor, y)
        # Plot the Figure
        fig = px.violin(x=y, y=column)
        fig.update_layout(
            title=f"Variable:{feature_name},Logistic Regression Fit Score={the_score}",
            xaxis_title=f"Variable: {feature_name}",
            yaxis_title="y",
        )
        fig.show()
        fig.write_html(file=f"./HW4_cat_cat_violin_plot.html", include_plotlyjs="cdn")
    return


def plot_cat_cont(to_plot):
    # Violin plot on response grouped by predictor
    user_db = to_plot
    X = user_db.data
    y = user_db.target
    #
    for idx, column in enumerate(X.T):
        feature_name = user_db.feature_names[idx]
        predictor = sm.add_constant(column)
        #
        logistic_regression_model = LogisticRegression(
            random_state=4622).fit(predictor, y)
        print(f"Variable: {feature_name}")
        print(logistic_regression_model.score(predictor, y))
        # Get the score
        the_score = logistic_regression_model.score(predictor, y)
        # Plot the Figure
        fig = px.violin(x=column, y=y, color=column)
        fig.update_layout(
            title=f"Variable:{feature_name},Logistic Regression Fit Score={the_score}",
            xaxis_title=f"Variable: {feature_name}",
            yaxis_title="y",
        )
        fig.show()
        fig.write_html(file=f"./HW4_cat_con_violin_plot{idx}.html",
                       include_plotlyjs="cdn")
    return


# add boolean check incase type check is wrong
def col_is_bool(df, col):
    c = len(df[col].unique())
    if c == 2:
        True
    else:
        False
    return col


# predictor select for any dataset
def predictor_select(ds):
    predictors = ds.feature_names
    # index_list = [i+1 for i in range(len(predictors))]
    selection_df = pd.DataFrame(predictors, columns=["Predictor"])
    selection_df.index += 1
    print(selection_df)
    pred_choice = input("Which predictors will you use? (use index numbers separate by a comma) :")
    pred_choice = pred_choice.split(",")
    for i in range(0, len(pred_choice)):
        pred_choice[i] = int(pred_choice[i])
    feature_list = [selection_df.at[i, "Predictor"] for i in pred_choice]

    return feature_list


def print_heading(title):
    print("*" * 80)
    print(title)
    print("*" * 80)
    return


# Main functions
def main():
    #    start_t = datetime.now()
    # set built-in dataset choices
    ds1 = datasets.load_boston()
    ds2 = datasets.load_iris()
    ds3 = datasets.load_diabetes()
    ds4 = datasets.load_digits()
    ds5 = datasets.load_linnerud()
    ds6 = datasets.load_wine()
    ds7 = datasets.load_breast_cancer()

    # Get user inputs -- add error handeling
    # when response is continous then no 'target_names'
    # when response is catagorical set 'target_names'
    print(
        """ Select SKLearn dataset to use: ~default is 3~
                    1 - boston (response is continuous)
                    2 - iris (response is catagorical [3 cats])
                    3 - diabetes (response is continuous)
                    4 - digits (response is an array) Not working with this version
                    5 - linnerud (response is catagorical array of continuous)  [3 cats]) Not working with this version
                    6 - wine (response is catagorical [3 cast])
                    7 - breast cancer (response is catagorical {2cats/bool])
                    8 - user choice
                  """
    )

    choice = int(input("Which set? " or 3))

    if choice == 1:
        the_ds = ds1
    elif choice == 2:
        the_ds = ds2
    elif choice == 3:
        the_ds = ds3
    elif choice == 4:
        the_ds = ds4
    elif choice == 5:
        the_ds = ds5
    elif choice == 6:
        the_ds = ds6
    elif choice == 7:
        the_ds = ds7
    elif choice == 8:
        the_ds = input("direct path to dataset: ")
    elif choice == "":
        the_ds = ds3
    else:
        print(f"{choice} is an invalid entry. Please try again.")

    print(f"You chose {choice}")
    # turn source data into a pandas df
    working_df = pd.DataFrame(the_ds.data, columns=the_ds.feature_names)
    working_df["target"] = pd.Series(the_ds.target)  # chg
    working_df.head()

    # get column names

    col_list = working_df.columns.values.tolist()
    titles = [i.replace(')', "_").replace('(', "").replace(' ', '_') for i in col_list]
    working_df.columns = titles

    print_heading("Original Dataset")
    print(working_df)

    # ~RESPONSE~
    y = the_ds.target  # assign the response here #chg
    res_type = tot(the_ds.target)
    print_heading("Response type is " + res_type)

    # Group Predictor types
    type_mask = [tot(working_df[i]) for i in col_list]
    predictor_array = np.column_stack((col_list, type_mask))
    pred_df = pd.DataFrame(predictor_array, columns=["Predictor", "Type"])

    # ~PREDICTORS~
    # Allow user to select the desired features
    # feature_list = predictor_select(the_ds) #gettgin an exception with some DS

    cont_feature_df = pred_df[pred_df['Type'] == 'continuous']  # where tot continuous and bool_check false
    cat_feature_df = pred_df[pred_df['Type'] != 'continuous']  # where tot not contious or bool_check true
    if cat_feature_df.empty:
        print('No Catagorical!')
    if cont_feature_df.empty:
        print('No Continuous!')
    cont_feature_list = list(cont_feature_df['Predictor'])
    print('Continuous predictors ' + cont_feature_list)
    cat_feature_list = list(cat_feature_df['Predictor'])
    print('Catagorical predictors ' +cat_feature_list)

    # Generate Report DF
    report_time = datetime.now().isoformat()
    report_col = (
        "Catagory",
        "p-val_&_t-val",
        "Regression",
        "Logistic_Regression",
        "Difference_with_mean",
        "Random_Forest",
    )
    # report_df_cont = pd.DataFrame("", index=continuous_features, columns=report_col)
    # report_df_cat = pd.DataFrame("", index=catagorical_features, columns=report_col)

    # Save report to HTML
    report_df = working_df
    report_df.to_html("HW_report_" + datetime.now().strftime("%Y_%m_%d") + ".html")

if __name__ == "__main__":
    sys.exit(main())
