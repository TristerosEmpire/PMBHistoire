#! /usr/bin/python3
# -*- coding:b utf-8 -*-
import tkinter as tk
import tkinter.messagebox as msgbox
import tkinter.ttk as ttk
import PMB_param
import PMB_search as search


class App(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        # Création d'un ojet StringVar pour l'Entry txtSearch
        self.strCodebarre = tk.StringVar()
        # Création d'un objet StringVar pour le retour de la requête
        self.lstResultQuery = tk.StringVar()
        # Création d'un objet de connexion à la base de données avec ID
        # par défaut
        self.cnx_id = search.ID()
        # self.cnx = search.Connexion(search.ID())
        self.master.title("PMB : historique")
        self.architecture(self.master)

    def architecture(self, master):
        btnSearch = ttk.Button(master, text="Recherche",
                               command=self.searchCodebarre)
        btnParam = ttk.Button(master, text="Paramètres", command=self.param)
        btnDel = ttk.Button(master, text="Effacer", command=self.clear)
        btnQuit = ttk.Button(master, text="Quitter", command=master.destroy)
        self.txtSearch = ttk.Entry(master, textvariable=self.strCodebarre)
        self.txtSearch.bind("<Return>", self.searchCodebarreEvent)
        self.lstResult = tk.Listbox(master, height=15, width=35,
                                    listvariable=self.lstResultQuery)
        # Mise en place des éléments
        self.txtSearch.grid(row=0, column=0, columnspan=2)
        btnSearch.grid(row=0, column=2)
        self.lstResult.grid(row=1, column=0, columnspan=3)
        btnParam.grid(row=2, column=0)
        btnDel.grid(row=2, column=1)
        btnQuit.grid(row=2, column=2)

    def clear(self):
        """Efface la liste des résultats et place le focus sur la zone de texte.
        """
        self.lstResult.delete(0, tk.END)
        self.txtSearch.focus_set()

    def param(self):
        """Affiche la boite de dialogue de paramétrage de la connexion."""
        root = tk.Toplevel()
        self.new_ID = PMB_param.ParamGui(root)
        root.mainloop()

    def searchCodebarreEvent(self, event):
        """Gestion de l'événement quand il y a appui sur la touche Entrée
        simulée par le scan.
        """
        self.searchCodebarre()

    def searchCodebarre(self):
        """Méthode de recherche de code barres :

        Suppression du contenu de la Listbox à chaque appel de cette méthode
        Vérifie que la zone de texte n'est pas vide.
        """
        self.clear()
        # variable stockant le retour de la recherche réinitialisée.
        self.rslt = ""
        try:
            self.cnx = search.Connexion()
            if (len(self.strCodebarre.get()) != 0):
                self.rslt = self.cnx.checkCodebarre(self.strCodebarre.get())
                if len(self.rslt) == 0:
                    self.rslt = "Aucune\ donnée."
                self.lstResultQuery.set(self.rslt)
            else:
                msgbox.showwarning("Attention", "Zone de recherche vide.")
            self.cnx.arret()
        except:
            msgbox.showwarning("Connexion", "Impossible de se connecter avec \
            la base : base activée ? paramètres corrects ?")
        # suppression du texte dans l'Entry
        self.strCodebarre.set("")
        # le focus redirigé sur l'Entry
        self.txtSearch.focus_set()


a = App(master=tk.Tk())
a.mainloop()
