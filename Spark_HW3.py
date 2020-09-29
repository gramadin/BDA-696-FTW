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
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.feature import CountVectorizer
from pyspark.sql import SparkSession

def main():
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
    bb_df.createOrReplaceTempView("batter")
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
            , atBat
            , Hit 
            , (Hit/nullif(atBat,0)) as game_bat_avg
        from batter
        """
        )
    bat_avg.show()


if __name__ == "__main__":
    sys.exit(main())
