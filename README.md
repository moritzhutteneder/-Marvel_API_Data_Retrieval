# Marvel API Data Retrieval and Interaction

## Overview
This project involves interacting with the Marvel Developer Portal to retrieve data about Marvel characters. The data is then stored and made available via a custom-built API. The project is divided into two main parts:

1. **Data Retrieval**: Connect to the Marvel Developer Portal and retrieve specific data about Marvel characters.
2. **API Creation**: Create an API to store and interact with the retrieved data.

## Objectives

### Part 1: Data Retrieval
1. Provide a list of 30 Marvel characters.
2. Retrieve the IDs for all the characters in the list.
3. Retrieve the total number of events available for all characters.
4. Retrieve the total number of series available for all characters.
5. Retrieve the total number of comics available for all characters.
6. Retrieve the price of the most expensive comic that each character was featured in.
7. Store the retrieved data in a pandas DataFrame with the following columns: 
    - Character Name
    - Character ID
    - Total Available Events
    - Total Available Series
    - Total Available Comics
    - Price of the Most Expensive Comic
8. Save the DataFrame to a file called `data.csv`.

### Part 2: API Creation
1. Create an API to interact with the DataFrame generated in Part 1.
2. Implement the following functionalities:
    - Retrieve the whole DataFrame in JSON format.
    - Retrieve information for a single entry or a list of entries identified by either Character Name or Character ID.
    - Add a new character to the existing DataFrame by specifying its characteristics.
    - Add a new character by specifying only the Character ID and filling in the remaining information from Marvel's API.
    - Delete a character or a list of characters by providing either the Character ID or the Character Name.
3. Protect addition and deletion of characters using an OAuth authentication scheme.

## Requirements

The following Python libraries are required to run the code:
- `requests`
- `pandas`
- `Flask`
- `flask-restful`
- `webdriver-manager`
- `selenium`
- `beautifulsoup4`

You can install these dependencies using the following command:

```sh
pip install requests pandas Flask flask-restful webdriver-manager selenium beautifulsoup4
