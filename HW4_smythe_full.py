"""
Created by Ed Smythe Oct 2020
BDA 696 @ SDSU
Given a pandas dataframe
    Contains both a response and predictors
Given a list of predictors and the response columns
    Determine if response is continuous or boolean
    (don't worry about >2 category responses)
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
I'm going to grade this by giving it some random dataset
and seeing if it outputs everything
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
from datetime import datetime

import numpy as np
import pandas as pd
import plotly.express as px
import statsmodels.api as sm
from sklearn import datasets
from sklearn.linear_model import LogisticRegression
from sklearn.utils.multiclass import type_of_target as tot


# PLOT Functions
def plot_cont_cont(to_plot):
    # Scatter plot with trendline
    # from class notes Week6
    user_db = to_plot
    X = user_db.data
    y = user_db.target
    con_con_file_list = []
    for idx, column in enumerate(X.T):
        feature_name = user_db.feature_names[idx]
        feature_name = feature_name.replace("/", "-")
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
        file_name = f"./HW4_{feature_name}_lin_plot.html"
        fig.write_html(file=file_name, include_plotlyjs="cdn")
        con_con_file_list += [file_name]
    return con_con_file_list


def plot_cont_cat(to_plot):
    # Violin plot on predictor grouped by response
    user_db = to_plot
    X = user_db.data
    y = user_db.target
    con_cat_file_list = []
    #
    for idx, column in enumerate(X.T):
        feature_name = user_db.feature_names[idx]
        feature_name = feature_name.replace("/", "-")
        predictor = sm.add_constant(column)
        #
        logistic_regression_model = LogisticRegression(random_state=4622).fit(
            predictor, y
        )
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
        file_name = f"./HW4_{feature_name}_cont_cat_violin_plot.html"
        fig.write_html(file=file_name, include_plotlyjs="cdn")
        con_cat_file_list += [file_name]
    return con_cat_file_list


def plot_cat_cat(to_plot):
    # haven't figured out how to implement a z in a Heatplot here, using violin
    user_db = to_plot
    X = user_db.data
    y = user_db.target
    cat_cat_file_list = []
    #
    for idx, column in enumerate(X.T):
        feature_name = user_db.feature_names[idx]
        feature_name = feature_name.replace("/", "-")
        predictor = sm.add_constant(column)
        #
        logistic_regression_model = LogisticRegression(random_state=4622).fit(
            predictor, y
        )
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
        file_name = f"./HW4_{feature_name}_cat_cat_violin_plot.html"
        fig.write_html(file=file_name, include_plotlyjs="cdn")
        cat_cat_file_list += [f'<a href="file:///{file_name}">link</a>']
    return cat_cat_file_list


def plot_cat_cont(to_plot):
    # Violin plot on response grouped by predictor
    user_db = to_plot
    X = user_db.data
    y = user_db.target
    cat_con_file_list = []
    #
    for idx, column in enumerate(X.T):
        feature_name = user_db.feature_names[idx]
        feature_name = feature_name.replace("/", "-")
        predictor = sm.add_constant(column)
        #
        logistic_regression_model = LogisticRegression(random_state=4622).fit(
            predictor, y
        )
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
        file_name = f"./HW4_{feature_name}_cat_con_violin_plot{idx}.html"
        fig.write_html(file=file_name, include_plotlyjs="cdn")
        cat_con_file_list += [file_name]
    return cat_con_file_list


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
    pred_choice = input(
        "Which predictors will you use? (use index numbers separate by a comma) :"
    )
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


def list_to_df(from_df, to_df, col):
    temp_list = from_df[col].to_list()
    to_df[col] = pd.Series(temp_list, index=to_df.index)


# Main functions
def main():
    start_t = datetime.now()
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
                    4 - digits (response is an array)
                    5 - linnerud (response is catagorical array of continuous)[3 cats])
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
    titles = [i.replace(")", "_").replace("(", "").replace(" ", "_") for i in col_list]
    working_df.columns = titles
    print_heading("Original Dataset")
    print(working_df)

    # ~RESPONSE~
    # y = the_ds.target  # assign the response here #chg
    res_type = tot(the_ds.target)
    print_heading("Response type is " + res_type)

    # Group Predictor types
    type_mask = [tot(working_df[i]) for i in col_list]
    predictor_array = np.column_stack((col_list, type_mask))
    pred_df = pd.DataFrame(predictor_array, columns=["Predictor", "Category"])

    # ~PREDICTORS~
    # Allow user to select the desired features
    # feature_list = predictor_select(the_ds)
    # enable abovce line to select only specific features to evaluate

    cont_feature_df = pred_df[
        pred_df["Category"] == "continuous"
    ]  # where tot continuous and bool_check false
    try:
        cont_feature_df = cont_feature_df.drop("target", axis=1, inplace=True)
    except Exception:
        pass

    cat_feature_df = pred_df[
        pred_df["Category"] != "continuous"
    ]  # where tot not continuous or bool_check true
    try:
        cat_feature_df = cat_feature_df.drop("target", axis=1, inplace=True)
    except Exception:
        pass

    print("No Continuous!") if cont_feature_df.empty else print(cont_feature_df)
    print("No Categorical!") if cat_feature_df.empty else print(cat_feature_df)

    # cont_feature_list = list(cont_feature_df["Predictor"])
    # cat_feature_list = list(cat_feature_df["Predictor"])

    # Make plots
    # if res_type == "continuous":
    cat_con_file_list = plot_cat_cont(the_ds)
    con_con_file_list = plot_cont_cont(the_ds)

    # else:
    con_cat_file_list = plot_cont_cat(the_ds)
    cat_cat_file_list = plot_cat_cat(the_ds)

    # Generate Report DF
    report_col = (
        "Category",
        "p-val_&_t-val",
        "Regression",
        "Logistic_Regression",
        "Difference_with_mean",
        "Random_Forest",
    )
    report_df = pd.DataFrame("", index=col_list, columns=report_col)
    report_df = report_df.drop(["target"])
    pred_df = pred_df.set_index(["Predictor"])
    pred_df = pred_df.drop(["target"])

    # Update Report with data
    report_df.index.name = "Predictor"
    pred_df.index = report_df.index

    # add plots to report
    list_to_df(pred_df, report_df, "Category")
    temp_df = pd.DataFrame(cat_con_file_list, columns=["Logistic_Regression"])
    list_to_df(temp_df, report_df, "Logistic_Regression")
    temp_df = pd.DataFrame(con_con_file_list, columns=["Regression"])
    list_to_df(temp_df, report_df, "Regression")
    temp_df = pd.DataFrame(con_cat_file_list, columns=["Random_Forest"])
    list_to_df(temp_df, report_df, "Random_Forest")
    temp_df = pd.DataFrame(cat_cat_file_list, columns=["Difference_with_mean"])
    list_to_df(temp_df, report_df, "Difference_with_mean")

    # Save report to HTML
    report_df.to_html(
        "HW_report_" + datetime.now().strftime("%Y_%m_%d-%H_%M") + ".html"
    )
    print(datetime.now() - start_t)
    return


if __name__ == "__main__":
    sys.exit(main())
