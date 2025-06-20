import requests

def search_google_books(query):
    response = requests.get("https://www.googleapis.com/books/v1/volumes", params={"q": query})
    return response.json()

def get_book_by_id(google_id):
    response = requests.get(f"https://www.googleapis.com/books/v1/volumes/{google_id}")
    if response.status_code == 200:
        return response.json()
    return None
