import os
import sys
import mariadb
#from sklearn.linear_model import LogisticRegression
#from sklearn.datasets import make_classification
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
#from sklearn.inspection import permutation_importance
from sklearn.ensemble import RandomForestClassifier as rfc
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.ensemble import RandomForestRegressor as rfr
import statsmodels.api as sm
from plotly import express as px
from plotly import figure_factory as ff
from plotly import graph_objects as go


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

# Main functions
def main():
    # Connect to MariaDB Platform
    try:
        conn = mariadb.connect(
            user="root",
            password="x11desktop",
            host="localhost",
            port=3306,
            database="baseball"

        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    df_roll_14 = pd.read_sql('SELECT * FROM rolling_014', con=conn)
    df_roll_30 = pd.read_sql('SELECT * FROM rolling_030', con=conn)
    df_roll_90 = pd.read_sql('SELECT * FROM rolling_090', con=conn)
    df_roll_180 = pd.read_sql('SELECT * FROM rolling_180', con=conn)

    #Drop any remaining NULLS. expecting a few games that do not have get filltered by R but are with non major teams.
    df1 = df_roll_14.dropna()
    df2 = df_roll_30.dropna()
    df3 = df_roll_90.dropna()
    df4 = df_roll_180.dropna()

    print('14 day rolling shape is ',df1.shape)
    df1_desc = df1.describe()
    print('30 day rolling shape is ',df2.shape)
    df2_desc = df2.describe()
    print('90 day rolling shape is ',df3.shape)
    df3_desc = df3.describe()
    print('180 day rolling shape is ',df4.shape)
    df4_desc = df4.describe()

    df_list = (df1,df2,df3,df4)
    ctr = 0
    ##########################################################################################
    for i in df_list:
        ctr += 1
        if ctr == 1:
            addon = ("_14_day")
        elif ctr == 2:
            addon = ("_30_day")
        elif ctr == 3:
            addon = ("_90_day")
        elif ctr == 4:
            addon = ("_180_day")


        working_df = i # will be looped

        # place holder for loop through all dfs
        response = np.array(working_df['win'])
        working_df = working_df.drop('win',axis=1).iloc[:,7:]
        feature_list = list(working_df.columns)
        features = np.array(working_df)

        # Generate Report DF

        report_cols = [
            "Predictor"
    #        ,"t-Score"
    #        ,"p-Value"
    #        ,"Charts"
        ]
        df_report = pd.DataFrame(columns=report_cols)
        df_report["Predictor"]= feature_list

        train_features, test_features, train_labels, test_labels = train_test_split(features, response, test_size = 0.20, random_state = 42)

        print('Training Features Shape:', train_features.shape)
        print('Training Labels Shape:', train_labels.shape)
        print('Testing Features Shape:', test_features.shape)
        print('Testing Labels Shape:', test_labels.shape)


        rf = rfr(n_estimators = 100, random_state = 42)
        rf.fit(train_features, train_labels);

        predictions = rf.predict(test_features)
        errors = abs(predictions - test_labels)
        print('Mean Absolute Error:', round(np.mean(errors), 2))




        importance = rf.feature_importances_
        df_imp = pd.DataFrame(columns=["Random Forest Importance"])
        df_imp["Random Forest Importance"] = importance


        df_report = pd.concat([df_report, df_imp], axis=1)

        df_report = df_report.sort_values('Random Forest Importance',ascending=False)

        df_report.to_html("Report"+ str(addon) +".html")
        print(ctr)
        print(addon + " complete....next")
    #####################################################################################################
    df_14_part = df_roll_14[['Pop_Out'
        ,'Ground_Out'
        ,'Line_Out'
        ,'Runs'
        ,'Duhble'
        ,'Grounded_Into_DP'
        ,'XBH'
        ,'toBase'
        ,'Hit_By_Pitch'
        ,'stolenBase2B'
        ,'Triple'
        ]].copy()
    df_30_part = df_roll_30[['Fly_Out'
        ,'atBat'
        ,'Strikeout'
        ,'Single'
        ,'Force_Out'
        ,'Hit'
        ,'Sac_Bunt'
        ,'Field_Error'
        ,'Intent_Walk'
        ,'Sac_Fly'
        ,'Double_Play'
        ]].copy()
    df_90_part = df_roll_90[['Walk']].copy()
    df_180_part = df_roll_180[['GO_AO'
        ,'BB_pct'
        ,'AB_HR'
        ,'HR_H'
        ,'OBP'
        ,'Bat_Avg'
        ,'pathag_v1'
        ,'pathag_v2'
        ,'pathag_v3'
        ,'PA_SO'
        ,'K_pct'
        ,'SB_pct'
        ,'BB_K'
        ,'K_BB'
        ,'OPS'
        ,'GPA'
        ,'Net_Jet_Lag'
        ,'Home_Run'
        ]].copy()


    final_df = df_roll_14.iloc[:,:7]
    #final_df = final_df.append([df_14_part,df_30_part,df_90_part,df_180_part])
    final_df = pd.concat([final_df,df_14_part,df_30_part,df_90_part,df_180_part],axis = 1)
    final_report_df = final_df.dropna()
    print('Final report contains Features with >= .01 importnace. Best date range selected for each feature.')
    print('14 Day Features')
    print(df_14_part.columns)
    print('30 Day Features')
    print(df_30_part.columns)
    print('90 Day Features')
    print(df_90_part.columns)
    print('180 Day Features')
    print(df_180_part.columns)
    #########################
    working_df = final_report_df

        # place holder for loop through all dfs
    response = np.array(working_df['win'])
    working_df = working_df.iloc[:,7:]
    feature_list = list(working_df.columns)
    features = np.array(working_df)

    # Generate Report DF

    report_cols = [
        "Predictor",
        "t-Score",
        "p-Value",
        "Charts",
    ]
    df_report = pd.DataFrame(columns=report_cols)
    df_report["Predictor"]= feature_list

    train_features, test_features, train_labels, test_labels = train_test_split(features, response, test_size = 0.20, random_state = 42)

    print('Training Features Shape:', train_features.shape)
    print('Training Labels Shape:', train_labels.shape)
    print('Testing Features Shape:', test_features.shape)
    print('Testing Labels Shape:', test_labels.shape)


    rf = rfr(n_estimators = 100, random_state = 42)
    rf.fit(train_features, train_labels);

    predictions = rf.predict(test_features)
    errors = abs(predictions - test_labels)
    print('Mean Absolute Error:', round(np.mean(errors), 2))




    importance = rf.feature_importances_
    df_imp = pd.DataFrame(columns=["Random Forest Importance"])
    df_imp["Random Forest Importance"] = importance


    df_report = pd.concat([df_report, df_imp], axis=1)
    X = final_report_df.iloc[:,7:]
    y = final_report_df['win']
    t_list = []
    p_list = []
    file_list = []

    for idx, column in enumerate(X.T):
        if idx >= 41: break
        feature_name = feature_list[idx]
        linear_regression_model = sm.OLS(y, X[feature_list[idx]])
        linear_regression_model_fitted = linear_regression_model.fit()
        print(f"Variable: {feature_name}")
        print(linear_regression_model_fitted.summary())
        t_value = (linear_regression_model_fitted.tvalues[0])
        p_value =(linear_regression_model_fitted.f_pvalue)
        print("*****************************************************************************")
        t_list += [t_value]
        p_list += [p_value]
        fig = px.violin(final_report_df, x="win", y=feature_name)
        fig.update_layout(
            title=f"Variable: {feature_name}: (t-value={t_value}) (p-value={p_value})",
            xaxis_title=f"Variable: {feature_name}",
            yaxis_title="y",
        )
        file_name = f"Final_{feature_name}_plot.html"
        fig.write_html(file=file_name, include_plotlyjs="cdn")
        file_list += [file_name]

    temp_df = pd.DataFrame(t_list, columns=['t-Score'])
    list_to_df(temp_df, df_report, "t-Score")
    temp_df = pd.DataFrame(p_list, columns=['p-Value'])
    list_to_df(temp_df, df_report, "p-Value")
    temp_df = pd.DataFrame(file_list, columns=["Charts"])
    list_to_df(temp_df, df_report, "Charts")

    df_report = df_report.sort_values('Random Forest Importance',ascending=False)

    df_report.to_html("Report_final.html")
    report_style = df_report.style.format({'Charts': clickable_report})
    report = report_style.render()
    with open("Report_final.html", "w") as temp:
        temp.write(report)

    print("Final report complete")

    #########################



    print('Model is based on Home Team winning.')

if __name__ == "__main__":
    sys.exit(main())