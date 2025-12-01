from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("ClashStep2_WinnerCards").getOrCreate()

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

cards = spark.read.csv(
    "cards.csv",
    header=True,
    inferSchema=True
).withColumnRenamed("team.card1.id", "card_id") \
 .withColumnRenamed("team.card1.name", "card_name")

winner_cards_long = battles.select(
    "battleTime",
    "arena_id",
    "game_mode_id",
    "avg_starting_trophies",
    "winner_tag",
    F.explode(
        F.array(
            "winner_card1_id",
            "winner_card2_id",
            "winner_card3_id",
            "winner_card4_id",
            "winner_card5_id",
            "winner_card6_id",
            "winner_card7_id",
            "winner_card8_id",
        )
    ).alias("card_id")
)

winner_cards_named = winner_cards_long.join(cards, on="card_id", how="left")

print("=== Sample of winner cards (one row per card) ===")
winner_cards_named.show(20, truncate=False)

spark.stop()
