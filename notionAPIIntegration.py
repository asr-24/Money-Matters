from dotenv import load_dotenv
import os
import requests
import getCategoryIDs
import json

load_dotenv()
INTERNAL_INTEGRATION_SECRET = os.getenv("Internal_Integration_Secret")

DATABASE_ID = os.getenv("Database_ID")

headers = {
    "Authorization": "Bearer " + INTERNAL_INTEGRATION_SECRET,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def update_page(page_id: str, data: dict):
    url = f"https://api.notion.com/v1/pages/{page_id}"

    payload = {"properties": data}

    res = requests.patch(url, json=payload, headers=headers)
    return res

def create_page(data: dict):
    create_url = "https://api.notion.com/v1/pages"

    new_page_data = {
    "parent": {
        "database_id": DATABASE_ID
    },
    "properties": {
        "Name": {
            "title": [
                {
                    "text": {
                        "content": "New Page Title"
                    }
                }
            ]
        },
        "Amount": {
            "number": 1234  # Example number property
        },
        "Date": {
            "date": {
                "start": "2024-08-27"  # Example date property
            }}}}

    # Make the POST request to create a new page
    response = requests.post("https://api.notion.com/v1/pages", headers=headers, data=json.dumps(new_page_data))

    # Check the response
    if response.status_code == 200:
        print("Page created successfully!")
        print(response.json())  # Print the created page details
    else:
        print(f"Failed to create page. Status code: {response.status_code}")
        print(response.text)

def get_pages(num_pages=None):
    """
    If num_pages is None, get all pages, otherwise just the defined number.
    """
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

    get_all = num_pages is None
    page_size = 100 if get_all else num_pages

    payload = {"page_size": page_size}
    response = requests.post(url, json=payload, headers=headers)

    data = response.json()

    results = data["results"]
    while data["has_more"] and get_all:
        payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
        url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        results.extend(data["results"])

    # return results

    page = results[0]
    page_id = page['id']
    # name = page['properties']['Name']['title'][0]['text']['content']
    # amount = page['properties']['Amount']['number']
    # category_relation_id = page['properties']['Category']['relation'][0]['id']

    # print(page_id, name, amount, category_relation_id)
 
# get_pages()

create_page({
    "parent": {
        "database_id": DATABASE_ID
    },
    "properties": {
        "Name": {
            "title": [
                {
                    "text": {
                        "content": "New Page Title"
                    }
                }
            ]
        },
        "Amount": {
            "number": 1234  # Example number property
        },
        "Date": {
            "date": {
                "start": "2024-08-27"  # Example date property
            }}}}
)