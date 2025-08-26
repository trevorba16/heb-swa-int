import csv
import random

first_names = [
    "John", "Jane", "Alex", "Emily", "Chris", "Olivia", "Michael", "Sarah", "David", "Linda",
    "Brian", "Sophie", "Daniel", "Laura", "James", "Emma", "Matthew", "Chloe", "Joshua", "Grace"
]
last_names = [
    "Smith", "Doe", "Turner", "Clark", "Martin", "Brown", "Lee", "Kim", "Wilson", "Scott",
    "Adams", "Evans", "Young", "King", "Hall", "Wright", "Green", "Baker", "Harris", "Nelson"
]

bands = [
    {"name": "The Rockers", "year_formed": 2000},
    {"name": "Jazz Masters", "year_formed": 1995},
    {"name": "Pop Stars", "year_formed": 2010},
    {"name": "Classic Ensemble", "year_formed": 1980},
    {"name": "Metal Heads", "year_formed": 2005},
    {"name": "Blues Crew", "year_formed": 1998},
    {"name": "Country Roads", "year_formed": 2003},
    {"name": "Indie Vibes", "year_formed": 2012},
    {"name": "Reggae Roots", "year_formed": 1992},
    {"name": "Electro Beats", "year_formed": 2015}
]

instruments = [
    {"name": "Guitar", "type": "String"},
    {"name": "Drums", "type": "Percussion"},
    {"name": "Bass", "type": "String"},
    {"name": "Keyboard", "type": "Keyboard"},
    {"name": "Violin", "type": "String"},
    {"name": "Trumpet", "type": "Brass"},
    {"name": "Saxophone", "type": "Woodwind"},
    {"name": "Flute", "type": "Woodwind"},
    {"name": "Cello", "type": "String"},
    {"name": "Harp", "type": "String"}
]

# Generate musicians_sample.csv
with open("musicians_sample.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["name", "birth_year", "instrument", "band"])
    for i in range(1750):
        name = random.choice(first_names) + " " + random.choice(last_names)
        birth_year = random.randint(1960, 2005)
        instrument = random.choice(instruments)["name"]
        band = random.choice(bands)["name"]
        writer.writerow([name, birth_year, instrument, band])