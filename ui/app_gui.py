import customtkinter as ctk
from services.auth_service import AuthService
from services.gestion_conges import GestionConges
from models.constants import StatutConge, TypeConge

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class CongesApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Système de Gestion des Congés")
        self.geometry("700x500") # Légèrement plus grand pour le confort
        
        self.service = GestionConges()
        self.show_login_view()

    def clear_window(self):
        """Nettoie la fenêtre avant de changer de vue."""
        for widget in self.winfo_children():
            widget.destroy()

    # --- VUE : LOGIN ---
    def show_login_view(self):
        self.clear_window()
        
        frame = ctk.CTkFrame(self)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(frame, text="Authentification", font=("Roboto", 24, "bold")).pack(pady=20, padx=40)

        self.entry_matricule = ctk.CTkEntry(frame, placeholder_text="Matricule (ex: E001)", width=200)
        self.entry_matricule.pack(pady=10)

        self.label_error = ctk.CTkLabel(frame, text="", text_color="red")
        self.label_error.pack()

        btn_login = ctk.CTkButton(frame, text="Se connecter", command=self.handle_login)
        btn_login.pack(pady=20)

    def handle_login(self):
        matricule = self.entry_matricule.get()
        if AuthService.login(matricule):
            self.show_dashboard_view()
        else:
            self.label_error.configure(text="Matricule inconnu !")

    # --- VUE : DASHBOARD ---
    def show_dashboard_view(self):
        self.clear_window()
        user = AuthService._utilisateur_connecte
        
        # Header
        header = ctk.CTkFrame(self, height=60)
        header.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(header, text=f"Connecté : {user['prenom']} {user['nom']} ({user['service']})", 
                     font=("Arial", 14, "bold")).pack(side="left", padx=20)
        
        ctk.CTkButton(header, text="Déconnexion", fg_color="indianred", 
                      command=self.handle_logout, width=100).pack(side="right", padx=10)

        # Corps
        content = ctk.CTkFrame(self)
        content.pack(expand=True, fill="both", padx=10, pady=5)

        if AuthService.est_responsable():
            ctk.CTkLabel(content, text="MENU RESPONSABLE RH", font=("Arial", 18, "bold"), text_color="#3a7ebf").pack(pady=20)
            ctk.CTkButton(content, text="Valider les demandes", width=250, command=self.show_validation_view).pack(pady=10)
            ctk.CTkButton(content, text="Gérer les employés", width=250, command=self.show_gestion_employes_view).pack(pady=10)
        else:
            ctk.CTkLabel(content, text="ESPACE EMPLOYÉ", font=("Arial", 18, "bold")).pack(pady=20)
            ctk.CTkLabel(content, text=f"Solde disponible : {user['solde_conges']} jours", font=("Arial", 16)).pack(pady=10)
            ctk.CTkButton(content, text="Poser un congé", width=250, command=self.show_nouvelle_demande_view).pack(pady=10)
            ctk.CTkButton(content, text="Mes demandes", width=250, command=self.show_mes_demandes_view).pack(pady=10)

    # --- VUE : NOUVELLE DEMANDE ---
    def show_nouvelle_demande_view(self):
        self.clear_window()
        ctk.CTkLabel(self, text="Soumettre une demande", font=("Arial", 20, "bold")).pack(pady=20)

        self.date_debut = ctk.CTkEntry(self, placeholder_text="Début (YYYY-MM-DD)")
        self.date_debut.pack(pady=5)

        self.date_fin = ctk.CTkEntry(self, placeholder_text="Fin (YYYY-MM-DD)")
        self.date_fin.pack(pady=5)

        # Utilisation de l'énumération pour les choix
        self.type_conge = ctk.CTkComboBox(self, values=[t.value for t in TypeConge])
        self.type_conge.pack(pady=5)

        ctk.CTkButton(self, text="Envoyer", fg_color="green", command=self.handle_soumettre).pack(pady=20)
        ctk.CTkButton(self, text="Annuler", fg_color="gray", command=self.show_dashboard_view).pack()

    def handle_soumettre(self):
        from models.conge import CongeAnnuel, CongeMaladie, CongeExceptionnel
        
        t = self.type_conge.get()
        u_id = AuthService.get_user_id()
        d_b = self.date_debut.get()
        d_f = self.date_fin.get()

        # Mapping Polymorphe
        mapping = {
            TypeConge.ANNUEL.value: CongeAnnuel,
            TypeConge.MALADIE.value: CongeMaladie,
            TypeConge.EXCEPTIONNEL.value: CongeExceptionnel
        }
        
        demande_obj = mapping[t](u_id, d_b, d_f)
        
        if self.service.soumettre_demande(demande_obj):
            self.show_dashboard_view()

    # --- VUE : VALIDATION (RH) ---
    def show_validation_view(self):
        self.clear_window()
        ctk.CTkLabel(self, text="Demandes à traiter", font=("Arial", 20, "bold")).pack(pady=10)

        demandes = self.service.conge_dao.trouver_par_statut(StatutConge.EN_ATTENTE.value)

        scroll = ctk.CTkScrollableFrame(self, width=600, height=300)
        scroll.pack(pady=10, padx=10)

        for d in demandes:
            emp = self.service.employe_dao.trouver_par_id(d['employe_id'])
            f = ctk.CTkFrame(scroll)
            f.pack(fill="x", pady=2)
            
            txt = f"{emp['nom']} | {d['type_conge']} | {d['date_debut']} au {d['date_fin']}"
            ctk.CTkLabel(f, text=txt, anchor="w").pack(side="left", padx=10)
            
            ctk.CTkButton(f, text="✔", width=40, fg_color="green", 
                          command=lambda i=d['id']: self.handle_decision(i, StatutConge.ACCEPTE.value)).pack(side="right", padx=5)
            ctk.CTkButton(f, text="✘", width=40, fg_color="red", 
                          command=lambda i=d['id']: self.handle_decision(i, StatutConge.REFUSE.value)).pack(side="right", padx=5)

        ctk.CTkButton(self, text="Retour", command=self.show_dashboard_view).pack(pady=10)

    def handle_decision(self, id_demande, decision):
        if self.service.traiter_demande(id_demande, decision):
            self.show_validation_view()

    # --- VUE : MES DEMANDES (EMPLOYÉ) ---
    def show_mes_demandes_view(self):
        self.clear_window()
        ctk.CTkLabel(self, text="Mon Historique", font=("Arial", 20, "bold")).pack(pady=10)

        demandes = self.service.conge_dao.trouver_par_employe(AuthService.get_user_id())
        scroll = ctk.CTkScrollableFrame(self, width=600, height=300)
        scroll.pack(pady=10)

        for d in demandes:
            f = ctk.CTkFrame(scroll)
            f.pack(fill="x", pady=2)
            
            color = "orange" if d['statut'] == StatutConge.EN_ATTENTE.value else "green" if d['statut'] == StatutConge.ACCEPTE.value else "red"
            
            ctk.CTkLabel(f, text=f"{d['date_debut']} - {d['type_conge']}", width=250, anchor="w").pack(side="left", padx=10)
            ctk.CTkLabel(f, text=d['statut'], text_color=color, font=("Arial", 12, "bold")).pack(side="right", padx=10)

        ctk.CTkButton(self, text="Retour", command=self.show_dashboard_view).pack(pady=10)

# --- VUE : GESTION PERSONNEL (RH) ---
    def show_gestion_employes_view(self):
        self.clear_window()
        ctk.CTkLabel(self, text="Gestion des Employés", font=("Arial", 20, "bold")).pack(pady=10)

        # Formulaire simplifié en ligne
        f_add = ctk.CTkFrame(self)
        f_add.pack(fill="x", padx=20, pady=5)
        
        self.e_mat = ctk.CTkEntry(f_add, placeholder_text="Matricule", width=100)
        self.e_mat.grid(row=0, column=0, padx=5, pady=5)
        
        self.e_nom = ctk.CTkEntry(f_add, placeholder_text="Nom", width=100)
        self.e_nom.grid(row=0, column=1, padx=5, pady=5)
        
        self.e_pre = ctk.CTkEntry(f_add, placeholder_text="Prénom", width=100)
        self.e_pre.grid(row=0, column=2, padx=5, pady=5)
        
        # Utilisation de l'Enum ServiceName pour le menu déroulant
        from models.constants import ServiceName
        self.e_service = ctk.CTkComboBox(f_add, values=[s.value for s in ServiceName], width=130)
        self.e_service.grid(row=0, column=3, padx=5, pady=5)
        self.e_service.set(ServiceName.INFORMATIQUE.value) # Valeur par défaut
        
        btn_add = ctk.CTkButton(f_add, text="+ Ajouter", width=80, command=self.handle_ajout_employe)
        btn_add.grid(row=0, column=4, padx=10)

        # Liste des employés
        scroll = ctk.CTkScrollableFrame(self, width=600, height=200)
        scroll.pack(pady=10, fill="both", expand=True)

        for e in self.service.employe_dao.trouver_tout():
            row = ctk.CTkFrame(scroll)
            row.pack(fill="x", pady=2)
            
            # Affichage complet : Matricule - NOM Prénom (Service)
            txt = f"{e['matricule']} - {e['nom'].upper()} {e['prenom']} ({e['service']})"
            ctk.CTkLabel(row, text=txt).pack(side="left", padx=10)
            
            ctk.CTkLabel(row, text=f"Solde: {e['solde_conges']}j", 
                         font=("Arial", 12, "bold"), text_color="#3a7ebf").pack(side="right", padx=10)

        ctk.CTkButton(self, text="Retour", command=self.show_dashboard_view).pack(pady=10)

    def handle_ajout_employe(self):
        from models.employe import Employe
        
        # Création de l'objet avec le service sélectionné dans le ComboBox
        new = Employe(
            matricule=self.e_mat.get(),
            nom=self.e_nom.get(),
            prenom=self.e_pre.get(),
            service=self.e_service.get()
        )
        
        if self.service.employe_dao.ajouter(new):
            # Effacer les champs après ajout réussi
            self.e_mat.delete(0, 'end')
            self.e_nom.delete(0, 'end')
            self.e_pre.delete(0, 'end')
            self.show_gestion_employes_view() # Rafraîchir la liste

    def handle_logout(self):
        AuthService.logout()
        self.show_login_view()

if __name__ == "__main__":
    app = CongesApp()
    app.mainloop()