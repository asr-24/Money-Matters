from dotenv import load_dotenv
import os
import requests
import getCategoryIDs

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

    payload = {"parent": {"database_id": DATABASE_ID}, "properties": data}

    res = requests.post(create_url, headers=headers, json=payload)
    # print(res.status_code)
    return res

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

    update_data = {"Name": "test 1"}

    print(update_page(page_id, update_data))
 
get_pages()