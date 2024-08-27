from dotenv import load_dotenv
import os
import requests

load_dotenv()
INTERNAL_INTEGRATION_SECRET = os.getenv("Internal_Integration_Secret")

DATABASE_ID = os.getenv("Database_ID_Categories")

headers = {
    "Authorization": "Bearer " + INTERNAL_INTEGRATION_SECRET,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def get_pages(num_pages=None):

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

    categories_list = []
    for page in results:
        categories_list.append(page['properties']['Name']['title'][0]['text']['content'])

    return categories_list

if __name__ == "__main__":
    print(get_pages())