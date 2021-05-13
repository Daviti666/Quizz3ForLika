import requests
import json
import sqlite3

#ავირჩიე კოვიდის სტატისტიკები
url = "https://covid-19-coronavirus-statistics.p.rapidapi.com/v1/stats"

querystring = {"country":"Georgia"}

headers = {
    'x-rapidapi-key': "a44b27c16amshac083d44c6fb560p1331c7jsn7e57ad3a5f74",
    'x-rapidapi-host': "covid-19-coronavirus-statistics.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

#დავალება 1

print(response.text)
print(response.status_code)
print(response.headers)
print("API Content Type: ", response.headers['Content-Type'])

#დავალება 2

res = response.json()
print(json.dumps(res, indent=5))

with open('CovidAPI.json', 'w') as file:
    json.dump(res, file, indent=4)

#დავალება 3
#შევქმენი დატა, რომელშიც კოდს შეაქვს საქართველოს სტატისტიკა, როგორიცაა: ქვეყნის სახელი, მომხდარი შემთხვევები, გარდაცვლილთა რაოდენობა და გამოჯანმრთელებულთა რაოდენობა

print("კოვიდის ყველა შემთხვევა საქართველოში: ", res['data']['covid19Stats'][0]['confirmed'])
print("გარდაცვლილთა რაოდენობა: ", res['data']['covid19Stats'][0]['deaths'])
print("გამოჯანმრთელებულთა რაოდენობა: ", res['data']['covid19Stats'][0]['recovered'])

#დავალება 4

rows = []

country = res['data']['covid19Stats'][0]['country']
confirmed = res['data']['covid19Stats'][0]['confirmed']
deaths = res['data']['covid19Stats'][0]['deaths']
recovered = res['data']['covid19Stats'][0]['recovered']


row = (country, confirmed, deaths, recovered)
rows.append(row)

print(rows)

connect = sqlite3.connect('CovidGeo.sqlite')
cursor = connect.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS GeorgiaStats
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            country TEXT,
            confirmed INTEGER,
            deaths INTEGER,
            recovered INTEGER
            )''')

connect.executemany('''INSERT INTO GeorgiaStats (country, confirmed, deaths, recovered) VALUES (?, ?, ?, ?)''', rows)

connect.commit()
connect.close()