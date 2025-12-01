from flask import Flask, render_template
from card import Card
import mysql.connector as mysql
import json

conn = mysql.connect(host="127.0.0.1", user="root", password="", autocommit=True)
cur = conn.cursor()
cur.execute("USE mysql")

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 # force no caching for faster debugging

def all_cards() -> list[Card]:
    out = []

    cur.execute("SELECT * FROM CardUsage ORDER BY wins DESC")
    res = cur.fetchall()
    for row in res:
        out.append(Card(row))

    return out

def cards_by_tag(tag: str) -> list[Card]:
    out = []

    cur.execute(f"SELECT * FROM CardUsage WHERE tags LIKE '%{tag}%' ORDER BY wins DESC")
    res = cur.fetchall()
    for row in res:
        out.append(Card(row))

    return out

def all_tags() -> list[str]:
    cards = all_cards()
    tagset = set()

    for card in cards:
        for tag in card.tags.split(","):
            if tag != "":
                tagset.add(tag)

    return list(tagset)

@app.route("/")
def index():
    filtertags = all_tags()
    filtertags.insert(0, "All")
    return render_template("index.html", tags=filtertags)

@app.route("/allcards")
def all_cards_json():
    out = all_cards()
    return json.dumps(out, default=vars)

@app.route("/cards/<tag>")
def cardstag(tag):
    out = []
    if tag == "All" or tag == "all":
        out = all_cards()
    else:
        out = cards_by_tag(tag)
    return json.dumps(out, default=vars)