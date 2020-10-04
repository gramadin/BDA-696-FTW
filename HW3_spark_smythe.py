"""
  Created by Ed Smythe Sept 2020
  BDA 696 @ SDSU
  Current run time is ~ xxxx
  Baseball ⚾
  Load this dataset into Spark directly from MariaDB
  Calculate the batting average using an Transformer
  Rolling (over last 100 days)
  Look at the last 100 days that player was in prior to this game
  Hints
  You already did it earlier, use that logic to your advantage
  Make sure the calculation works first
  Then worry about wrapping it up as a transformer
  Only get the needed raw data from MariaDB
  No calculations in MariaDB
  Do all the logic in Spark
"""

import sys

from pyspark import StorageLevel, keyword_only
from pyspark.ml import Pipeline, Transformer
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.feature import CountVectorizer
from pyspark.ml.param.shared import HasInputCols, HasOutputCol
from pyspark.ml.util import DefaultParamsReadable, DefaultParamsWritable
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, concat, lit, split, when






def main():
    # Setup Spark
    spark = SparkSession.builder.master("local[*]").getOrCreate()

    # set up sql defaults
    database = "baseball"
    port = "3306"
    user = "root"
    password = "x11desktop"  # pragma: allowlist secret

    # get table and make batter df
    bb_df = (
        spark.read.format("jdbc")
        .options(
            url=f"jdbc:mysql://localhost:{port}/{database}?zeroDateTimeBehavior=convertToNull",
            driver="com.mysql.cj.jdbc.Driver",
            dbtable="batter_counts",
            user=user,
            password=password,
            inferSchema="true",
            header="true",
        )
        .load()
    )

    bb_df.select("batter", "game_id", "atBat", "Hit").show()
    bb_df.createOrReplaceTempView("batter_tab")
    bb_df.persist(StorageLevel.DISK_ONLY)

    #get table and make game df
    gd_df = spark.read.format("jdbc").options(
        url=f"jdbc:mysql://localhost:{port}/{database}?zeroDateTimeBehavior=convertToNull",
        driver="com.mysql.cj.jdbc.Driver",
        dbtable="game",
        user=user,
        password=password,inferSchema="true", header="true").load()

    gd_df.select("game_id", "local_date").show()
    gd_df.createOrReplaceTempView("game")
    gd_df.persist(StorageLevel.DISK_ONLY)

    bat_avg = spark.sql(
        """
        select
            batter
            , game_id
            , atBat
            , Hit 
            , (Hit/nullif(atBat,0)) as game_bat_avg
            , case when Hit > 0 then 1 else 0 end as ahit
        from batter_tab
        order by batter, game_id
        """
        )
    bat_avg.show()
    # make pipeline
    test_df = spark.sql(
            """
            SELECT
                    *
                    , SPLIT(CONCAT(
                        CASE WHEN batter IS NULL THEN ""
                        ELSE batter END,
                        " ",
                        CASE WHEN game_id IS NULL THEN ""
                        ELSE game_id END,
                        " ",
                        CASE WHEN atBat IS NULL THEN ""
                        ELSE atBat END,
                        " ",
                        CASE WHEN Hit IS NULL THEN ""
                        ELSE Hit END
                    ), " ") AS categorical
                FROM batter_tab
            """
        )
    test_df.show()
    split_column_transform = SplitColumnTransform(
        inputCols=["batter", "game_id", "atBat", "Hit", "ahit"], outputCol="categorical"
    )


    #
    count_vectorizer = CountVectorizer(
        inputCol="categorical", outputCol="categorical_vector"
    )
    random_forest = RandomForestClassifier(
    labelCol="ahit",
    featuresCol="categorical_vector",
    numTrees=100,
    predictionCol="will_hit",
    probabilityCol="prob_of_hit",
    rawPredictionCol="raw_pred_hit",
    )

    pipeline = Pipeline(
        stages=[split_column_transform, count_vectorizer, random_forest]
    )
    model = pipeline.fit(bat_avg)
    bat_avg = model.transform(bat_avg)
    bat_avg.show()

    return


if __name__ == "__main__":
    sys.exit(main())
