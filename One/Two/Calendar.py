# One/Two/Calendar.py
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, date
import calendar

class CalendarModule:
    def __init__(self, parent):
        self.parent = parent
        self.janela = None
    
    def abrir(self):
        """Abre o módulo de calendário"""
        if self.janela and self.janela.winfo_exists():
            self.janela.lift()
            return
        
        self.parent.atualizar_status("Abrindo Calendário...")
        
        self.janela = tk.Toplevel(self.parent.root)
        self.janela.title("📅 Calendário")
        self.janela.geometry("600x550")
        self.janela.configure(bg='#ecf0f1')
        
        frame = tk.Frame(self.janela, bg='#ecf0f1', padx=20, pady=20)
        frame.pack(fill='both', expand=True)
        
        # Ano e mês atuais
        ano_atual = date.today().year
        mes_atual = date.today().month
        
        # Variáveis
        self.ano_var = tk.IntVar(value=ano_atual)
        self.mes_var = tk.IntVar(value=mes_atual)
        
        # Frame de navegação
        nav_frame = tk.Frame(frame, bg='#ecf0f1')
        nav_frame.pack(pady=10)
        
        tk.Button(nav_frame, text="◀", command=self.mudar_mes_anterior,
                 font=('Arial', 14), bg='#3498db', fg='white').pack(side='left', padx=5)
        tk.Button(nav_frame, text="▶", command=self.mudar_proximo_mes,
                 font=('Arial', 14), bg='#3498db', fg='white').pack(side='left', padx=5)
        
        # Frame do calendário
        self.frame_calendario = tk.Frame(frame, bg='white', relief=tk.RAISED, borderwidth=2)
        self.frame_calendario.pack(pady=10, fill='both', expand=True)
        
        # Eventos
        tk.Label(frame, text="Eventos do dia:", bg='#ecf0f1', 
                font=('Arial', 10, 'bold')).pack(anchor='w', pady=(10,0))
        
        self.txt_evento = tk.Text(frame, height=5, width=50, font=('Arial', 10))
        self.txt_evento.pack(pady=5, fill='x')
        
        btn_frame = tk.Frame(frame, bg='#ecf0f1')
        btn_frame.pack(pady=5)
        
        tk.Button(btn_frame, text="Salvar Evento", command=self.salvar_evento,
                 bg='#2ecc71', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Fechar", command=self.fechar,
                 bg='#e74c3c', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        
        self.atualizar_calendario()
    
    def mudar_mes_anterior(self):
        """Muda para o mês anterior"""
        novo_mes = self.mes_var.get() - 1
        novo_ano = self.ano_var.get()
        
        if novo_mes < 1:
            novo_mes = 12
            novo_ano -= 1
        
        self.mes_var.set(novo_mes)
        self.ano_var.set(novo_ano)
        self.atualizar_calendario()
    
    def mudar_proximo_mes(self):
        """Muda para o próximo mês"""
        novo_mes = self.mes_var.get() + 1
        novo_ano = self.ano_var.get()
        
        if novo_mes > 12:
            novo_mes = 1
            novo_ano += 1
        
        self.mes_var.set(novo_mes)
        self.ano_var.set(novo_ano)
        self.atualizar_calendario()
    
    def atualizar_calendario(self):
        """Atualiza a exibição do calendário"""
        # Limpar frame
        for widget in self.frame_calendario.winfo_children():
            widget.destroy()
        
        ano = self.ano_var.get()
        mes = self.mes_var.get()
        
        # Título
        titulo = tk.Label(self.frame_calendario, text=f"{calendar.month_name[mes]} {ano}",
                         font=('Arial', 16, 'bold'), bg='white')
        titulo.pack(pady=10)
        
        # Dias da semana
        dias_frame = tk.Frame(self.frame_calendario, bg='white')
        dias_frame.pack()
        
        dias_semana = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
        for dia in dias_semana:
            tk.Label(dias_frame, text=dia, width=8, height=2,
                    font=('Arial', 10, 'bold'), bg='#3498db', fg='white',
                    relief=tk.RAISED).pack(side='left', padx=1)
        
        # Dias do mês
        cal = calendar.monthcalendar(ano, mes)
        for semana in cal:
            semana_frame = tk.Frame(self.frame_calendario, bg='white')
            semana_frame.pack()
            for dia in semana:
                if dia == 0:
                    tk.Label(semana_frame, text="", width=8, height=2,
                            bg='white', relief=tk.RAISED).pack(side='left', padx=1)
                else:
                    cor = '#e74c3c' if (dia == date.today().day and 
                                       mes == date.today().month and 
                                       ano == date.today().year) else '#ecf0f1'
                    tk.Label(semana_frame, text=str(dia), width=8, height=2,
                            bg=cor, relief=tk.RAISED, cursor='hand2').pack(side='left', padx=1)
    
    def salvar_evento(self):
        """Salva um evento"""
        evento = self.txt_evento.get("1.0", tk.END).strip()
        if evento:
            self.parent.atualizar_status(f"Evento salvo: {evento[:50]}...")
            messagebox.showinfo("Sucesso", "Evento salvo!")
            self.txt_evento.delete("1.0", tk.END)
        else:
            messagebox.showwarning("Aviso", "Digite um evento primeiro!")
    
    def fechar(self):
        """Fecha a janela"""
        if self.janela:
            self.janela.destroy()
            self.janela = None