# Progetto basi di dati 2020 - Tema Cinema
# Gruppo: ArceCity
# Membri: Casarotti Giulio, Ferrari Simone, Trolese Gulio

# File: admin_route.py
# Descrizione: applicazione principale
#---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---#
from flask import Flask, render_template, url_for, redirect, request, session, flash, abort, Blueprint
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.sql import func
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
import json
from PIL import Image

import main_app as main_app
#from main_app import generate_persone_dict

admin_app = Blueprint('admin_app', __name__)

#--------------------------------------------------------------------------------------------#
# HOME PER LA GESTIONE DATABASE
@admin_app.route('/home_gestione_database')
@login_required
def home_gestione_database():
    if(current_user.is_admin == True):
        return render_template('home_gestione_database.html')
    else:
        return redirect(url_for('login'))


#--------------------------------------------------------------------------------------------#
# Inseriemnto di una persona
@admin_app.route('/aggiungi_persona', methods=['GET', 'POST'])
@login_required
def aggiungi_persona():
    if(current_user.is_admin == True):
        if request.method == 'POST':
            # prendiamo i dati dal form
            nome = request.form["nome"]
            cognome = request.form["cognome"]

            persone = meta.tables['persone']  # prendo la tabella
            ins = persone.insert()  # prendo la insert
            values = {  # dizionario per i valori
                'nome': nome,
                'cognome': cognome,
            }
            conn = admin_engine.connect()  # mi connetto
            conn.execute(ins, values)  # eseguo l'inserimento con i valori
            conn.close()
            if request.form["Submit"] == "Film": #abbiamo due diversi bottoni di sumbit
                return redirect(url_for('aggiungi_film'))  # return
            else:
                return redirect(url_for('aggiungi_persona'))
        else:
            return render_template('aggiungi_persona.html')
    else:
        return redirect(url_for('login')) # TODO: inserire messaggio di errore

#--------------------------------------------------------------------------------------------#
# Inserimento di un film
@admin_app.route('/aggiungi_film', methods=['GET', 'POST'])
@login_required
def aggiungi_film():
    if(current_user.is_admin == True):
        if request.method == 'POST':
            # prendiamo i dati dal form
            titolo = request.form["titolo"]
            durata = request.form["durata"]
            descrizione = request.form["descrizione"]

            film = main_app.meta.tables["film"]  # prendo la tabella
            ins = film.insert()  # prendo la insert
            values = {  # dizionario per i valori
                'titolo': titolo,
                'durata': durata,
                'descrizione': descrizione
            }

            id_film = 0

            # transazione per prendere l'id dell'ultimo film inserito (Ovvero quello che stiamo per inserire)
            # Questa transazione serve perchè, una voltas inserito il film, abbiamo bisogno
            # di prenderci il suo id... ma dobbiamo essere sicuri che nel mentre nessuno
            # aggiunga altri film: l'id preso risulterebbe quindi sbagliato.
            # Questo id poi ci serve per collegarlo agli attori e ai registi che recitano/dirigono il film inserito
            with main_app.admin_engine.connect().execution_options(isolation_level="SERIALIZABLE") as conn:
                trans = conn.begin()
                try:
                    conn.execute(ins, values)
                    sel = select([func.max(film.c.id_film).label('latest_film')])
                    result = conn.execute(sel)
                    id_film = result.fetchone()['latest_film']
                    trans.commit()
                except:
                    trans.rollback()
                finally:
                    conn.close()

            copertina = request.files["copertina"]

            copertina.save("./static/copertine/" + str(id_film) + ".jpg")

            conn = main_app.admin_engine.connect()
            # prendo le tre tabelle
            attori = main_app.meta.tables["attori"]
            registi = main_app.meta.tables["registi"]
            genere_film = main_app.meta.tables["genere_film"]

            list_attori = []
            list_registi = []
            list_generi = []
            # per ogni elemento del form (non so quanti siano di preciso...)
            for elem in request.form:
                # se è un attore
                if "attori" in str(elem):
                    id_attore = request.form[str(elem)]
                    if id_attore in list_attori:
                        return render_template('aggiungi_film.html', persone_dict=json.dumps(dict_p), generi_dict=json.dumps(dict_g), error = True, error_message="Attenzione, hai scelto lo stesso attore due volte.")
                    list_attori.append(id_attore)
                    ins_attori = attori.insert()
                    attori_values = {
                        "id_film": id_film,
                        "id_persona": id_attore
                    }

                    # aggiungo i dati alla tabella attori
                    conn.execute(ins_attori, attori_values)
                # se è un regista
                elif "registi" in str(elem):
                    id_regista = request.form[str(elem)]
                    if id_regista in list_registi:
                        return render_template('aggiungi_film.html', persone_dict=json.dumps(dict_p), generi_dict=json.dumps(dict_g), error = True, error_message="Attenzione, hai scelto lo stesso regista due volte.")
                    list_registi.append(id_regista)
                    ins_regista = registi.insert()
                    regista_values = {
                        "id_film": id_film,
                        "id_persona": id_regista
                    }
                    # aggiungo i dati alla tabella registi
                    conn.execute(ins_regista, regista_values)
                # se è un genere
                elif "generi" in str(elem):
                    tipo_genere = request.form[str(elem)]
                    if tipo_genere in list_generi:
                        return render_template('aggiungi_film.html', persone_dict=json.dumps(dict_p), generi_dict=json.dumps(dict_g), error = True, error_message="Attenzione, hai scelto lo stesso genere due volte.")
                    list_generi.append(tipo_genere)
                    ins_genere = genere_film.insert()
                    genere_values = {
                        "id_film": id_film,
                        "tipo_genere": tipo_genere
                    }
                    # aggiungo i dati alla tabella generi
                    conn.execute(ins_genere, genere_values)
                # TODO: togliere possibilità di selezione multipla da attori e registi
            conn.close()
            return redirect(url_for('admin_app.aggiungi_film'))
        else:
            dict_p = main_app.generate_persone_dict()
            dict_g = main_app.generate_generi_dict()
            return render_template('aggiungi_film.html', errore = False, error_message="", persone_dict=json.dumps(dict_p), generi_dict=json.dumps(dict_g))
    else:
        return redirect(url_for('login')) # TODO: inserire messaggio di errore

#--------------------------------------------------------------------------------------------#
# Inseriemnto di un amministratore (da parte di un amministratore)
@admin_app.route('/aggiungi_admin', methods=['GET', 'POST'])
@login_required
def aggiungi_admin():
    if(current_user.is_admin == True):
        if request.method == 'POST':

            # prendiamo i dati dal form
            nome = request.form["nome"]
            cognome = request.form["cognome"]
            data_nascita = str(request.form["data_nascita"])
            email = request.form["email"]
            psw = request.form["psw"]
            conferma = request.form["conferma_password"]

            utenti = meta.tables['utenti']  # prendo la tabella
            s = select(utenti.c.email).where(utenti.c.email == email)

            if result.rowcount > 0:
                return render_template('aggiungi_admin.html', errore=False)

            hashed_psw = bcrypt.generate_password_hash(psw).decode('utf-8')  # cripto la password

            # se le due password non corrispondono
            if(psw != conferma):
                return render_template('aggiungi_admin.html', errore=True)
            else:
                # prendiamo la tabella utenti dal metadata tramite reflection
                ins = utenti.insert()  # prendo la insert
                values = {  # dizionario per i valori
                    'nome': nome,
                    'cognome': cognome,
                    'data_nascita': data_nascita,
                    'email': email,
                    'password': hashed_psw,
                    'is_admin': True,
                    'saldo': 0.0
                }
                conn = admin_engine.connect()  # mi connetto
                conn.execute(ins, values)  # eseguo l'inserimento con i valori
                conn.close()
                return redirect(url_for('login'))  # return
        else:
            return render_template('aggiungi_admin.html', errore=False)
    else:
        return redirect(url_for('login')) # TODO: inserire messaggio di errore

#--------------------------------------------------------------------------------------------#
# Inseriemnto di una sala
@admin_app.route('/riepilogo_sale', methods=['GET', 'POST'])
@login_required
def riepilogo_sale():
    if(current_user.is_admin == True):
        if request.method == 'POST':
            n_posti = 150  # per semplicità, tutte le nostre sale hanno 150 posti

            sale = meta.tables['sale']  # prendo la tabella
            ins = sale.insert()  # prendo la insert
            values = {  # dizionario per i valori
                'n_posti': n_posti,
            }
            conn = admin_engine.connect()  # mi connetto
            conn.execute(ins, values)  # eseguo l'inserimento con i valori
            conn.close()
            return redirect(url_for('riepilogo_sale'))  # return
        else:
            return render_template('riepilogo_sale.html', sale=main_app.generate_sale_list())
    else:
        return redirect(url_for('login')) # TODO: inserire messaggio di errore
#--------------------------------------------------------------------------------------------#
# Inseriemnto di una proiezione
@admin_app.route('/aggiungi_proiezione', methods=['GET', 'POST'])
@login_required
def aggiungi_proiezione():
    if(current_user.is_admin == True):
        if request.method == 'POST':
            film = request.form["film"]
            proiezioni = meta.tables['proiezioni']
            ins = proiezioni.insert()
            conn = admin_engine.connect()
            row = dict()
            i = 0
            for elem in request.form:
                if "data" in str(elem):
                    row["data"] = request.form[str(elem)]
                    i += 1
                elif "ora" in str(elem):
                    row["ora_inizio"] = request.form[str(elem)]
                    i += 1
                elif "sala" in str(elem):
                    row["sala"] = request.form[str(elem)]
                    i += 1
                row["film"] = film
                if i == 3:
                    i = 0
                    conn.execute(ins, row)
            conn.close()
            return redirect(url_for('aggiungi_proiezione'))
        else:
            return render_template('aggiungi_proiezione.html', film_dict=main_app.generate_film_dict(), sale=json.dumps(main_app.generate_sale_list()))
    else:
        return redirect(url_for('login')) # TODO: inserire messaggio di errore

#--------------------------------------------------------------------------------------------#
# Inserimento di un genere
@admin_app.route('/aggiungi_genere', methods=['GET', 'POST'])
@login_required
def aggiungi_genere():
    if(current_user.is_admin == True):
        if request.method == 'POST':
            # prendiamo i dati dal form
            tipo = request.form["tipo"]

            genere = meta.tables['genere']  # prendo la tabella
            ins = genere.insert()  # prendo la insert
            values = {  # dizionario per i valori
                'tipo': tipo
            }
            conn = admin_engine.connect()  # mi connetto
            conn.execute(ins, values)  # eseguo l'inserimento con i valori
            conn.close()
            return redirect(url_for('aggiungi_film'))  # return
        else:
            return render_template('aggiungi_genere.html')
    else:
        return redirect(url_for('login')) # TODO: inserire messaggio di errore
