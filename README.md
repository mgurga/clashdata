# clashdata
Clash Royale deck builder based on 37.9 million season 18 battles.

# How to run
1. Install Python 3, PySpark >= 3.5.0, mysql-connector-python, java 17, and Flask
2. Enter database directory
3. Setup mysql on localhost
4. Download BattlesStaging_01012021_WL_tagged.csv and CardMasterListSeason18_12082020.csv from [Kaggle](https://www.kaggle.com/datasets/bwandowando/clash-royale-season-18-dec-0320-dataset/data)
5. Rename BattlesStaging_01012021_WL_tagged.csv to battles_Jan01_21.csv and CardMasterListSeason18_12082020.csv to cards.csv
6. Run card_usage.py
7. Return to project directory
8. Run ```flask run```

# Credits
- Game assets from [Supercell Fankit](https://fankit.supercell.com/d/BmehSDJrZNff/game-assets-1?)
- Formatted card graphics from [cr-cardgen](https://github.com/smlbiobot/cr-cardgen/)