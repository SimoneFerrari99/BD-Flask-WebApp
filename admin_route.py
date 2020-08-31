# Progetto basi di dati 2020 - Tema Cinema
# Gruppo: ArceCity
# Membri: Casarotti Giulio, Ferrari Simone, Trolese Gulio

# File: admin_route.py
# Descrizione: File contenente tutte le route accessibili da un amminisrtatore / manager
#---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---#
from query import *

admin_app = Blueprint('admin_app', __name__)

#--------------------------------------------------------------------------------------------#
# HOME PER LA GESTIONE DATABASE
@ admin_app.route('/home_gestione_sito')
@ login_required
def home_gestione_sito():
    if(current_user.is_manager == True):
        return render_template('AdminTemplate/home_gestione_sito.html')
    else:
        return errore_admin()

#--------------------------------------------------------------------------------------------#
# Inserimento di una persona
@ admin_app.route('/aggiungi_persona', methods=['GET', 'POST'])
@ login_required
def aggiungi_persona():
    if(current_user.is_manager == True):
        if request.method == 'POST':
            # prendiamo i dati dal form
            nome = request.form["nome"]
            cognome = request.form["cognome"]

            ins = persone.insert()  # prendo la insert
            values = {  # dizionario per i valori
                'nome': nome,
                'cognome': cognome,
            }
            conn = manager_engine.connect()  # mi connetto
            conn.execute(ins, values)  # eseguo l'inserimento con i valori
            conn.close()
            # abbiamo due diversi bottoni di sumbit
            if request.form["Submit"] == "Film":
                return redirect(url_for('admin_app.aggiungi_film'))  # return
            else:
                return redirect(url_for('admin_app.aggiungi_persona'))
        else:
            return render_template('AdminTemplate/aggiungi_persona.html')
    else:
        return errore_admin()

#--------------------------------------------------------------------------------------------#
# Inserimento di un film
@ admin_app.route('/aggiungi_film', methods=['GET', 'POST'])
@ login_required
def aggiungi_film():
    if(current_user.is_manager == True):
        dict_p = generate_persone_dict()
        dict_g = generate_generi_dict()
        if request.method == 'POST':
            # prendiamo i dati dal form
            titolo = request.form["titolo"]
            durata = request.form["durata"]
            descrizione = request.form["descrizione"]

            ins = film.insert()  # prendo la insert
            values = {  # dizionario per i valori
                'titolo': titolo,
                'durata': durata,
                'descrizione': descrizione
            }

            id_film = 0

            list_attori = []
            list_registi = []
            list_generi = []

            for elem in request.form:
                # se è un attore
                if "attori" in str(elem):
                    id_attore = request.form[str(elem)]
                    if id_attore in list_attori:
                        return render_template('AdminTemplate/aggiungi_film.html',  errore=True, error_message="Attenzione, hai scelto lo stesso attore più di una volta.", persone_dict=json.dumps(dict_p), generi_dict=json.dumps(dict_g))
                    list_attori.append(id_attore)
                # se è un regista
                elif "registi" in str(elem):
                    id_regista = request.form[str(elem)]
                    if id_regista in list_registi:
                        return render_template('AdminTemplate/aggiungi_film.html',  errore=True, error_message="Attenzione, hai scelto lo stesso regista più di una volta.", persone_dict=json.dumps(dict_p), generi_dict=json.dumps(dict_g))
                    list_registi.append(id_regista)
                # se è un genere
                elif "generi" in str(elem):
                    tipo_genere = request.form[str(elem)]
                    if tipo_genere in list_generi:
                        return render_template('AdminTemplate/aggiungi_film.html', errore=True, error_message="Attenzione, hai scelto lo stesso genere più di una volta.", persone_dict=json.dumps(dict_p), generi_dict=json.dumps(dict_g))
                    list_generi.append(tipo_genere)

            if not list_generi:
                return render_template('AdminTemplate/aggiungi_film.html', errore=True, error_message="Attenzione, il film non ha un genere!", persone_dict=json.dumps(dict_p), generi_dict=json.dumps(dict_g))

            # transazione per prendere l'id dell'ultimo film inserito (Ovvero quello che stiamo per inserire)
            # Questa transazione serve perchè, una voltas inserito il film, abbiamo bisogno
            # di prenderci il suo id... ma dobbiamo essere sicuri che nel mentre nessuno
            # aggiunga altri film: l'id preso risulterebbe quindi sbagliato.
            # Questo id poi ci serve per collegarlo agli attori e ai registi che recitano/dirigono il film inserito
            with manager_engine.connect().execution_options(isolation_level="SERIALIZABLE") as conn:
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

            conn = manager_engine.connect()
            # prendo le tre tabelle

            # per ogni elemento del form (non so quanti siano di preciso...)
            for elem in request.form:
                # se è un attore
                if "attori" in str(elem):
                    id_attore = request.form[str(elem)]
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
                    ins_genere = genere_film.insert()
                    genere_values = {
                        "id_film": id_film,
                        "tipo_genere": tipo_genere
                    }
                    # aggiungo i dati alla tabella generi
                    conn.execute(ins_genere, genere_values)
            conn.close()
            return redirect(url_for('admin_app.aggiungi_film'))
        else:
            return render_template('AdminTemplate/aggiungi_film.html', errore=False, error_message="", persone_dict=json.dumps(dict_p), generi_dict=json.dumps(dict_g))
    else:
        return errore_admin()

#--------------------------------------------------------------------------------------------#
# Inseriemnto di un amministratore (da parte di un amministratore)
@ admin_app.route('/aggiungi_admin', methods=['GET', 'POST'])
@ login_required
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
            type_admin = request.form["type"]

            if type_admin == "admin":
                is_admin = True
                is_manager = True
            else:
                is_admin = False
                is_manager = True

            s = select([utenti]).where(
                utenti.c.email == email
            )
            conn = anonim_engine.connect()
            result = conn.execute(s)
            conn.close()

            if result.rowcount > 0:
                return render_template('AdminTemplate/aggiungi_admin.html', errore=True, error_message="Attenzione, email già in uso. Inserire una email non in uso")

            hashed_psw = bcrypt.generate_password_hash(psw).decode('utf-8')  # cripto la password

            # se le due password non corrispondono
            if(psw != conferma):
                return render_template('AdminTemplate/aggiungi_admin.html', errore=True, error_message="Attenzione, le due password non combaciano.")
            else:
                # prendiamo la tabella utenti dal metadata tramite reflection
                ins = utenti.insert()  # prendo la insert
                values = {  # dizionario per i valori
                    'nome': nome,
                    'cognome': cognome,
                    'data_nascita': data_nascita,
                    'email': email,
                    'password': hashed_psw,
                    'is_admin': is_admin,
                    'is_manager': is_manager,
                    'saldo': 0.0
                }
                conn = admin_engine.connect()  # mi connetto
                conn.execute(ins, values)  # eseguo l'inserimento con i valori
                conn.close()
                # return
                return redirect(url_for('login', errore=False, messaggio="None"))
        else:
            return render_template('AdminTemplate/aggiungi_admin.html', errore=False)
    else:
        return errore_admin()

#--------------------------------------------------------------------------------------------#
# Inseriemnto di una sala
@ admin_app.route('/riepilogo_sale', methods=['GET', 'POST'])
@ login_required
def riepilogo_sale():
    if(current_user.is_manager == True):
        if request.method == 'POST':
            n_posti = 150  # per semplicità, tutte le nostre sale hanno 150 posti

            ins = sale.insert()  # prendo la insert
            values = {  # dizionario per i valori
                'n_posti': n_posti,
            }
            conn = manager_engine.connect()  # mi connetto
            conn.execute(ins, values)  # eseguo l'inserimento con i valori
            conn.close()
            return redirect(url_for('admin_app.riepilogo_sale'))  # return
        else:
            return render_template('AdminTemplate/riepilogo_sale.html', sale=generate_sale_list())
    else:
        return errore_admin()
#--------------------------------------------------------------------------------------------#
# Inseriemnto di una proiezione
@ admin_app.route('/aggiungi_proiezione', methods=['GET', 'POST'])
@ login_required
def aggiungi_proiezione():
    if(current_user.is_manager == True):
        if request.method == 'POST':
            film = request.form["film"]
            ins = proiezioni.insert()
            conn = manager_engine.connect()
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
            return redirect(url_for('admin_app.aggiungi_proiezione'))
        else:
            return render_template('AdminTemplate/aggiungi_proiezione.html', film_dict=generate_film_dict(), sale=json.dumps(generate_sale_list()))
    else:
        return errore_admin()

#--------------------------------------------------------------------------------------------#
# Inserimento di un genere
@ admin_app.route('/aggiungi_genere', methods=['GET', 'POST'])
@ login_required
def aggiungi_genere():
    if(current_user.is_manager == True):
        if request.method == 'POST':
            # prendiamo i dati dal form
            tipo = request.form["tipo"]


            s = select([genere]).where(genere.c.tipo == tipo)
            conn = manager_engine.connect()
            result = conn.execute(s)
            conn.close()

            if result.rowcount > 0:
                return render_template("AdminTemplate/aggiungi_genere.html", errore=True, error_message="Attenzione, genere già inserito.")

            ins = genere.insert()  # prendo la insert
            values = {  # dizionario per i valori
                'tipo': tipo
            }
            conn = admin_engine.connect()  # mi connetto
            conn.execute(ins, values)  # eseguo l'inserimento con i valori
            conn.close()
            return redirect(url_for('admin_app.aggiungi_film'))  # return
        else:
            return render_template('AdminTemplate/aggiungi_genere.html', errore=False)
    else:
        return errore_admin()

#--------------------------------------------------------------------------------------------#
# Rimozione di un film
@ admin_app.route('/rimuovi_film', methods=['GET', 'POST'])
@ login_required
def rimuovi_film():
    if(current_user.is_admin == True):
        if request.method == 'POST':
            if "film" in request.form:
                # prendiamo i dati dal form
                id_film = request.form["film"]


                rem = film.delete().where(film.c.id_film == id_film)
                conn = admin_engine.connect()  # mi connetto
                conn.execute(rem)  # eseguo l'inserimento con i valori
                conn.close()
                return render_template('AdminTemplate/rimuovi_film.html', film_dict=generate_film_dict(), errore=False)
            else:
                return render_template('AdminTemplate/rimuovi_film.html', errore=True, error_message="Errore, stai provando a rimuovere una proiezione che non esiste", film_dict=generate_film_dict())
        else:
            return render_template('AdminTemplate/rimuovi_film.html', film_dict=generate_film_dict(), errore=False)
    else:
        return errore_admin()

#--------------------------------------------------------------------------------------------#
# Rimozione di una proiezione
@ admin_app.route('/rimuovi_proiezione', methods=['GET', 'POST'])
@ login_required
def rimuovi_proiezione():
    if(current_user.is_admin == True):
        if request.method == 'POST':
            if "film" and "proiezione" in request.form:
                # prendiamo i dati dal form
                id_pr = request.form["proiezione"]


                rem = proiezioni.delete().where(proiezioni.c.id_proiezione == id_pr)
                conn = admin_engine.connect()  # mi connetto
                conn.execute(rem)  # eseguo l'inserimento con i valori
                conn.close()
                return render_template('AdminTemplate/rimuovi_proiezioni.html', film_dict=generate_film_dict(), proiezioni=json.dumps(generate_all_projection()), errore=False)
            else:
                return render_template('AdminTemplate/rimuovi_proiezioni.html', errore=True, error_message="Errore, stai provando a rimuovere una proiezione che non esiste", film_dict=generate_film_dict(), proiezioni=json.dumps(generate_all_projection()))
        else:

            return render_template('AdminTemplate/rimuovi_proiezioni.html', film_dict=generate_film_dict(), proiezioni=json.dumps(generate_all_projection()), errore=False)
    else:
        return errore_admin()


@ admin_app.route('/statistiche')
@ login_required
def statistiche():
    statistiche = dict()
    statistiche["n_film"] = STAT_numero_di_film()
    statistiche["film_piu_proiezioni"] = STAT_film_con_piu_proiezioni()
    statistiche["film_piu_posti"] = STAT_film_con_piu_posti_prenotati_totali()
    statistiche["film_piu_incasso"] = STAT_film_con_piu_incassi_totali()
    statistiche["genere_piu_posti"] = STAT_genere_con_piu_posti_prenotati()
    statistiche["genere_piu_incassi"] = STAT_genere_con_piu_incassi()
    statistiche["n_proiezioni"] = STAT_numero_di_proiezioni_totale()
    statistiche["pr_piu_prenotata"] = STAT_proiezione_piu_prenotata()
    statistiche["pr_piu_incasso"] = STAT_proiezione_con_incasso_piu_alto()
    statistiche["orario_piu_pr"] = STAT_orario_piu_prenotato()
    statistiche["attore_piu_film"] = STAT_attore_in_piu_film()
    statistiche["regista_piu_film"] = STAT_regista_di_piu_film()
    statistiche["n_clienti"] = STAT_numero_clienti_iscritti()
    statistiche["n_posti_medio"] = STAT_numero_posti_medio_prenotati_da_un_cliente()
    statistiche["eta_media_user"] = STAT_eta_media_utenti()
    statistiche["numero_proiezioni_sala"] = STAT_numero_proiezioni_per_sala()
    statistiche["durata_media_per_sala"] = STAT_durata_media_dei_film_per_sala()

    return render_template('AdminTemplate/statistiche.html', statistiche=statistiche)
