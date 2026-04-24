"""
Interface do módulo de configurações
"""
import customtkinter as ctk
from tkinter import messagebox


class SettingsView(ctk.CTkToplevel):
    """Janela de configurações"""
    
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        
        # Configurar janela
        self.title("⚙️ Configurações")
        self.geometry("700x600")
        
        # Centralizar
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 700) // 2
        y = (screen_height - 600) // 2
        self.geometry(f"+{x}+{y}")
        
        # Configurar fechamento
        self.protocol("WM_DELETE_WINDOW", self.fechar)
        
        # Aplicar tema
        tema = self.controller.app.config.get("tema", "dark")
        ctk.set_appearance_mode(tema)
        
        self._setup_ui()
        self.carregar_configuracoes()
    
    def _setup_ui(self):
        """Configura a interface"""
        # Frame principal
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        titulo = ctk.CTkLabel(
            self.main_frame,
            text="⚙️ Configurações",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#FF6B8A"
        )
        titulo.pack(pady=(0, 20))
        
        # Frame para as configurações
        config_frame = ctk.CTkScrollableFrame(self.main_frame)
        config_frame.pack(fill="both", expand=True)
        
        # ===== Aparência =====
        self.criar_secao(config_frame, "🎨 Aparência")
        
        # Tema
        tema_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
        tema_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(
            tema_frame,
            text="Tema:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=10)
        
        self.tema_var = ctk.StringVar(value="dark")
        tema_switch = ctk.CTkSwitch(
            tema_frame,
            text="Modo Escuro",
            variable=self.tema_var,
            onvalue="dark",
            offvalue="light",
            command=self.alternar_tema
        )
        tema_switch.pack(side="right", padx=10)
        
        # Separador
        ctk.CTkFrame(config_frame, height=1, fg_color="#3D3D3D").pack(fill="x", pady=10)
        
        # ===== Notificações =====
        self.criar_secao(config_frame, "🔔 Notificações")
        
        # Notificações
        notif_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
        notif_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(
            notif_frame,
            text="Ativar notificações:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=10)
        
        self.notif_var = ctk.BooleanVar(value=True)
        notif_switch = ctk.CTkSwitch(
            notif_frame,
            text="",
            variable=self.notif_var,
            onvalue=True,
            offvalue=False,
            command=self.salvar_notificacoes
        )
        notif_switch.pack(side="right", padx=10)
        
        # Separador
        ctk.CTkFrame(config_frame, height=1, fg_color="#3D3D3D").pack(fill="x", pady=10)
        
        # ===== Backup =====
        self.criar_secao(config_frame, "💾 Backup")
        
        # Backup automático
        backup_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
        backup_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(
            backup_frame,
            text="Backup automático:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=10)
        
        self.backup_var = ctk.BooleanVar(value=False)
        backup_switch = ctk.CTkSwitch(
            backup_frame,
            text="",
            variable=self.backup_var,
            onvalue=True,
            offvalue=False,
            command=self.salvar_backup_auto
        )
        backup_switch.pack(side="right", padx=10)
        
        # Botão backup manual
        ctk.CTkButton(
            config_frame,
            text="📦 Fazer Backup Agora",
            command=self.fazer_backup,
            height=40,
            font=ctk.CTkFont(size=14)
        ).pack(fill="x", pady=10, padx=10)
        
        # Separador
        ctk.CTkFrame(config_frame, height=1, fg_color="#3D3D3D").pack(fill="x", pady=10)
        
        # ===== Dados =====
        self.criar_secao(config_frame, "🗑️ Dados")
        
        # Limpar dados
        ctk.CTkButton(
            config_frame,
            text="⚠️ Limpar Todos os Dados",
            command=self.limpar_dados,
            height=40,
            fg_color="#8B3A3A",
            hover_color="#B04D4D",
            font=ctk.CTkFont(size=14)
        ).pack(fill="x", pady=10, padx=10)
        
        # Separador
        ctk.CTkFrame(config_frame, height=1, fg_color="#3D3D3D").pack(fill="x", pady=10)
        
        # ===== Sobre =====
        self.criar_secao(config_frame, "ℹ️ Sobre")
        
        info_frame = ctk.CTkFrame(config_frame, corner_radius=10)
        info_frame.pack(fill="x", pady=10, padx=10)
        
        ctk.CTkLabel(
            info_frame,
            text="🌸 Meu Cantinho",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#FF6B8A"
        ).pack(pady=(10, 5))
        
        ctk.CTkLabel(
            info_frame,
            text="Versão 1.0.0",
            font=ctk.CTkFont(size=12)
        ).pack()
        
        ctk.CTkLabel(
            info_frame,
            text="Seu espaço pessoal de organização ♡",
            font=ctk.CTkFont(size=12),
            text_color="#808080"
        ).pack(pady=(5, 10))
        
        # Botão fechar
        ctk.CTkButton(
            self.main_frame,
            text="Fechar",
            command=self.fechar,
            height=40,
            font=ctk.CTkFont(size=14)
        ).pack(side="bottom", fill="x", pady=(20, 0))
    
    def criar_secao(self, parent, titulo):
        """Cria uma seção com título"""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", pady=(10, 5))
        
        ctk.CTkLabel(
            frame,
            text=titulo,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#FF6B8A"
        ).pack(anchor="w", padx=10)
    
    def carregar_configuracoes(self):
        """Carrega as configurações atuais"""
        tema = self.controller.get_config("tema", "dark")
        self.tema_var.set(tema)
        
        notificacoes = self.controller.get_config("notificacoes", True)
        self.notif_var.set(notificacoes)
        
        backup_auto = self.controller.get_config("backup_automatico", False)
        self.backup_var.set(backup_auto)
    
    def alternar_tema(self):
        """Alterna o tema da aplicação"""
        novo_tema = self.controller.alternar_tema()
        messagebox.showinfo("Tema", f"Tema alterado para {novo_tema}")
    
    def salvar_notificacoes(self):
        """Salva configuração de notificações"""
        self.controller.set_config("notificacoes", self.notif_var.get())
        messagebox.showinfo("Configurações", "Preferências de notificações salvas!")
    
    def salvar_backup_auto(self):
        """Salva configuração de backup automático"""
        self.controller.set_config("backup_automatico", self.backup_var.get())
        if self.backup_var.get():
            messagebox.showinfo("Backup", "Backup automático ativado!")
    
    def fazer_backup(self):
        """Faz backup manual"""
        if messagebox.askyesno("Backup", "Deseja fazer um backup dos seus dados agora?"):
            if self.controller.fazer_backup():
                messagebox.showinfo("Backup", "Backup realizado com sucesso!")
            else:
                messagebox.showerror("Erro", "Erro ao realizar backup")
    
    def limpar_dados(self):
        """Limpa todos os dados"""
        if messagebox.askyesno("Atenção!", 
                               "Isso irá apagar TODOS os seus dados (notas, diário, finanças, eventos).\n"
                               "As configurações serão mantidas.\n\n"
                               "Tem certeza que deseja continuar?"):
            if messagebox.askyesno("Confirmação Final", 
                                  "Esta ação é irreversível!\n"
                                  "Digite 'LIMPAR' no campo abaixo para confirmar."):
                from tkinter import simpledialog
                confirmacao = simpledialog.askstring("Confirmar", "Digite 'LIMPAR' para confirmar:")
                if confirmacao == "LIMPAR":
                    if self.controller.limpar_dados():
                        messagebox.showinfo("Sucesso", "Dados limpos com sucesso!")
                        self.fechar()
                    else:
                        messagebox.showerror("Erro", "Erro ao limpar dados")
    
    def fechar(self):
        """Fecha a janela"""
        self.controller.fechar()