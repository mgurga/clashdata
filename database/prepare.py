from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import mysql.connector as mysql

spark = SparkSession.builder.appName("clashdata").getOrCreate()
conn = mysql.connect(host="127.0.0.1", user="root", password="", autocommit=True)
cur = conn.cursor()

cur.execute("CREATE DATABASE IF NOT EXISTS mysql")
cur.execute("USE mysql")

print("loading cards csv...")
cards = spark.read.csv(
    "cards.csv",
    header=True,
    inferSchema=True
).withColumnRenamed("team.card1.id", "card_id") \
 .withColumnRenamed("team.card1.name", "card_name")

print("loading battles csv...")
battles = spark.read.csv(
    "battles_Jan01_21.csv",
    header=True,
    inferSchema=True
)

battles = (
    battles
    .withColumnRenamed("average.startingTrophies", "avg_starting_trophies")
    .withColumnRenamed("arena.id", "arena_id")
    .withColumnRenamed("gameMode.id", "game_mode_id")
    .withColumnRenamed("winner.tag", "winner_tag")
    .withColumnRenamed("loser.tag", "loser_tag")
    .withColumnRenamed("winner.trophyChange", "winner_trophy_change")
    .withColumnRenamed("winner.crowns", "winner_crowns")
    .withColumnRenamed("loser.crowns", "loser_crowns")
    .withColumnRenamed("winner.card1.id", "winner_card1_id")
    .withColumnRenamed("winner.card2.id", "winner_card2_id")
    .withColumnRenamed("winner.card3.id", "winner_card3_id")
    .withColumnRenamed("winner.card4.id", "winner_card4_id")
    .withColumnRenamed("winner.card5.id", "winner_card5_id")
    .withColumnRenamed("winner.card6.id", "winner_card6_id")
    .withColumnRenamed("winner.card7.id", "winner_card7_id")
    .withColumnRenamed("winner.card8.id", "winner_card8_id")
)

agg_count = []
print("getting aggrigate count for column ", end="")
for i in range(1, 9):
    print(f"{i}... ", end="")
    agg_count.append(battles.groupBy(f"winner_card{i}_id").agg(F.count("*")))
print()

combined_count = []
for card in cards.rdd.collect():
    print(card.card_id)

# print(battles.select("winner_card1_id").where("26000061").count())

# cleanup
spark.stop()
cur.close()
conn.cmd_quit()