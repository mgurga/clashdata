import json

def test_all_cards(client):
    res = client.get("/allcards")
    resjson = json.loads(res.data)
    print(resjson)
    assert len(resjson) == 102

def test_sort_asc(client):
    res = client.get("/cards/All/sortby/cost/ASC")
    resjson = json.loads(res.data)
    print(resjson)
    assert resjson[0]["cost"] == 0

def test_sort_desc(client):
    res = client.get("/cards/All/sortby/cost/DESC")
    resjson = json.loads(res.data)
    print(resjson)
    assert resjson[0]["cost"] == 9