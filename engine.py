# Progetto basi di dati 2020 - Tema Cinema
# Gruppo: ArceCity
# Membri: Casarotti Giulio, Ferrari Simone, Trolese Gulio

# File: engine.py
# Descrizione: File contenentegli engine, le tabelle, i moduli importati e la classe Utente
#---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---#
# Moduli importati
from flask import Flask, Blueprint, render_template, url_for, redirect, request, session, flash, abort, make_response
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.sql import func, and_, or_, not_
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
import json
from PIL import Image

#---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---#
# Configurazione APP
app = Flask(__name__)

bcrypt = Bcrypt(app)  # inizializzo il bycript della app

# settiamo la secret_key per flask login... settata come consigliato nella documentazione di flask_login
# Configuriamo flask login
app.secret_key = b'f^iz\x05~\x1b\xaat\xf7\x00\xb4Lf7\xa0'
login_manager = LoginManager()
login_manager.init_app(app)
# apriamo l'engine creato in precedenza in fase di creazione del database (file create_database.py)

anonim_engine = create_engine("postgres+psycopg2://anonim:passwordanonim@localhost/progettobd")
clienti_engine = create_engine("postgres+psycopg2://cliente:passwordcliente@localhost/progettobd")
admin_engine = create_engine("postgres+psycopg2://admin:passwordadmin@localhost/progettobd")
manager_engine = create_engine("postgres+psycopg2://manager:passwordmanager@localhost/progettobd")

#---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---#
# prendiamo i metadata dell'engine
meta = MetaData(admin_engine)
meta.reflect()

utenti = meta.tables['utenti']
posti = meta.tables['posti']
proiezioni = meta.tables['proiezioni']
sale = meta.tables['sale']
film = meta.tables['film']
genere_film = meta.tables['genere_film']
genere = meta.tables['genere']
registi = meta.tables['registi']
attori = meta.tables['attori']
persone = meta.tables['persone']

#---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---#
# classe che rappresenta un nostro utente
class Utente(UserMixin):
    def __init__(self, email, password, is_admin, is_manager):  # costruttore
        self.email = email
        self.password = password
        self.is_admin = is_admin
        self.is_manager = is_manager

    def get_id(self):  # metodo che restituisce l'id (in questo caso, la email)
        return self.email
