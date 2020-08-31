# Progetto basi di dati 2020 - Tema Cinema
# Gruppo: ArceCity
# Membri: Casarotti Giulio, Ferrari Simone, Trolese Gulio

# File: app.py
# Descrizione: App principale, contiene le route a cui vi si può accedere senza essere loggati

#---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---#
# Moduli importati
from user_route import user_app
from admin_route import admin_app
from query import *

app.register_blueprint(user_app)
app.register_blueprint(admin_app)

#---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---#
# Route principale: Home
@ app.route('/')
def home():
    if(current_user.is_anonymous == False and current_user.is_admin == True):
        admin = True
        manager = True
    elif current_user.is_anonymous == False and current_user.is_manager == True:
        admin = False
        manager = True
    else:
        admin = False
        manager = False
    proj_list = generate_all_film_next_projection()
    new_proj = []
    for dict in proj_list:
        if not is_in(new_proj, dict["id_film"]):
            new_proj.append(dict)
    proj_list = new_proj
    ordered_list = sorted(proj_list, key = lambda i: (i['data'], i['ora_inizio']))
    ordered_list = ordered_list[:5]
    return render_template('home.html', proj_list=ordered_list, is_admin=admin, is_manager = manager)

#--------------------------------------------------------------------------------------------#
# Login
@ login_manager.user_loader
def load_user(user_email):  # funzione che restituisce l'utente associato alla user_email
    utenti = meta.tables['utenti']
    s = select([utenti]).where(utenti.c.email == user_email)
    conn = anonim_engine.connect()
    result = conn.execute(s)
    if result.rowcount == 0:  # se non è presente l'utente cercato
        return None
    user = result.fetchone()
    conn.close()
    # ritorna un Utente
    return Utente(user.email, user.password, user.is_admin, user.is_manager)


# Quando il login è richiesto, e non sei loggato, vieni rimandato al login
@ login_manager.unauthorized_handler
def unauthorized():
    # TODO: dare un messaggio di errore
    return redirect(url_for('login', errore=True, messaggio="Attenzione, non sei autorizzato ad accedere a questa pagina. Accedi con le giuste credenziali"))


@ app.route('/login/<errore>/<messaggio>', methods=['GET', 'POST'])
def login(errore, messaggio):
    if request.method == 'POST':  # gestione del form
        # prendiamo i dati dal form
        email_form = request.form["email"]
        password = request.form["psw"]
        # carichiamo l'utente
        utente = load_user(email_form)
        # se la password salvata nel database e quella inserita nel form coincidono
        if utente != None and bcrypt.check_password_hash(utente.password, password) == True:
            login_user(utente)  # loggo l'utente
            resp = make_response(redirect(url_for('home')))
            resp.set_cookie("userEmail", current_user.email)
            return resp
        else:
            return redirect(url_for('login', errore=True, messaggio="Attenzione, mail o password errate."))
    else:
        return render_template('login.html', error=errore, error_message=messaggio)
#--------------------------------------------------------------------------------------------#
# Logout
@ app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('home')))
    resp.set_cookie("userEmail", "", max_age=0)
    logout_user()
    return resp

#--------------------------------------------------------------------------------------------#
# Registrazione di un nuovo utente
@ app.route('/registrazione', methods=['GET', 'POST'])
def registrazione():
    if request.method == 'POST':
        # prendiamo i dati dal form
        nome = request.form["nome"]
        cognome = request.form["cognome"]
        data_nascita = str(request.form["data_nascita"])
        email = request.form["email"]
        psw = request.form["psw"]
        conferma = request.form["conferma_password"]

        s = select([utenti]).where(
            utenti.c.email == email
        )
        conn = anonim_engine.connect()
        result = conn.execute(s)
        if result.rowcount > 0:  # se non è presente l'utente cercato
            conn.close()
            return render_template('registrazione.html', errore=True, error_message="Attenzione, email già in uso. Inserire un'altra email")

        hashed_psw = bcrypt.generate_password_hash(psw).decode('utf-8')  # cripto la password

        # se le due password non corrispondono
        if(psw != conferma):
            conn.close()
            return render_template('registrazione.html', errore=True, error_message="Attenzione, le due password non combaciano. Prego reinserire correttamente i dati")
        else:
            # prendiamo la tabella utenti dal metadata tramite reflection
            ins = utenti.insert()  # prendo la insert
            values = {  # dizionario per i valori
                'nome': nome,
                'cognome': cognome,
                'data_nascita': data_nascita,
                'email': email,
                'password': hashed_psw,
                'is_admin': False,
                'is_manager': False,
                'saldo': 0.0
            }
            conn.execute(ins, values)  # eseguo l'inserimento con i valori
            conn.close()
            # return
            return redirect(url_for('login', errore=False, messaggio="None"))
    else:
        return render_template('registrazione.html', errore=False)

#--------------------------------------------------------------------------------------------#
# visualizziamo tutti i film con la prossima proiezione in programma
@ app.route('/tutti_i_film', methods=['GET', 'POST'])
def tutti_i_film():
    proj_list = generate_all_film_next_projection()
    if request.method == "POST":
        if request.form["cerca_genere"]:
            genere = request.form["cerca_genere"].capitalize()
            proj_list = filter(lambda d: d["genere"] == genere, proj_list)
    new_proj = []
    for dict in proj_list:
        if not is_in(new_proj, dict["id_film"]):
            new_proj.append(dict)
    proj_list = new_proj
    ordered_list = sorted(proj_list, key = lambda i: (i['titolo']))
    return render_template('UserTemplate/tutti_i_film.html', proj_list=ordered_list)

#--------------------------------------------------------------------------------------------#
# visualizziamo tutte le proiezioni in programma per un determinato film
@app.route('/altre_date_film/<id_film>', methods=['GET', 'POST'])
def altre_date_film(id_film):
    dict = generate_all_projection_film(id_film)
    return render_template('UserTemplate/altre_date_film.html', dict_film = dict )
