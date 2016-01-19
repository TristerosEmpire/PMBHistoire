#!/usr/bin/python3
# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.messagebox as msgbox
import tkinter.ttk as ttk
import mysql.connector as mysql
import json
import PMB_search
import os.path


class ParamGui():

    """Paramètres : connexion.

    - demande un objet ID que l'on va manipuler et tester.
    """

    def __init__(self, master_p=None):
        """Initialisation des paramètres de connexion."""
        self.connexion = PMB_search.ID.config
        master_p.title("Paramètres")

        # Création des objets stockant les valeurs chaines
        self.strUser = tk.StringVar()
        self.strUser.set(self.connexion['user'])
        self.strPasswd = tk.StringVar()
        self.strPasswd.set(self.connexion['password'])
        self.strDbName = tk.StringVar()
        self.strDbName.set(self.connexion['database'])
        self.strSite = tk.StringVar()
        self.strSite.set(self.connexion['host'])
        # création de l'interface graphique
        self.architecture(master_p)

    def architecture(self, master):
        """Définit l'architecture de l'interface utilisateur."""
        # Labels
        lblUser = tk.Label(master, text="Nom")
        lblPasswd = tk.Label(master, text="Mot de Passe")
        lblDbName = tk.Label(master, text="Base")
        lblSite = tk.Label(master, text="Adr. serveur")
        # Entries
        self.txtUser = tk.Entry(master, textvariable=self.strUser)
        self.txtPasswd = tk.Entry(
            master, textvariable=self.strPasswd, show='*')
        self.txtDbName = tk.Entry(master, textvariable=self.strDbName)
        self.txtSite = tk.Entry(master, textvariable=self.strSite)
        # Boutons
        btnTest = ttk.Button(master, text="Connexion ?", command=self.test)
        btnRec = ttk.Button(master, text="Enregistrement",
                            command=self.enregistre)
        btnQuit = ttk.Button(master, text="Fermer", command=master.destroy)

        # Disposition
        # Labels
        lblUser.grid(row=0, column=0)
        lblPasswd.grid(row=1, column=0)
        lblDbName.grid(row=2, column=0)
        lblSite.grid(row=3, column=0)
        # Entries
        self.txtUser.grid(row=0, column=1, columnspan=3, sticky="e,w")
        self.txtPasswd.grid(row=1, column=1, columnspan=3, sticky="e,w")
        self.txtDbName.grid(row=2, column=1, columnspan=3, sticky="e,w")
        self.txtSite.grid(row=3, column=1, columnspan=3, sticky="e,w")
        # Boutons
        btnTest.grid(row=4, column=0)
        btnRec.grid(row=4, column=1)
        btnQuit.grid(row=4, column=2)

        self.current_config = None

    def test(self):
        """test : teste la connexion.

        Ce test est effectué non depuis l'objet passé à l'initialisation
        mais depuis les zones de texte.

        Comportement : affiche un messagebox.
        """
        msg = None
        self.lectureChamps()
        try:
            test_connexion = mysql.connect(**self.current_config)
            msg = "Connexion réussie."
            # enregistrement en mémoire de la configuration
            PMB_search.ID.config = self.current_config
            test_connexion.close()
        except:
            msg = "Aucune connexion. Paramètres erronés."
        msgbox.showinfo(title="information", message=msg)

    def enregistre(self):
        """Enregistre les données en mémoire et sur le JSON."""
        self.lectureChamps()
        # écrase la config actuelle en mémoire :
        PMB_search.ID.config = self.current_config
        # écrase le json
        if os.path.isfile("config.json"):
            action = 'w'
        else:
            action = 'x'
        f = open("config.json", action)
        f.write(json.dumps(self.current_config))
        f.close()

    def lectureChamps(self):
        """Effectue la lecture des champs du formulaire."""
        self.current_config = {
            'user': self.strUser.get(),
            'password': self.strPasswd.get(),
            'host': self.strSite.get(),
            'database': self.strDbName.get()
        }
