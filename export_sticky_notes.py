import requests
from dotenv import load_dotenv
import os
import re

# Load environment variables from the .env file
load_dotenv()

# Get the API token from the environment variable
API_TOKEN = os.getenv('MIRO_API_TOKEN')
BASE_URL = 'https://api.miro.com/v2'
SUBFOLDER = 'gitrepo'

# Function to get all boards in the workspace
def get_boards():
    url = f'{BASE_URL}/boards'
    headers = {
        'Authorization': f'Bearer {API_TOKEN}'
    }
    boards = []
    while url:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            boards.extend(data['data'])
            links = data['links']
            url = links.get('next')  # Handle pagination
        else:
            print(f'Failed to fetch boards: {response.status_code} {response.text}')
            break
    return boards

# Function to get all sticky notes from a board
def get_sticky_notes(board_id):
    url = f'{BASE_URL}/boards/{board_id}/items'
    headers = {
        'Authorization': f'Bearer {API_TOKEN}'
    }
    sticky_notes = []
    while url:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            widgets = data['data']
            links = data['links']
            # Filter to only sticky notes
            sticky_notes.extend([widget for widget in widgets if widget['type'] == 'sticky_note'])
            url = links.get('next')  # Handle pagination
        else:
            print(f'Failed to fetch items for board {board_id}: {response.status_code} {response.text}')
            break
    return sticky_notes

# Function to export sticky notes
def export_sticky_notes(sticky_notes, folder):
    os.makedirs(f"{SUBFOLDER}", exist_ok=True)
    os.makedirs(f"{SUBFOLDER}/{folder}", exist_ok=True)
    with open(f"{SUBFOLDER}/{folder}/sticky_notes_export.txt", 'a') as file:
        for note in sticky_notes:
            data = note['data']
            if data['content']:
                print(f"'{data}'")
                file.write(f"{note['id']}: {note['data']['content']}\n")

def main():
    all_sticky_notes = []
    boards = get_boards()
    
    for board in boards:
        board_name = board['name']
        match = re.search(r"^(.*?)(?=:)", board_name)
        if match:
            folder = match.group(1).strip()
        else:
            folder = "None"
        print(f"Fetching sticky notes for board: {board_name}, folder {folder}")
        sticky_notes = get_sticky_notes(board['id'])
        export_sticky_notes(sticky_notes, folder)
    
    
    print(f"Exported {len(all_sticky_notes)} sticky notes.")

if __name__ == '__main__':
    main()
