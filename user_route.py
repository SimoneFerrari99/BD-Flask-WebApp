# Progetto basi di dati 2020 - Tema Cinema
# Gruppo: ArceCity
# Membri: Casarotti Giulio, Ferrari Simone, Trolese Gulio

# File: user_route.py
# Descrizione: File contenente tutte le route accessibili da un utente normale
#---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---#
from flask import Flask, render_template, url_for, redirect, request, session, flash, abort, Blueprint
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.sql import func
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
import json
from PIL import Image
from main_app import *

user_app = Blueprint('user_app', __name__)

#--------------------------------------------------------------------------------------------#
# Registrazione di un nuovo utente
@user_app.route('/registrazione', methods=['GET', 'POST'])
def registrazione():
    if request.method == 'POST':
        # prendiamo i dati dal form
        nome = request.form["nome"]
        cognome = request.form["cognome"]
        data_nascita = str(request.form["data_nascita"])
        email = request.form["email"]
        psw = request.form["psw"]
        conferma = request.form["conferma_password"]

        hashed_psw = bcrypt.generate_password_hash(psw).decode('utf-8')  # cripto la password

        # se le due password non corrispondono
        if(psw != conferma):
            return render_template('registrazione.html', errore=True)
        else:
            # prendiamo la tabella utenti dal metadata tramite reflection
            utenti = meta.tables['utenti']  # prendo la tabella
            ins = utenti.insert()  # prendo la insert
            values = {  # dizionario per i valori
                'nome': nome,
                'cognome': cognome,
                'data_nascita': data_nascita,
                'email': email,
                'password': hashed_psw,
                'is_admin': False,
                'saldo': 0.0
            }
            conn = anonim_engine.connect()  # mi connetto
            conn.execute(ins, values)  # eseguo l'inserimento con i valori
            conn.close()
            return redirect(url_for('login'))  # return
    else:
        return render_template('registrazione.html', errore=False)

#--------------------------------------------------------------------------------------------#
#Visualizzaizone saldo e ricarica protafoglio
@user_app.route('/aggiungi_visualizza_saldo', methods=['GET', 'POST'])
@login_required
def aggiungi_visualizza_saldo():
     if request.method == "POST":

         taglio = request.form["taglio"]
         saldo = meta.tables['saldo']
         ins = genere.insert();
         values = {
             'taglio' : taglio
         }

         conn = clienti_engine.connect()
         conn.execute(ins,values)
         conn.close()
         return redirect(url_for('aggiungi_visualizza_saldo'))
     else:
         utenti = request.tables['utenti']
         s = select([utenti.c.email, utenti.c.saldo]).where(utenti.c.email == current_user.email)

         conn = clienti_engine.connect()
         conn.execute(s)
         patrimonio = result.fetchone()
         conn.close()
         return render_template('dashboard_account.html', saldo = patrimonio)

#--------------------------------------------------------------------------------------------#
#modifica dei dati
@user_app.route('modifica_sicurezza', methods=['GET', 'POST'])
@login_required
def sicurezza():
     if request.method == "POST":
        utenti = meta.tables["utenti"]
        s = select(utenti).where(utenti.c.email == current_user.email)

        conn = clienti_engine.connect()
        result = conn.execute(s)

        nome = result.fetchone()["nome"]
        email = result.fetchone()["email"]
        psw_old = result.fetchone()["password"]

        psw_new_raw = meta.tables["psw"]
        psw_ceck = bcrypt.check_password_hash(pw_hash, 'psw_new_raw')
        if(psw_ceck)
           return render_template('aggiorna_dati_utente.html', errore = True)
       else:
           psw_new_hash = bcrypt.generate_password_hash(psw_new_raw).decode('utf-8')
           ins = utenti.insert()
           values = {
               'password' : psw_new_hash
           }

           conn.execute(ins)
           conn.close()
           return render_template('aggiorna_dati_utente.html', errore = False)
    else:
           utenti = meta.tables["utenti"]
           s = select(utenti).where(utenti.c.email == current_user.email)

           conn = clienti_engine.connect()
           result = conn.execute(s)

           money = result.fetchone()["saldo"]
           id = result.fetchone()["email"]

           conn.close()
           return render_template('aggiorna_dati_utente.html', saldo = money, email = id )

#--------------------------------------------------------------------------------------------#
