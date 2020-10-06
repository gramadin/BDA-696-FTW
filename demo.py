import sys

import statsmodels.api
from plotly import express as px
from sklearn import datasets


def main():
    diabetes = datasets.load_diabetes()
    X = diabetes.data
    y = diabetes.target

    for idx, column in enumerate(X.T):
        feature_name = diabetes.feature_names[idx]
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
        fig.write_html(file=f"demo{idx}.html", include_plotlyjs="cdn")
    return


if __name__ == "__main__":
    sys.exit(main())
