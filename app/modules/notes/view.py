import tkinter as tk
from tkinter import ttk, messagebox

class NotesView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.setup_ui()
        self.refresh_notes()
    
    def setup_ui(self):
        # Título
        title_label = ttk.Label(self, text="📝 Minhas Notas", font=("Segoe UI", 18, "bold"))
        title_label.pack(pady=10)
        
        # Frame principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Lista de notas
        self.notes_listbox = tk.Listbox(main_frame, height=15)
        self.notes_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.notes_listbox.yview)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.notes_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Frame de conteúdo
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        ttk.Label(content_frame, text="Título:").pack(anchor=tk.W)
        self.title_entry = ttk.Entry(content_frame, width=40)
        self.title_entry.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(content_frame, text="Conteúdo:").pack(anchor=tk.W)
        self.content_text = tk.Text(content_frame, height=10, width=50)
        self.content_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Botões
        button_frame = ttk.Frame(content_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Nova Nota", command=self.new_note).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Salvar", command=self.save_note).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Excluir", command=self.delete_note).pack(side=tk.LEFT, padx=5)
        
        self.notes_listbox.bind("<<ListboxSelect>>", self.on_note_select)
    
    def refresh_notes(self):
        self.notes_listbox.delete(0, tk.END)
        for note in self.controller.get_all_notes():
            self.notes_listbox.insert(tk.END, f"{note.title} - {note.updated_at.strftime('%d/%m/%Y')}")
    
    def new_note(self):
        self.title_entry.delete(0, tk.END)
        self.content_text.delete(1.0, tk.END)
        self.current_note_id = None
    
    def save_note(self):
        title = self.title_entry.get().strip()
        content = self.content_text.get(1.0, tk.END).strip()
        
        if not title:
            messagebox.showerror("Erro", "Digite um título!")
            return
        
        if hasattr(self, 'current_note_id') and self.current_note_id:
            self.controller.update_note(self.current_note_id, title, content, "Geral")
        else:
            self.controller.add_note(title, content, "Geral")
        
        self.refresh_notes()
        self.new_note()
    
    def delete_note(self):
        if hasattr(self, 'current_note_id') and self.current_note_id:
            if messagebox.askyesno("Confirmar", "Excluir esta nota?"):
                self.controller.delete_note(self.current_note_id)
                self.refresh_notes()
                self.new_note()
    
    def on_note_select(self, event):
        selection = self.notes_listbox.curselection()
        if selection:
            notes = self.controller.get_all_notes()
            note = notes[selection[0]]
            self.current_note_id = note.id
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, note.title)
            self.content_text.delete(1.0, tk.END)
            self.content_text.insert(1.0, note.content)