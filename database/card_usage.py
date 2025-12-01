from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import mysql.connector as mysql

spark = SparkSession.builder.appName("ClashStep3_CardUsage").getOrCreate()
conn = mysql.connect(host="127.0.0.1", user="root", password="", autocommit=True)
cur = conn.cursor()

cur.execute("CREATE DATABASE IF NOT EXISTS mysql")
cur.execute("USE mysql")

print("reading battles csv... ", end="")
battles = spark.read.csv(
    "battles_Jan01_21.csv",
    header=True,
    inferSchema=True
)
print("done")

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

print("reading cards csv... ", end="")
cards = spark.read.csv(
    "cards.csv",
    header=True,
    inferSchema=True
).withColumnRenamed("team.card1.id", "card_id") \
 .withColumnRenamed("team.card1.name", "card_name")
print("done")

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

card_usage = (
    winner_cards_named
    .groupBy("card_id", "card_name")
    .agg(
        F.count("*").alias("wins_with_card"),
        F.avg("avg_starting_trophies").alias("avg_trophies_when_used")
    )
    .orderBy(F.desc("wins_with_card"))
)

# tags: WinCondition, Spell, MiniTank, AirDefense, Building, AoE
card_data = spark.createDataFrame(
    [
[26000000, 3, "MiniTank,"], # Knight
[26000001, 3, "AirDefense,"], # Archers
[26000002, 2, ""], # Goblins
[26000003, 5, "WinCondition,"], # Giant
[26000004, 7, "WinCondition,"], # P.E.K.K.A
[26000005, 3, ""], # Minions
[26000006, 5, "WinCondition,"], # Balloon
[26000007, 5, "AoE,"], # Witch
[26000008, 5, ""], # Barbarians
[26000009, 8, "WinCondition,AoE,"], # Golem
[26000010, 1, ""], # Skeletons
[26000011, 4, "MiniTank,AoE,"], # Valkyrie
[26000012, 3, ""], # Skeleton Army
[26000013, 2, "AoE,"], # Bomber
[26000014, 4, "AirDefense,"], # Musketeer
[26000015, 4, "AirDefense,AoE,"], # Baby Dragon
[26000016, 5, "WinCondition,"], # Prince
[26000017, 5, "AirDefense,AoE,"], # Wizard
[26000018, 4, "MiniTank,"], # Mini P.E.K.K.A
[26000019, 2, "AirDefense,"], # Spear Goblins
[26000020, 6, "WinCondition,"], # Giant Skeleton
[26000021, 4, "WinCondition,"], # Hog Rider
[26000022, 4, ""], # Minion Horde
[26000023, 3, "AirDefense,AoE,"], # Ice Wizard
[26000024, 6, "WinCondition,"], # Royal Giant
[26000025, 3, ""], # Guards
[26000026, 3, "AirDefense,AoE,"], # Princess
[26000027, 4, "MiniTank,AoE,"], # Dark Prince
[26000028, 9, "AirDefense,"], # Three Musketeers
[26000029, 7, ""], # Lava Hound
[26000030, 1, "AoE,"], # Ice Spirit
[26000031, 1, "AoE,"], # Fire Spirits
[26000032, 3, "MiniTank,"], # Miner
[26000033, 6, "WinCondition,"], # Sparky
[26000034, 5, "AoE,"], # Bowler
[26000035, 4, ""], # Lumberjack
[26000036, 4, ""], # Battle Ram
[26000037, 4, ""], # Inferno Dragon
[26000038, 2, "MiniTank,AoE,"], # Ice Golem
[26000039, 3, "AirDefense,"], # Mega Minion
[26000040, 3, "AirDefense,"], # Dart Goblin
[26000041, 3, "AirDefense,"], # Goblin Gang
[26000042, 4, "AirDefense,AoE,"], # Electro Wizard
[26000043, 6, "WinCondition,"], # Elite Barbarians
[26000044, 4, "AirDefense,AoE,"], # Hunter
[26000045, 5, "AirDefense,AoE,"], # Executioner
[26000046, 3, ""], # Bandit
[26000047, 7, ""], # Royal Recruits
[26000048, 4, ""], # Night Witch
[26000049, 2, "AirDefense,"], # Bats
[26000050, 3, "AoE,"], # Royal Ghost
[26000051, 5, "WinCondition,"], # Ram Rider
[26000052, 4, "AirDefense,"], # Zappies
[26000053, 5, ""], # Rascals
[26000054, 5, "MiniTank,"], # Cannon Cart
[26000055, 7, "WinCondition,AoE,"], # Mega Knight
[26000056, 3, "WinCondition,AoE,"], # Skeleton Barrel
[26000057, 4, "AirDefense,"], # Flying Machine
[26000058, 2, "WinCondition,"], # Wall Breakers
[26000059, 5, ""], # Royal Hogs
[26000060, 6, ""], # Goblin Giant
[26000061, 3, ""], # Fisherman
[26000062, 4, "AirDefense,AoE,"], # Magic Archer
[26000063, 5, "AoE,"], # Electro Dragon
[26000064, 3, "AirDefense,AoE,"], # Firecracker
[26000067, 4, "WinCondition,"], # Elixir Golem
[26000068, 4, "AoE,"], # Battle Healer
[26000080, 4, "AirDefense,AoE,"], # Skeleton Dragons
[26000083, 4, "AoE,"], # Mother Witch
[26000084, 1, "AirDefense,AoE,"], # Electro Spirit
[26000085, 7, "WinCondition,AoE,"], # Electro Giant
[27000000, 3, "Building,"], # Cannon
[27000001, 4, "Building,"], # Goblin Hut
[27000002, 4, "Building,AoE,"], # Mortar
[27000003, 5, "Building,"], # Inferno Tower
[27000004, 4, "Building,AoE,"], # Bomb Tower
[27000005, 6, "Building,"], # Barbarian Hut
[27000006, 4, "Building,"], # Tesla
[27000007, 6, "Building,"], # Elixir Collector
[27000008, 6, "Building,"], # X-Bow
[27000009, 3, "Building,"], # Tombstone
[27000010, 4, "Building,"], # Furnace
[27000012, 4, "Building,"], # Goblin Cage
[28000000, 4, "Spell,AirDefense,AoE,"], # Fireball
[28000001, 3, "Spell,AirDefense,AoE,"], # Arrows
[28000002, 2, "Spell,AirDefense,AoE,"], # Rage
[28000003, 6, "Spell,AirDefense,AoE,"], # Rocket
[28000004, 3, "Spell,"], # Goblin Barrel
[28000005, 4, "Spell,AirDefense,AoE,"], # Freeze
[28000006, 0, "Spell,"], # Mirror
[28000007, 6, "Spell,AirDefense,AoE,"], # Lightning
[28000008, 2, "Spell,AirDefense,AoE,"], # Zap
[28000009, 4, "Spell,AirDefense,AoE,"], # Poison
[28000010, 5, "Spell,"], # Graveyard
[28000011, 2, "Spell,AoE,"], # The Log
[28000012, 3, "Spell,AirDefense,AoE,"], # Tornado
[28000013, 3, "Spell,AoE,"], # Clone
[28000014, 3, "Spell,AoE,"], # Earthquake
[28000015, 2, "Spell,AoE,"], # Barbarian Barrel
[28000016, 1, "AoE,"], # Heal Spirit
[28000017, 2, "Spell,AirDefense,AoE,"], # Giant Snowball
[28000018, 3, "AirDefense,AoE,"], # Royal Delivery
    ],
    ["card_id", "cost", "tags"]
)
card_usage = card_usage.join(card_data, on="card_id", how="right")

print("=== Top 20 most-used cards in winning decks ===")
card_usage.show(20, truncate=False)

print("exporting to mysql database...")
cur.execute("DROP TABLE IF EXISTS CardUsage")
cur.execute("CREATE TABLE CardUsage (" \
"card_id INT PRIMARY KEY, " \
"card_name VARCHAR(200), " \
"wins INT, " \
"avg_trophies INT, " \
"cost INT, " \
"tags VARCHAR(200));")

sqlvalues = ""
for card in card_usage.rdd.collect():
    sqlvalues += f"({card.card_id}, '{card.card_name}', {card.wins_with_card}, {card.avg_trophies_when_used}, {card.cost}, '{card.tags}'),"
sqlvalues = sqlvalues[0:-1]
cur.execute(f"INSERT INTO CardUsage VALUES {sqlvalues};")

# print finished mysql table
cur.execute("SELECT * FROM CardUsage")
res = cur.fetchall()
for row in res:
    print(row)

print("cleaning up...")
# cleanup
spark.stop()
cur.close()
conn.cmd_quit()