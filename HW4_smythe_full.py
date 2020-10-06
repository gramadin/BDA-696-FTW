"""
Created by Ed Smythe Oct 2020
BDA 696 @ SDSU
Homework - Assignment 4
    Given a pandas dataframe
        Contains both a response and predictors
    Given a list of predictors and the response columns
        Determine if response is continuous or boolean
            (don't worry about >2 category predictions)
        Loop through each predictor column
            Determine if the predictor cat/cont
            Automatically generate the necessary plot(s) to inspect it
            Calculate the different ranking algos
                p-value & t-score along with it's plot
                    Regression: Continuous response
                    Logistic Regression: Boolean response
                Difference with mean of response along with it's plot
                    (weighted and unweighted)
                Random Forest Variable importance ranking
            Generate a table with all the variables and their rankings
    I'm going to grade this by giving it some random dataset and seeing
        if it outputs everything
    Desire: HTML based rankings report with links to the plots

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
from io import StringIO

import pandas as pd
import plotly.express as px
import pydot
import statsmodels.api
from pandas import DataFrame
from plotly import graph_objects as go
from sklearn import datasets
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier, export_graphviz


# Ploting Continuous data
def plot_continuous(working_df):
    user_db = working_df
    X = user_db.data
    y = user_db.target
    for idx, column in enumerate(X.T):
        feature_name = user_db.feature_names[idx]
        predictor = statsmodels.api.add_constant(column)
        linear_regression_model = statsmodels.api.OLS(y, predictor)
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
        fig.write_html(file=f"./HW4_plot{idx}.html", include_plotlyjs="cdn")
    return


def print_heading(title):
    print("*" * 80)
    print(title)
    print("*" * 80)
    return


def plot_decision_tree(decision_tree, feature_names, class_names, file_out):
    with StringIO() as dot_data:
        export_graphviz(
            decision_tree,
            feature_names=feature_names,
            class_names=class_names,
            out_file=dot_data,
            filled=True,
        )
        graph = pydot.graph_from_dot_data(dot_data.getvalue())
        graph[0].write_pdf(file_out + ".pdf")  # must access graph's first element
        graph[0].write_png(file_out + ".png")  # must access graph's first element


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
    print(
        """ Select SKLearn dataset to use: ~default is 3~
                    1 - boston
                    2 - iris
                    3 - diabetes
                    4 - digits
                    5 - linnerud
                    6 - wine
                    7 - breast cancer
                    8 - user choice
                  """
    )

    choice = int(input("Which set? " or 3))

    if choice == 1:
        choice = ds1
    elif choice == 2:
        choice = ds2
    elif choice == 3:
        choice = ds3
    elif choice == 4:
        choice = ds4
    elif choice == 5:
        choice = ds5
    elif choice == 6:
        choice = ds6
    elif choice == 7:
        choice = ds7
    elif choice == 8:
        choice = input("direct path to dataset: ")
    elif choice == "":
        choice = ds3
    else:
        print(f"{choice} is an invalid entry. Please try again.")

    print(f"You chose {choice}")

    the_ds = choice
    # turn into a pandas df
    working_df = pd.DataFrame(the_ds.data, columns=the_ds.feature_names)
    working_df["target"] = pd.Series(the_ds.target)
    working_df.head()

    # get column names
    col_list = working_df.columns.values.tolist()

    # Increase pandas print viewport (so we see more on the screen)
    pd.set_option("display.max_rows", 60)
    pd.set_option("display.max_columns", 500)
    pd.set_option("display.width", 1_040)

    # working_df.columns = col_list

    # Drop rows with missing values
    # working_df = working_df.dropna()

    print_heading("Original Dataset")
    print(working_df)

    # Continuous Features ~ use a function to get which is continus
    # Need to find out why putting col_list[:-1] does not work here
    continuous_features = [
        "sepal length (cm)",
        "sepal width (cm)",
        "petal length (cm)",
        "petal width (cm)",
    ]  # chg
    X = working_df[continuous_features].values

    # Response
    y = working_df[col_list[-1:]].values

    # Decision Tree Classifier
    max_tree_depth = 7
    tree_random_state = 0  # Always set a seed
    decision_tree = DecisionTreeClassifier(
        max_depth=max_tree_depth, random_state=tree_random_state
    )
    decision_tree.fit(X, y)

    # Plot the decision tree
    plot_decision_tree(
        decision_tree=decision_tree,
        feature_names=continuous_features,
        class_names="classification",
        file_out="./hw4_tree",
    )

    # Find an optimal tree via cross-validation
    parameters = {
        "max_depth": range(1, max_tree_depth),
        "criterion": ["gini", "entropy"],
    }
    decision_tree_grid_search = GridSearchCV(
        DecisionTreeClassifier(random_state=tree_random_state), parameters, n_jobs=4
    )
    decision_tree_grid_search.fit(X=X, y=y)

    cv_results = DataFrame(decision_tree_grid_search.cv_results_["params"])
    cv_results["score"] = decision_tree_grid_search.cv_results_["mean_test_score"]
    print_heading("Cross validation results")
    print(cv_results)
    print_heading("Cross validation results - HTML table")
    print(cv_results.to_html())

    # Plot these cross_val results
    gini_results = cv_results.loc[cv_results["criterion"] == "gini"]
    entropy_results = cv_results.loc[cv_results["criterion"] == "entropy"]
    data = [
        go.Scatter(
            x=gini_results["max_depth"].values,
            y=gini_results["score"].values,
            name="gini",
            mode="lines",
        ),
        go.Scatter(
            x=entropy_results["max_depth"].values,
            y=entropy_results["score"].values,
            name="entropy",
            mode="lines",
        ),
    ]

    layout = go.Layout(
        title="Cross Validation",
        xaxis_title="Tree Depth",
        yaxis_title="Score",
    )

    fig = go.Figure(data=data, layout=layout)
    fig.show()
    fig.write_html(
        file="./HW4_cross_val.html",
        include_plotlyjs="cdn",
    )

    # Get the "best" model
    best_tree_model = decision_tree_grid_search.best_estimator_

    # Plot this "best" decision tree
    plot_decision_tree(
        decision_tree=best_tree_model,
        feature_names=continuous_features,
        class_names="classification",
        file_out="./HW4_cross_val",
    )
    #    F" {(datetime.now() - start_t)} seconds"
    return


if __name__ == "__main__":
    sys.exit(main())
