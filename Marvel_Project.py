"""
Marvel Data Retrieval and API Project
Created on Thu Oct  5 14:27:01 2023
"""

import hashlib as hl
import requests
import time
import pandas as pd
from flask import Flask, request
from flask_restful import Api, Resource

# -----------------------------------------------------------------------------------------
# Marvel API Data Retrieval
# -----------------------------------------------------------------------------------------

# Variables needed for calling the Marvel API
publicKey = 'your_public_key_here'
privateKey = 'your_private_key_here'
ts = str(int(time.time()))

# Create string for hashing
hashString = ts + privateKey + publicKey

# Encode the string with hashlib library
encodedString = hl.md5(hashString.encode())

# Create hexadecimal equivalent encoded string of encoded string
hash = encodedString.hexdigest()

# Function to extract a list of 30 Marvel characters
def extractCharacters() -> list:
    urlCharacters = 'http://gateway.marvel.com/v1/public/characters'
    paramsCharacters = {
        'limit': '30',
        'ts': ts,
        'apikey': publicKey,
        'hash': hash
    }
    responseCharacters = requests.get(urlCharacters, params=paramsCharacters)
    if responseCharacters.status_code == 200:
        return responseCharacters.json().get('data').get('results')
    else:
        print('Error: Unable to fetch data from the API. Status code:', responseCharacters.status_code)
        return []

# Function to extract character names
def extractCharacterNames(characters: list) -> list:
    return [character['name'] for character in characters]

# Function to retrieve the IDs for all characters
def retrieveIds(characters: list) -> list:
    return [str(character['id']) for character in characters]

# Function to retrieve the total number of events available for all characters
def getNumberOfEvents(characters: list) -> int:
    return sum(character['events']['available'] for character in characters)

# Function to retrieve the number of events per character
def getNumberOfEventCharacter(characters: list) -> list:
    return [character['events']['available'] for character in characters]

# Function to retrieve the total number of series available for all characters
def getNumberOfTotalSeries(characters: list) -> int:
    return sum(character['series']['available'] for character in characters)

# Function to retrieve the number of series per character
def getNumberOfSeriesCharacter(characters: list) -> list:
    return [character['series']['available'] for character in characters]

# Function to retrieve the total number of comics available for all characters
def getNumberOfComics(characters: list) -> int:
    return sum(character['comics']['available'] for character in characters)

# Function to retrieve the number of comics per character
def getNumberOfComicsCharacter(characters: list) -> list:
    return [character['comics']['available'] for character in characters]

# Function to retrieve the price of the most expensive comic per character
def getMostExpensiveComics(characters: list) -> list:
    responsePriceComics = []
    for character in characters:
        offset = 0
        maxCharacterPrice = 0
        comicsFound = False
        while True:
            paramsComics = {
                'limit': 100,
                'offset': offset,
                'ts': ts,
                'apikey': publicKey,
                'hash': hash
            }
            response = requests.get(f'http://gateway.marvel.com/v1/public/characters/{character}/comics', params=paramsComics)
            if response.status_code == 200:
                response = response.json()
                if response['data']['results']:
                    comicsFound = True
                    for comic in response['data']['results']:
                        price = comic['prices'][0]['price']
                        if float(price) > maxCharacterPrice:
                            maxCharacterPrice = float(price)
                else:
                    break
            else:
                print('Error: Unable to fetch data from the API. Status code:', response.status_code)
                break
            offset += 100
        responsePriceComics.append(maxCharacterPrice if comicsFound else None)
    return responsePriceComics

# Execute the following code to retrieve Marvel character data
characters = extractCharacters()
characterNames = extractCharacterNames(characters)
listOfIds = retrieveIds(characters)
numberEventsCharacter = getNumberOfEventCharacter(characters)
numberOfSeriesCharacter = getNumberOfSeriesCharacter(characters)
numberComicsCharacter = getNumberOfComicsCharacter(characters)
pricesComics = getMostExpensiveComics(listOfIds)

# Create a DataFrame with the retrieved data
charactersInformation = {
    'Character Name': characterNames,
    'Character ID': listOfIds,
    'Total Available Events': numberEventsCharacter,
    'Total Available Series': numberOfSeriesCharacter,
    'Total Available Comics': numberComicsCharacter,
    'Price of the Most Expensive Comic': pricesComics
}
df = pd.DataFrame(charactersInformation)
df = df.replace(0, None)
df.to_csv('data.csv', index=False)

# -----------------------------------------------------------------------------------------
# API Creation
# -----------------------------------------------------------------------------------------

app = Flask(__name__)
api = Api(app)

# Load data from the local CSV
df = pd.read_csv('data.csv')

class Characters(Resource):
    def get(self):
        characterName = request.args.get('name')
        characterId = request.args.get('id')

        if not characterName and not characterId:
            data = df.to_dict(orient='records')
            return {'status': 200, 'response': data}, 200

        if characterName:
            filteredDf = df[df['Character Name'] == characterName]
        elif characterId:
            filteredDf = df[df['Character ID'] == int(characterId)]

        if filteredDf.empty:
            return {'message': 'No data found for the specified character name or ID'}, 404
        data = filteredDf.to_dict(orient='records')
        return {'status': 200, 'response': data}, 200

api.add_resource(Characters, '/characters', endpoint='characters')

if __name__ == '__main__':
    app.run(debug=True)
