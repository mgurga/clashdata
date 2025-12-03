from flask import Flask, render_template
from card import Card
import mysql.connector as mysql
import json

conn = mysql.connect(host="127.0.0.1", user="root", password="", autocommit=True)
cur = conn.cursor()
cur.execute("USE mysql")

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 # force no caching for faster debugging

def all_cards(sort: str = "wins", ascdesc: str = "DESC") -> list[Card]:
    out = []

    cur.execute(f"SELECT * FROM CardUsage ORDER BY {sort} {ascdesc}")
    res = cur.fetchall()
    for row in res:
        out.append(Card(row))

    return out

def cards_by_tag(tag: str, sort: str = "wins", ascdesc: str = "DESC") -> list[Card]:
    out = []

    cur.execute(f"SELECT * FROM CardUsage WHERE tags LIKE '%{tag}%' ORDER BY {sort} {ascdesc}")
    res = cur.fetchall()
    for row in res:
        out.append(Card(row))

    return out

def card_by_id(id: str) -> Card | None:
    cur.execute(f"SELECT * FROM CardUsage WHERE card_id = {id}")
    res = cur.fetchall()
    for row in res:
        return Card(row)

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
def cards_tag(tag):
    out = []
    if tag == "All" or tag == "all":
        out = all_cards()
    else:
        out = cards_by_tag(tag)
    return json.dumps(out, default=vars)

@app.route("/cards/<tag>/sortby/<sort>/<ascdesc>")
def cards_tag_sort(tag, sort, ascdesc):
    direction = "DESC"
    if ascdesc == "ASC" or ascdesc == "asc" or ascdesc == "ascending":
        direction = "ASC"
    out = []
    if tag == "All" or tag == "all":
        out = all_cards(sort, direction)
    else:
        out = cards_by_tag(tag, sort, direction)
    return json.dumps(out, default=vars)

@app.route("/cardid/<id>")
def card_id(id):
    return json.dumps(card_by_id(id), default=vars)