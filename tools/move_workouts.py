# Make a python script that uses the notion sdk to communicate with the Notion API to search a database for all items with the property "Completed" set to false and then updates the value of the "Date" property in that item to the saved date plus 5 days

import os
import json
from notion_client import Client
from datetime import datetime, timedelta

# Function to load secrets from a JSON file
def load_secrets(secrets_file):
    with open(secrets_file) as f:
        return json.load(f)

# Load secrets
secrets = load_secrets('secrets.json')
notion_api_key = secrets.get('NOTION_API_KEY')

# Initialize the Notion client with the API key from the secrets file
notion = Client(auth=notion_api_key)

# Define the database ID
DATABASE_ID = secrets.get('WORKOUTS_DB')  # Workouts database

# Function to add days to a given date
def add_days_to_date(date_str, days):
    date_obj = datetime.fromisoformat(date_str)
    new_date_obj = date_obj + timedelta(days=days)
    if 'T' in date_str:
        return new_date_obj.isoformat()
    else:
        return new_date_obj.date().isoformat()

# Query the database to find all items with "Completed" set to false and "Date" without time
def query_database():
    response = notion.databases.query(
        **{
            "database_id": DATABASE_ID,
            "filter": {
                "and": [
                    {
                        "property": "Completed",
                        "checkbox": {
                            "equals": False
                        }
                    },
                    {
                        "property": "Date",
                        "date": {
                            "is_not_empty": True
                        }
                    }
                ]
            }
        }
    )
    # Filter out items where the date includes a time
    results = []
    for item in response['results']:
        date_property = item['properties'].get('Date', {})
        if date_property and date_property['date'] and date_property['date']['start']:
            date_str = date_property['date']['start']
            # Check if the date string contains a time component
            if '+02:00' not in date_str:
                results.append(item)
    return results

# Update the "Date" property for a specific page
def update_page_date(page_id, new_date):
    notion.pages.update(
        page_id=page_id,
        properties={
            "Date": {
                "date": {
                    "start": new_date
                }
            }
        }
    )

# Retrieve all databases the token has access to
def get_all_databases():
    response = notion.search(
        **{
            "filter": {
                "property": "object",
                "value": "database"
            }
        }
    )
    return response['results']

# Main function
def main():
    # Retrieve and print all databases
    databases = get_all_databases()
    print("Databases accessible by the token:")
    for db in databases:
        print(f"ID: {db['id']}, Title: {db['title'][0]['text']['content']}")

    items = query_database()
    
    for item in items:
        page_id = item['id']
        page_name = item['properties']['Name']['title'][0]['text']['content']
        date_property = item['properties'].get('Date', {})
        
        if 'Saiyan' in page_name:
            original_date = date_property['date']['start']
            new_date = add_days_to_date(original_date, 3)
            print(f"Update page {page_name} {page_id} date from {original_date} to {new_date}")

            # UNCOMMENT TO MODIFY DATABASE
            update_page_date(page_id, new_date)

if __name__ == "__main__":
    main()
