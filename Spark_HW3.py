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

from pyspark import StorageLevel
from pyspark.sql import SparkSession
# Setup Spark
spark = SparkSession.builder.master("local[*]").getOrCreate()

database = "baseball"
port = "3306"
user = "root"
password = "x11desktop"

bb_df = spark.read.format("jdbc").options(
    url=f"jdbc:mysql://localhost:{port}/{database}",
    driver="com.mysql.cj.jdbc.Driver",
    dbtable="batter_counts",
    user=user,
    password=password).load()

bb_df.select("batter", "game_id", "atBat", "Hit").show()

gd_df = spark.read.format("jdbc").options(
    url=f"jdbc:mysql://localhost:{port}/{database}",
    driver="com.mysql.cj.jdbc.Driver",
    dbtable="game",
    user=user,
    password=password).load()

gd_df.select("game_id", "local_date").show()
