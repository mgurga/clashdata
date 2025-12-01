from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("ClashStep1").getOrCreate()

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
)

print("=== Battles schema (after renaming) ===")
battles.printSchema()

print("=== First 5 battles ===")
battles.select(
    "battleTime",
    "arena_id",
    "game_mode_id",
    "avg_starting_trophies",
    "winner_tag",
    "loser_tag",
    "winner_crowns",
    "loser_crowns"
).show(5, truncate=False)

cards = spark.read.csv(
    "cards.csv",
    header=True,
    inferSchema=True
)

cards = (cards
    .withColumnRenamed("team.card1.id", "card_id")
    .withColumnRenamed("team.card1.name", "card_name")
)

print("=== Cards schema ===")
cards.printSchema()

print("=== First 10 cards ===")
cards.show(10, truncate=False)

spark.stop()
