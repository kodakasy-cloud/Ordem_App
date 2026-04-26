from typing import List, Optional
from app.services.storage import StorageService
from app.utils.helpers import generate_id
from .model import Note

class NotesController:
    def __init__(self, storage_service: StorageService):
        self.storage = storage_service
        self.notes: List[Note] = []
        self.load_notes()
    
    def load_notes(self):
        data = self.storage.load_notes()
        self.notes = [Note.from_dict(note_data) for note_data in data.get('notes', [])]
    
    def save_notes(self):
        notes_data = [note.to_dict() for note in self.notes]
        self.storage.save_notes({'notes': notes_data})
    
    def add_note(self, title: str, content: str, category: str = "Geral") -> Note:
        note = Note(
            id=generate_id(title),
            title=title,
            content=content,
            category=category
        )
        self.notes.append(note)
        self.save_notes()
        return note
    
    def update_note(self, note_id: str, title: str, content: str, category: str) -> bool:
        for note in self.notes:
            if note.id == note_id:
                note.title = title
                note.content = content
                note.category = category
                note.updated_at = datetime.now()
                self.save_notes()
                return True
        return False
    
    def delete_note(self, note_id: str) -> bool:
        initial_len = len(self.notes)
        self.notes = [n for n in self.notes if n.id != note_id]
        if len(self.notes) < initial_len:
            self.save_notes()
            return True
        return False
    
    def get_all_notes(self) -> List[Note]:
        return sorted(self.notes, key=lambda x: x.updated_at, reverse=True)
    
    def get_note_by_id(self, note_id: str) -> Optional[Note]:
        for note in self.notes:
            if note.id == note_id:
                return note
        return None