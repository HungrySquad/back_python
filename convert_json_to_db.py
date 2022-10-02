"""
Simple 1-time use script to convert json to db
"""
import json
import sqlite3


connection = sqlite3.connect('recipies.db')
cursor = connection.cursor()
cursor.execute("""CREATE TABLE post (
	id INTEGER PRIMARY KEY AUTOINCREMENT,  
	name VARCHAR(50), 
	ingredients VARCHAR(3000), 
	image VARCHAR(255), 
	time VARCHAR(255), 
	description VARCHAR(3000), 
	source VARCHAR(255), 
	nutrients VARCHAR(255), 
	instructions VARCHAR(4000), 
	servings VARCHAR(255)
)""")
with open('data_test.json', encoding="utf-8") as f:
    traffic = json.load(f)
    columns = [
        'name',
        'ingredients',
        'img_url',
        'time_values',
        'description',
        'url',
        'nutritions',
        'instructions',
        'servings',
    ]

    COUNTER = 0
    for r in traffic:
        r["id"] = COUNTER
        COUNTER += 1
        cursor.execute(
            "insert into post values(:id, :name, :ingredients, :img_url, :time_values, :description, :url, :nutritions, :instructions, :servings)",  # pylint: disable=line-too-long
            r,
        )

    connection.commit()
    connection.close()
