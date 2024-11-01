import os
import argparse
import requests
from typing import List, Dict

class NotesApi:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.printed_ids = set()

    def get_notes(self) -> List[Dict]:
        """Retrieve all notes."""
        response = requests.get(f"{self.base_url}/notes")
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()

    def create_note(self, title: str, content: str) -> Dict:
        """Create a new note."""
        data = {"title": title, "content": content}
        response = requests.post(f"{self.base_url}/notes/new", json=data)
        response.raise_for_status()
        return response.json()

    def get_note(self, note_id: int) -> Dict:
        """Retrieve a note by ID."""
        response = requests.get(f"{self.base_url}/{note_id}/get")
        response.raise_for_status()
        return response.json()

    def update_note(self, note_id: int, title: str, content: str) -> Dict:
        """Update a note."""
        data = {"title": title, "content": content}
        response = requests.put(f"{self.base_url}/notes/{note_id}/update", json=data)
        response.raise_for_status()
        return response.json()

    def delete_note(self, note_id: int) -> None:
        """Delete a note."""
        response = requests.delete(f"{self.base_url}/notes/{note_id}/delete")
        response.raise_for_status()

    def clear_notes(self):
        response = requests.delete(f"{self.base_url}/notes/clear")
        response.raise_for_status()


def main():
    parser = argparse.ArgumentParser(description="Notes API Command Line Interface")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000", help="Base URL of the API")
    args = parser.parse_args()

    api = NotesApi(args.base_url)

    while True:
        command = input("Enter a command (get, create, get_note, update, delete, clear, exit): ")

        if command == "get":
            notes = api.get_notes()
            for note in notes:
                note_id = note.get("id")
                if note_id not in api.printed_ids:
                    print(f"{note_id}: {note.get('name')}\n\t{note.get('title')}\n\t{note.get('content')}\n{'-' * 20}")
                    api.printed_ids.add(note_id)
        elif command == "create":
            title = input("Enter the title: ")
            content = input("Enter the content: ")
            note = api.create_note(title, content)
            print(f"Note created successfully: {note}")
        elif command == "get_note":
            note_id = int(input("Enter the note ID: "))
            note = api.get_note(note_id)
            print(f"Note: {note}")
        elif command == "update":
            note_id = int(input("Enter the note ID: "))
            title = input("Enter the new title: ")
            content = input("Enter the new content: ")
            note = api.update_note(note_id, title, content)
            print(f"Note updated successfully: {note}")
        elif command == "delete":
            note_id = int(input("Enter the note ID: "))
            api.delete_note(note_id)
            print("Note deleted successfully")
        elif command == "clear":
            api.clear_notes()
            print("All notes cleared successfully")


if __name__ == "__main__":
    main()