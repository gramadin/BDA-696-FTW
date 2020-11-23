"""
Created by Ed Smythe Oct 2020
BDA 696 @ SDSU
Given a pandas dataframe
    Contains both a response and predictors
    Assume you could have either a boolean or continuous response
Split dataset predictors between categoricals and continuous
    Assume only nominal categoricals (no ordinals)
Calculate correlation metrics between all
    Continuous / Continuous pairs
    Continuous / Categorical pairs
    Categorical / Categorical pairs
Put values in tables ordered DESC by correlation metric
Put links to the original variable plots done in HW #4
Generate correlation matricies for the above 3
Calculate "Brute-Force" variable combinations between all
    Continuous / Continuous pairs
    Continuous / Categorical pairs
    Categorical / Categorical pairs
Calculate weighted and unweighted "difference with mean of response" metric
Put values in tables ordered DESC by the "weighted" ranking metric
For each of the combinations generate the necessary plots to help see the relationships
"Link" to these plots from the table (html, excel)
Final output
    3 Correlation tables
        With links to individual plots done in HW#4
    3 Correlation Matricies
    3 "Brute Force" tables, with links to plots showing combined relationship
I'm going to grade this by giving it some random dataset and seeing if it outputs everything
Due October 23rd
"""

import sys
import os
from datetime import datetime

import numpy as np
import pandas as pd
import plotly.express as px
import statsmodels.api as sm
import ipywidgets as widgets
import plotly.graph_objs as go
from scipy import stats
from sklearn import datasets
from sklearn.linear_model import LogisticRegression
from sklearn.utils.multiclass import type_of_target as tot


# PLOT Functions
def adj_plot_hist (pred, initial_bin_width=3): # missing the mean simple line plot
    pop_mean = [pred.mean()] * len(pred)
    figure_widget = go.FigureWidget(
        data=[go.Histogram(x=pred, xbins={"size": initial_bin_width},
                           name='Bin'),
              go.Scatter(x=pred[0:], y=pop_mean,
                         mode='lines',
                         name='Predictor Mean')]
    )

    bin_slider = widgets.FloatSlider(
        value=initial_bin_width,
        min=0,
        max=pred.max(),
        step=pred.max() / 20,
        description="Bin width:",
        readout_format=".1f",  # display as integer
    )

    histogram_object = figure_widget.data[0]

    def set_bin_size(change):
        histogram_object.xbins = {"size": change["new"]}

    bin_slider.observe(set_bin_size, names="value")

    output_widget = widgets.VBox([figure_widget, bin_slider])
    return output_widget

def plot_hist (pred): # missing the mean simple line plot
    pop_mean = [pred.mean()] * len(pred)
    data=[go.Histogram(x=pred, xbins={"size": len(pred.unique())/20},
                       name='Bin'),
          go.Scatter(x=pred[0:], y=pop_mean,
                     mode='lines',
                     name='Predictor Mean')]
    return

def plot_cont_cont(to_plot):
    # Scatter plot with trendline
    # from class notes Week6
    user_db = to_plot
    X = user_db.data
    y = user_db.target
    con_con_file_list = []
    tp_list = []
    for idx, column in enumerate(X.T):
        feature_name = user_db.feature_names[idx]
        feature_name = feature_name.replace("/","-")
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
        file_name = f"HW4_{feature_name}_lin_plot.html"
        fig.write_html(file=file_name, include_plotlyjs="cdn")
        con_con_file_list += [file_name]
        tp_list += [f'{p_value} & {t_value}']

    return con_con_file_list, tp_list


def plot_cont_cat(to_plot):
    # Violin plot on predictor grouped by response
    user_db = to_plot
    X = user_db.data
    y = user_db.target
    con_cat_file_list=[]
    #
    for idx, column in enumerate(X.T):
        feature_name = user_db.feature_names[idx]
        feature_name = feature_name.replace("/","-")
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
        file_name = f"HW4_{feature_name}_cont_cat_violin_plot.html"
        fig.write_html(file=file_name, include_plotlyjs="cdn")
        con_cat_file_list += [file_name]
    return con_cat_file_list


def plot_cat_cat(to_plot):
    # haven't figured out how to implement a z in a Heatplot here, using violin
    user_db = to_plot
    X = user_db.data
    y = user_db.target
    cat_cat_file_list=[]
    #
    for idx, column in enumerate(X.T):
        feature_name = user_db.feature_names[idx]
        feature_name = feature_name.replace("/","-")
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
        file_name = f"HW4_{feature_name}_cat_cat_violin_plot.html"
        fig.write_html(file=file_name, include_plotlyjs="cdn")
        cat_cat_file_list += [file_name]
    return cat_cat_file_list


def plot_cat_cont(to_plot):
    # Violin plot on response grouped by predictor
    user_db = to_plot
    X = user_db.data
    y = user_db.target
    cat_con_file_list=[]
    #
    for idx, column in enumerate(X.T):
        feature_name = user_db.feature_names[idx]
        feature_name = feature_name.replace("/","-")
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
        file_name = f"HW4_{feature_name}_cat_con_violin_plot.html"
        fig.write_html(file=file_name, include_plotlyjs="cdn")
        cat_con_file_list += [file_name]
    return cat_con_file_list

def plot_bool(to_plot):
    user_db = to_plot
    X = user_db.data
    y = user_db.target
    bool_file_list = []
    for idx, column in enumerate(X.T):
        feature_name = user_db.feature_names[idx]
        predictor = sm.add_constant(column)
        log_regression_model = sm.Logit(y, predictor)
        log_regression_model_fitted = log_regression_model.fit()
        print(f"Variable: {feature_name}")
        print(log_regression_model_fitted.summary())

        # Get the stats
        t_value = round(log_regression_model_fitted.tvalues[1], 6)
        p_value = "{:.6e}".format(log_regression_model_fitted.pvalues[1])

        # Plot the figure
        fig = px.scatter(x=column, y=y, trendline="ols")
        fig.update_layout(
            title=f"Variable: {feature_name}: (t-value={t_value}) (p-value={p_value})",
            xaxis_title=f"Variable: {feature_name}",
            yaxis_title="y",
        )
        file_name = f"HW4_{feature_name}_bool_plot.html"
        fig.write_html(file=f"HW4_{feature_name}log_plot.html", include_plotlyjs="cdn")
        bool_file_list += [file_name]
    return bool_file_list

# add boolean check incase type check is wrong
def col_is_bool(df,col):
    c = len(df[col].unique())
    if c == 2:
        return col
    else:
        return


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

def clickable_report(loc):
    name= os.path.basename(loc)
    # remove target="_blank" from below to open in the report tab
    return '<a target="_blank" href=\"{}\">{}</a>'.format(loc,name)

def coor_con_con(df, col, resp):
    corr_con_con_list =[]
    a = df[col]
    b = df[resp]
    corr_con_con_list += [stats.pearsonr(a,b)]
    return corr_con_con_list

def coor_con_cat(df, col, resp):
    corr_con_cat_list =[]
    a = df[col]
    b = df[resp]
    corr_con_cat_list += [stats.kendalltau(a,b)]
    return corr_con_cat_list

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

    choice = int(input("Which set? ")or 3)

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
    working_df["target"] = pd.Series(the_ds.target)  # chg designate response(s)
    working_df.head()

    # get column names

    col_list = working_df.columns.values.tolist()
    #titles = [i.replace(")", "_").replace("(", "").replace(" ", "_") for i in col_list]
    #working_df.columns = titles
    print_heading("Original Dataset")
    print(working_df)

    # ~RESPONSE~
    # y = the_ds.target  # assign the response here #chg
    resp = input('What is desired respnose |default = target ') or 'target'
    res_type = tot(working_df[resp])
    print_heading("Response type is " + res_type)

    # Group Predictor types
    type_mask = [tot(working_df[i]) for i in col_list]
    bool_list = [col_is_bool(working_df,i) for i in col_list]
    bool_df = pd.DataFrame(bool_list,index=[col_list])
    predictor_array = np.column_stack((col_list, type_mask))
    pred_df = pd.DataFrame(predictor_array, columns=["Predictor", "Category"])

    # ~PREDICTORS~
    # Allow user to select the desired features
    # feature_list = predictor_select(the_ds)
    # enable above line to select only specific features to evaluate

    cont_feature_df = pred_df[
        pred_df["Category"] == "continuous"
        ]  # where tot continuous and bool_check false
    try:
        cont_feature_df = cont_feature_df.drop(
            "target", axis=1, inplace=True
        )
    except Exception:
        pass

    cat_feature_df = pred_df[
        pred_df["Category"] != "continuous"
        ]  # where tot not continuous or binary
    try:
        cat_feature_df = cat_feature_df.drop(
            "target", axis=1, inplace=True
        )
    except Exception:
        pass

    binary_feature_df = pred_df[
        pred_df["Category"] == "binary"
        ]  # where tot binary
    try:
        binary_feature_df = binary_feature_df.drop(
            "target", axis=1, inplace=True
        )
    except Exception:
        pass

    # Need to check if boolean since sometimes binary fails to cathc booleans
    bool_feature_df = bool_df.dropna()
    try:
        bool_feature_df = bool_feature_df.drop(
            "target", axis=1, inplace=True
        )
    except Exception:
        pass

    print("No Continuous!") if cont_feature_df.empty else print(cont_feature_df)
    print("No Categorical!") if cat_feature_df.empty else print(cat_feature_df)
    print("No Boolean!") if binary_feature_df.empty else print(binary_feature_df)

    cont_feature_list = list(cont_feature_df["Predictor"])
    cat_feature_list = list(cat_feature_df["Predictor"])

    # Generate Report DF
    # 1
    report_col = (
        "Category",
        "p-val_&_t-val",
        "Regression",
        "Logistic_Regression",
        "If Cat v Cat",
        "If Cont v Cat",
    )
    report_df = pd.DataFrame("", index=col_list, columns=report_col)
    report_df = report_df.drop(['target'])
    # 2
    report_col_2 = ('Correlation Con v Con',
                    'Correlation Con v Cat',)
    report_df_2 = pd.DataFrame("", index=col_list, columns=report_col_2)
    pred_df = pred_df.set_index(["Predictor"])
    pred_df = pred_df.drop(['target'])

    # Update Report with data
    report_df.index.name = "Predictor"
    pred_df.index = report_df.index

    # Make plots
#    for i in pred_df:
#            if res_type == "continuous" and i in cat_feature_list:
    con_cat_file_list = plot_cont_cat(the_ds)
    temp_df = pd.DataFrame(con_cat_file_list, columns=['If Cont v Cat'])
    list_to_df(temp_df, report_df, "If Cont v Cat")
#            elif res_type == "continuous" and i in cont_feature_list:
    con_con_file_list, tp_list = plot_cont_cont(the_ds)
    temp_df = pd.DataFrame(con_con_file_list, columns=['Regression'])
    list_to_df(temp_df, report_df, "Regression")
    temp_df = pd.DataFrame(tp_list, columns=['p-val_&_t-val'])
    list_to_df(temp_df, report_df, "p-val_&_t-val")

#    bool_list_1 =

    # else:

    cat_con_file_list = plot_cat_cont(the_ds)
    temp_df = pd.DataFrame(cat_con_file_list, columns=['Logistic_Regression'])
    list_to_df(temp_df, report_df, "Logistic_Regression")
    cat_cat_file_list = plot_cat_cat(the_ds)
    temp_df = pd.DataFrame(cat_cat_file_list, columns=['If Cat v Cat'])
    list_to_df(temp_df, report_df, "If Cat v Cat")
#    bool_list_2 =
    # correlation
    #con con
    corr_con_con_list = [coor_con_con(working_df, i, 'target') for i in col_list]
    temp_df = pd.DataFrame(corr_con_con_list, columns=['Correlation Con v Con'])
    list_to_df(temp_df, report_df_2, 'Correlation Con v Con')
    coor_con_cat_list = [coor_con_cat(working_df, i, 'target') for i in col_list]
    temp_df = pd.DataFrame(corr_con_con_list, columns=['Correlation Con v Cat'])
    list_to_df(temp_df, report_df_2, 'Correlation Con v Cat')

    report_df_2 = report_df_2.sort_values(['Correlation Con v Con'], ascending=[False])
    report_df_2 = report_df_2.drop(['target'])
    report_df_2.to_html("HW_report_2_" + datetime.now().strftime("%Y_%m_%d-%H_%M") + ".html")
    #con cat

    # add plots to report

    list_to_df(pred_df, report_df, "Category")





    # Make some cols clickable
    report_style = report_df.style.format({'Regression': clickable_report})\
        .format({'Logistic_Regression': clickable_report})\
        .format({'If Cat v Cat': clickable_report})\
        .format({'If Cont v Cat': clickable_report})
# Save report to HTML
    print('See report in current directory')
#    report_df.DataFrame.to_html(
#       "HW_report_" + datetime.now().strftime("%Y_%m_%d-%H_%M") + ".html"
#    )
    report = report_style.render()
    with open("HW_report_" + datetime.now().strftime("%Y_%m_%d-%H_%M") + ".html", "w") as temp:
        temp.write(report)



#    report_html = report_style.render()
    print(datetime.now() - start_t)


if __name__ == "__main__":
    sys.exit(main())
