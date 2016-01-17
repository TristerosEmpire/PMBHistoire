#!/usr/bin/python3
# -*- coding: utf-8 -*-
from mysql.connector import *
import os.path
import json


class ID:
    """
    Gestion des identifiants pour une connexion à MySQL
    - propriété de classe : config (à privilégier)
    - propriétés d'instance : database, user, password et host
    """
    config = {
        'user': '',
        'password': '',
        'host': '',
        'database': ''
    }

    def __init__(self, database='bibli', user='root',
                 password='', host='127.0.0.1'):
        if os.path.isfile("config.json"):
            self.lecture = open("config.json", 'r')
            self.io = self.lecture.readline()
            self.lecture.close()
            ID.config = json.loads(self.io)
        else:
            self.database = database
            self.user = user
            self.password = password
            self.host = host
            # more efficient
            ID.config['user'] = self.user
            ID.config['database'] = self.database
            ID.config['password'] = self.password
            ID.config['host'] = self.host

    def __str__(self):
        return "Paramètres de connexion :\n\t- user = " +\
            self.user + "\n\t- database = " + self.database + "\n" +\
            "\t- host = " + self.host


class Connexion:
    """
    Gestion de la connexion à la base de données
    """

    def __init__(self):
        # connexion_id.config.
        # self.user = connexion_id.user
        # self.database = connexion_id.database
        # self.password = connexion_id.password
        # self.host = connexion_id.host
        # self.config = connexion_id.config
        # Vérification de la connexion
        self.cnx = self.est_connectee()

    def est_connectee(self):
        """
        La base est-elle bien connectée ?
        """
        try:
            # pas d'utilisation directe du self.config
            self.c = MySQLConnection(**ID.config)
            return True
        except:
            return False
        else:
            self.c.close()

    def arret(self):
        """
        Arrêt de la connexion à la base
        """
        if self.cnx:
            self.c.close()
            self.cnx = False

    # DEBUG : cb ="5369450062"
    def checkCodebarre(self, cb):
        """
        Vérification de l'historique des emprunteurs pour un exemplaire donné
        Argument cd : demande le code-barre de l'exemplaire
        Retour : une chaine de caractères
        """
        self.sql = str("select empr.empr_nom, empr.empr_prenom " +
                       "from empr, pret_archive, exemplaires " +
                       "where empr.id_empr = pret_archive.arc_id_empr " +
                       "and pret_archive.arc_expl_id = exemplaires.expl_id " +
                       "and exemplaires.expl_cb = '" + cb + "'")
        self.resultat = ""
        cursor = self.c.cursor()
        cursor.execute(self.sql)
        for (nom, prenom) in cursor:
            # Faire attention à l'échappement des espaces
            self.resultat += prenom + "\ " + nom + " "
        return self.resultat
        cursor.close()

    def __del__(self):
        """
        On force la déconnexion à la destruction de l'objet
        """
        if self.cnx:
            self.c.close()
            self.cnx = False
