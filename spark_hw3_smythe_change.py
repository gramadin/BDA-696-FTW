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
import tempfile
import requests
from pyspark import StorageLevel
from pyspark.ml import Pipeline
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.feature import CountVectorizer
from pyspark.sql import SparkSession
from pyspark import keyword_only
from pyspark.ml import Transformer
from pyspark.ml.param.shared import HasInputCols, HasOutputCol
from pyspark.ml.util import DefaultParamsReadable, DefaultParamsWritable
from pyspark.sql.functions import col, concat, lit, split, when
#from split_column_transform import SplitColumnTransform

#copy from class notes for custom trasnform
class SplitColumnTransform(
    Transformer,
    HasInputCols,
    HasOutputCol,
    DefaultParamsReadable,
    DefaultParamsWritable,
):
    @keyword_only
    def __init__(self, inputCols=None, outputCol=None):
        super(SplitColumnTransform, self).__init__()
        kwargs = self._input_kwargs
        self.setParams(**kwargs)
        return

    @keyword_only
    def setParams(self, inputCols=None, outputCol=None):
        kwargs = self._input_kwargs
        return self._set(**kwargs)

    def _transform(self, dataset):
        input_cols = self.getInputCols()
        output_col = self.getOutputCol()

        # Generate a list of columns to append
        concat_list = []
        for count, column in enumerate(input_cols):
            column_func = when(col(column).isNull(), lit("")).otherwise(col(column))
            concat_list.append(column_func)
            if count < len(input_cols) - 1:
                concat_list.append(lit(" "))
        dataset = dataset.withColumn(
            output_col, split(concat(*concat_list), pattern=" ")
        )
        return dataset

# Setup Spark
spark = SparkSession.builder.master("local[*]").getOrCreate()


#set up sql defaults
database = "baseball"
port = "3306"
user = "root"
password = "x11desktop"

#get table and make batter df
bb_df = spark.read.format("jdbc").options(
    url=f"jdbc:mysql://localhost:{port}/{database}",
    driver="com.mysql.cj.jdbc.Driver",
    dbtable="batter_counts",
    user=user,
    password=password,inferSchema="true", header="true").load()

bb_df.select("batter", "game_id", "atBat", "Hit").show()
bb_df.createOrReplaceTempView("batter_tab")
bb_df.persist(StorageLevel.DISK_ONLY)

#get table and make game df
gd_df = spark.read.format("jdbc").options(
    url=f"jdbc:mysql://localhost:{port}/{database}",
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

full_table = spark.sql(
    """
    Select batter_counts.batter
           , batter_counts.atBat
           , batter_counts.Hit
           , (batter_counts.Hit/nullif(batter_counts.atBat,0)) as bat_avg
           , year(game.local_date) as g_yr 
    From batter_counts
    Join game on batter_counts.game_id = game.game_id
    Group by batter, g_yr
    """
)
# make pipeline
split_column_transform = SplitColumnTransform(
    inputCols=["g_yr"], outputCol="categorical"
)


#
count_vectorizer = CountVectorizer(
    inputCol="categorical", outputCol="categorical_vector"
)


pipeline = Pipeline(
    stages=[split_column_transform, count_vectorizer]
)
model = pipeline.fit(full_table)
bat_avg = model.transform(full_table)
bat_avg.show()
