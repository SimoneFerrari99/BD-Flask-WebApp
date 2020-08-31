# Progetto basi di dati 2020 - Tema Cinema
# Gruppo: ArceCity
# Membri: Casarotti Giulio, Ferrari Simone, Trolese Gulio

# File: user_route.py
# Descrizione: File contenente tutte le route accessibili da un cliente registrato
#---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---#
from query import *

user_app = Blueprint('user_app', __name__)


#--------------------------------------------------------------------------------------------#
# Visualizzaizone profilo, saldo e ricarica protafoglio
@ user_app.route('/dashboard_account')
@ login_required
def dashboard_account():

    s = select([utenti]).where(utenti.c.email == current_user.email)

    conn = clienti_engine.connect()
    result = conn.execute(s)
    row = result.fetchone()

    portafoglio = row["saldo"]
    name = row["nome"].capitalize()
    surname = row["cognome"].capitalize()
    email = row["email"]

    conn.close()
    return render_template('UserTemplate/dashboard_account.html', saldo=portafoglio, nome=name, cognome=surname, email=email)

#--------------------------------------------------------------------------------------------#
# modifica della password
@ user_app.route('/cambia_password', methods=['GET', 'POST'])
@ login_required
def cambia_password():
    if request.method == "POST":

        old_psw = request.form["old_psw"]
        psw = request.form["psw"]
        conferma = request.form["conferma_password"]

        conn = clienti_engine.connect()

        psw_ceck = bcrypt.check_password_hash(current_user.password, old_psw)

        if psw_ceck == False:
            # Messaggio di errore da inviare all'utente
            return render_template('UserTemplate/cambia_password.html', errore=True, error_message="Errore: password vecchia errata!")
        elif psw != conferma:
            conn.close()
            return render_template('UserTemplate/cambia_password.html', errore=True, error_message="Attenzione, le due nuove password non combaciano. Prego reinserire correttamente i dati")
        elif old_psw == psw:
            conn.close()
            return render_template('UserTemplate/cambia_password.html', errore=True, error_message="Attenzione, la vecchia e la nuova password combaciano. Prego reinserire password diverse")
        else:
            psw_new_hash = bcrypt.generate_password_hash(psw).decode('utf-8')
            ins = utenti.update().where(utenti.c.email == current_user.email)
            values = {
                'password': psw_new_hash
            }

            conn.execute(ins, values)
            conn.close()
            return redirect(url_for('user_app.dashboard_account'))
    else:
        return render_template('UserTemplate/cambia_password.html', errore=False)

#--------------------------------------------------------------------------------------------#
# ricaricare il proprio saldo
@ user_app.route('/ricarica_saldo', methods=['GET', 'POST'])
@ login_required
def ricarica_saldo():
    s = select([utenti]).where(utenti.c.email == current_user.email)
    conn = clienti_engine.connect()
    result = conn.execute(s)
    saldo = result.fetchone()["saldo"]

    if request.method == "POST":
        taglio = request.form["taglio"]
        ins = utenti.update().where(utenti.c.email == current_user.email)
        values = {
            'saldo': saldo + float(taglio)
        }

        conn.execute(ins, values)
        conn.close()
        return redirect(url_for('user_app.dashboard_account'))

    else:
        return render_template('UserTemplate/ricarica_saldo.html', saldo=saldo)

#--------------------------------------------------------------------------------------------#
# Prenotazione di un prenota_biglietto
@ user_app.route('/prenota_biglietto/<id_pr>', methods=['GET', 'POST'])
@ login_required
def prenota_biglietto(id_pr):
    if request.method == "POST":
        scelti = request.json["posti"]
        totale = float(request.json["totale"])
        ins = posti.insert()


        with clienti_engine.connect().execution_options(isolation_level="REPEATABLE READ") as conn:
            trans = conn.begin()
            try:
                sel = select([utenti.c.saldo]).\
                      where(utenti.c.email == current_user.email)
                result = conn.execute(sel)
                row = result.fetchone()
                if row["saldo"] >= totale:
                    for posto in scelti:
                        values = {
                            "id_posto": posto,
                            "prezzo": 5,
                            "prenotato": current_user.email,
                            "id_proiezione": id_pr
                        }
                        conn.execute(ins, values)
                    up = utenti.update().where(utenti.c.email == current_user.email)
                    values = {
                        "saldo": row["saldo"] - totale
                    }
                    conn.execute(up, values)
                    trans.commit()
                else:
                    trans.rollback()
                    return "Unassigned", 430
            except:
                trans.rollback()
                return "Conflict", 409
            finally:
                conn.close()
        return 'OK', 200
    else:
        j = film.join(proiezioni, film.c.id_film == proiezioni.c.film)  # JOIN
        s = select([film, proiezioni]).\
            select_from(j).\
            where(proiezioni.c.id_proiezione == id_pr)
        conn = clienti_engine.connect()
        proiezione = conn.execute(s)
        row = proiezione.fetchone()
        s = select([posti.c.id_posto]).\
            where(posti.c.id_proiezione == id_pr)
        result = conn.execute(s)
        occupati = []
        for elem in result:
            occupati.append(elem[0])
        return render_template('UserTemplate/prenota_biglietto.html', rossi = occupati, titolo=row["titolo"], data=row["data"], ora=row["ora_inizio"], sala=row["sala"], id=id_pr)

#--------------------------------------------------------------------------------------------#
# visualizziamo tutte le mie prenotazioni
@ user_app.route('/le_mie_prenotazioni')
@ login_required
def le_mie_prenotazioni():
    dict = generate_my_projection_dict()
    ordered_list = sorted(dict, key = lambda i: (i['data'], i['ora_inizio']))
    return render_template('UserTemplate/le_mie_prenotazioni.html', projection_dict=ordered_list)
