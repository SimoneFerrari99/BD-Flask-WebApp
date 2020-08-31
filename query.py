# Progetto basi di dati 2020 - Tema Cinema
# Gruppo: ArceCity
# Membri: Casarotti Giulio, Ferrari Simone, Trolese Gulio

# File: query.py
# Descrizione: File contenente funzioni d'appoggio e query utili
#---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---#
# Moduli importati
from engine import *

#---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---#
# Funzioni utili

# controlla se un id_film è presente in uno dei dizonari presenti nella lista passata come parametro
def is_in(dict_list, id_film):
    for dict in dict_list:
        if id_film == dict["id_film"]:
            return True
    return False

# generatore di un dizionario per le persone
def generate_persone_dict():
    s = select([persone])
    conn = anonim_engine.connect()
    result = conn.execute(s)
    dict_persone = dict()
    for row in result:
        dict_persone[row['id_persona']] = str(row['nome'])+' '+str(row['cognome'])
    conn.close()
    return dict_persone

 # generatore di un dizionario per i film
def generate_film_dict():
    s = select([film])
    conn = anonim_engine.connect()
    result = conn.execute(s)
    dict_film = dict()
    for row in result:
        dict_film[row['id_film']] = [
            row['titolo'], row['durata'], row['descrizione']]
    conn.close()
    return dict_film

# generatore di un dizionario per i generi
def generate_generi_dict():
    s = select([genere])
    conn = anonim_engine.connect()
    result = conn.execute(s)
    dict_generi = dict()
    for row in result:
        dict_generi[row['tipo']] = [row['tipo']]
    conn.close()
    return dict_generi

# generatore di un dizionario per le sale
def generate_sale_list():
    s = select([sale])
    conn = anonim_engine.connect()
    result = conn.execute(s)
    list_sale = []
    for row in result:
        list_sale.append(row['n_sala'])
    conn.close()
    return list_sale

def errore_admin():
    return redirect(url_for('login', errore=True, messaggio="Attenzione, solo gli amministratori sono autorizzati ad accedere a questa pagina."))

# Genera una lista di dizionari contenente tutte le mie proiezioni prenotate e non ancor avvenute
def generate_my_projection_dict():
    j = posti.join(proiezioni.join(film, proiezioni.c.film == film.c.id_film),
                   posti.c.id_proiezione == proiezioni.c.id_proiezione)
    s = select([proiezioni.c.id_proiezione, film.c.id_film, film.c.titolo, film.c.durata, film.c.descrizione, proiezioni.c.data, proiezioni.c.ora_inizio, proiezioni.c.sala, func.count().label('num_biglietti')]).\
        select_from(j).\
        where(and_(
            posti.c.prenotato == current_user.email,
            or_(
                proiezioni.c.data > func.current_date(),
                and_(
                    proiezioni.c.data == func.current_date(),
                    proiezioni.c.ora_inizio >= func.current_time()
                    )
               )
        )).\
        group_by(proiezioni.c.id_proiezione, film.c.id_film, film.c.titolo, film.c.durata, film.c.descrizione, proiezioni.c.id_proiezione)

    conn = clienti_engine.connect()
    result = conn.execute(s)

    list_all_projection = []

    for row in result:  # lista di dizionari
        dict_projection = dict()
        dict_projection["id_film"] = row['id_film']
        dict_projection["id_proiezione"] = row['id_proiezione']
        dict_projection["titolo"] = row['titolo']
        dict_projection["durata"] = row['durata']
        dict_projection["descrizione"] = row['descrizione']
        dict_projection["data"] = row['data']
        dict_projection["ora_inizio"] = row['ora_inizio']
        dict_projection["sala"] = row['sala']
        dict_projection["num_biglietti"] = row['num_biglietti']
        list_all_projection.append(dict_projection)

    conn.close()
    return list_all_projection

# genera una lista di dizionari contenente la prossima proiezione per ogni film
def generate_all_film_next_projection():
    pr = meta.tables['proiezioni']

    view = '''create or replace view proiezioni_valide(id_proiezione, data_ora, film) as
                select id_proiezione, ora_inizio + data, film
                from proiezioni
                where ("data" > current_date or ("data" = current_date and ora_inizio >= current_time))'''

    s = '''
        select f.titolo, gf.tipo_genere, f.descrizione, f.durata, pr.id_proiezione, pr.sala, pr.film, pr."data" , pr.ora_inizio
        from proiezioni pr join film f on pr.film = f.id_film join genere_film gf on f.id_film = gf.id_film
        where (pr.ora_inizio + pr.data) = (select min("data_ora")
                         from proiezioni_valide pv
                         where pv.film = pr.film )
        group by (f.titolo, gf.tipo_genere, f.descrizione, pr.film, pr.id_proiezione, pr."data", pr.ora_inizio, f.durata, pr.sala)'''

    conn = anonim_engine.connect()
    conn.execute(view)
    result = conn.execute(s)

    list_next_projection = []

    for row in result:  # lista di dizionari
        dict_next_projection = dict()
        dict_next_projection["id_proiezione"] = int(row["id_proiezione"])
        dict_next_projection["id_film"] = row['film']
        dict_next_projection["genere"] = row["tipo_genere"]
        dict_next_projection["titolo"] = row['titolo']
        dict_next_projection["descrizione"] = row["descrizione"]
        dict_next_projection["ora_inizio"] = str(row['ora_inizio'])
        dict_next_projection["durata"] = row['durata']
        dict_next_projection["data"] = str(row['data'])
        dict_next_projection["sala"] = row['sala']
        list_next_projection.append(dict_next_projection)

    conn.close()
    return list_next_projection


# genera tutte le proiezioni programmate per un determinato film
def generate_all_projection_film(id):
    j = film.join(proiezioni, film.c.id_film == proiezioni.c.film)  # JOIN
    s = select([film, proiezioni]).\
        select_from(j).\
        where(and_(or_(
                proiezioni.c.data > func.current_date(),
                and_(
                    proiezioni.c.data == func.current_date(),
                    proiezioni.c.ora_inizio >= func.current_time()
                    )
                ), film.c.id_film == id)
            )
    conn = clienti_engine.connect()
    result = conn.execute(s)

    list_all_projection = []
    for row in result:
        dict_projection = dict()
        dict_projection["id_proiezione"] = row["id_proiezione"]
        dict_projection["descrizione"] = row["descrizione"]
        dict_projection["durata"] = row["durata"]
        dict_projection["id_film"] = row["id_film"]
        dict_projection["titolo"] = row["titolo"]
        dict_projection["data"] = row["data"]
        dict_projection["ora_inizio"] = row["ora_inizio"]
        dict_projection["sala"] = row["sala"]
        list_all_projection.append(dict_projection)
    conn.close()
    return list_all_projection

# genera tutte le proiezioni programmate per tutti i film
def generate_all_projection():
    j = film.join(proiezioni, film.c.id_film == proiezioni.c.film)  # JOIN
    s = select([film, proiezioni]).\
        select_from(j).\
        where(or_(
                proiezioni.c.data > func.current_date(),
                and_(
                    proiezioni.c.data == func.current_date(),
                    proiezioni.c.ora_inizio >= func.current_time()
                    )
                )
            )
    conn = clienti_engine.connect()
    result = conn.execute(s)

    list_all_projection = []
    for row in result:
        dict_projection = dict()
        dict_projection["id_proiezione"] = row["id_proiezione"]
        dict_projection["titolo"] = row["titolo"]
        dict_projection["id_film"] = row["id_film"]
        dict_projection["data"] = str(row["data"])
        dict_projection["ora_inizio"] = str(row["ora_inizio"])
        dict_projection["sala"] = row["sala"]
        list_all_projection.append(dict_projection)
    conn.close()
    return list_all_projection


#---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---#
# Query Statistiche


def STAT_numero_di_film():
    select = '''select count(*) as numfilm
                from film '''
    conn = manager_engine.connect()
    result = conn.execute(select)
    dict_list = []
    for row in result:
        dizionario = dict()
        dizionario["numfilm"] = row["numfilm"]
        dict_list.append(dizionario)
    return dict_list


def STAT_film_con_piu_proiezioni():
    view = '''create or replace view numero_proiezioni_per_film(id_film, num_proiezioni) as
                select id_film, count(id_proiezione)
                from film left join proiezioni on film.id_film = proiezioni.film
                group by id_film'''

    select = '''select *
                from film f natural join numero_proiezioni_per_film n
                where n.num_proiezioni = (select max(num_proiezioni)
                                          from numero_proiezioni_per_film)'''
    conn = manager_engine.connect()
    conn.execute(view)
    result = conn.execute(select)
    dict_list = []
    for row in result:
        dizionario = dict()
        dizionario["titolo"] = row["titolo"]
        dizionario["num_proiezioni"] = row["num_proiezioni"]
        dict_list.append(dizionario)
    return dict_list


def STAT_film_con_piu_posti_prenotati_totali():
    view = '''create or replace view numero_posti_totali_prenotati_per_film(id_film, num_posti) as
                select pr.film, count(po.id_posto)
                from proiezioni pr natural join posti po
                group by pr.film'''

    select = '''select *
                from film f natural join numero_posti_totali_prenotati_per_film n
                where n.num_posti = (select max(num_posti)
                                     from numero_posti_totali_prenotati_per_film)'''

    conn = manager_engine.connect()
    conn.execute(view)
    result = conn.execute(select)
    dict_list = []
    for row in result:
        dizionario = dict()
        dizionario["titolo"] = row["titolo"]
        dizionario["num_posti"] = row["num_posti"]
        dict_list.append(dizionario)
    return dict_list


def STAT_film_con_piu_incassi_totali():
    view = '''create or replace view incasso_per_ogni_film(id_film, incasso) as
                select film, sum(prezzo)
                from proiezioni natural join posti
                group by film'''

    select = '''select *
                from film f natural join incasso_per_ogni_film n
                where n.incasso = (select max(incasso)
                                  from incasso_per_ogni_film)'''
    conn = manager_engine.connect()
    conn.execute(view)
    result = conn.execute(select)
    dict_list = []
    for row in result:
        dizionario = dict()
        dizionario["titolo"] = row["titolo"]
        dizionario["incasso"] = row["incasso"]
        dict_list.append(dizionario)
    return dict_list


def STAT_genere_con_piu_posti_prenotati():
    view = '''create or replace view numero_posti_totali_prenotati_e_incasso_per_genere(tipo_genere, num_posti, incasso) as
                select gf.tipo_genere, count(po.id_posto), sum(po.prezzo)
                from proiezioni pr natural join posti po join film f on pr.film = f.id_film natural join genere_film gf
                group by gf.tipo_genere'''

    select = '''select *
                from numero_posti_totali_prenotati_e_incasso_per_genere n
                where n.num_posti = (select max(num_posti)
                                     from numero_posti_totali_prenotati_e_incasso_per_genere)'''
    conn = manager_engine.connect()
    conn.execute(view)
    result = conn.execute(select)
    dict_list = []
    for row in result:
        dizionario = dict()
        dizionario["tipo_genere"] = row["tipo_genere"]
        dizionario["num_posti"] = row["num_posti"]
        dict_list.append(dizionario)
    return dict_list


def STAT_genere_con_piu_incassi():
    view = '''create or replace view numero_posti_totali_prenotati_e_incasso_per_genere(tipo_genere, num_posti, incasso) as
                select gf.tipo_genere, count(po.id_posto), sum(po.prezzo)
                from proiezioni pr natural join posti po join film f on pr.film = f.id_film natural join genere_film gf
                group by gf.tipo_genere'''
    select = '''select *
                from numero_posti_totali_prenotati_e_incasso_per_genere n
                where n.incasso = (select max(incasso)
                                   from numero_posti_totali_prenotati_e_incasso_per_genere)'''
    conn = manager_engine.connect()
    conn.execute(view)
    result = conn.execute(select)
    dict_list = []
    for row in result:
        dizionario = dict()
        dizionario["tipo_genere"] = row["tipo_genere"]
        dizionario["incasso"] = row["incasso"]
        dict_list.append(dizionario)
    return dict_list


def STAT_numero_di_proiezioni_totale():
    select = '''select count(*) as numproiezioni
                from proiezioni'''
    conn = manager_engine.connect()
    result = conn.execute(select)
    dict_list = []
    for row in result:
        dizionario = dict()
        dizionario["numproiezioni"] = row["numproiezioni"]
        dict_list.append(dizionario)
    return dict_list


def STAT_proiezione_piu_prenotata():
    view = '''create or replace view numero_posti_prenotati_e_incasso_per_proiezione(id_proiezione, data, ora_inizio, sala, id_film, num_posti, incasso) as
                select pr.id_proiezione, pr.data, pr.ora_inizio, pr.sala, pr.film, count(po.id_posto), sum(po.prezzo)
                from proiezioni pr natural join posti po
                group by pr.id_proiezione, pr.film '''

    select = '''select *
                from film f natural join numero_posti_prenotati_e_incasso_per_proiezione n
                where n.num_posti = (select max(num_posti)
                                     from numero_posti_prenotati_e_incasso_per_proiezione)'''

    conn = manager_engine.connect()
    conn.execute(view)
    result = conn.execute(select)
    dict_list = []
    for row in result:
        dizionario = dict()
        dizionario["titolo"] = row["titolo"]
        dizionario["data"] = str(row["data"])
        dizionario["ora_inizio"] = str(row["ora_inizio"])
        dizionario["sala"] = row["sala"]
        dizionario["num_posti"] = row["num_posti"]
        dict_list.append(dizionario)
    return dict_list


def STAT_proiezione_con_incasso_piu_alto():
    view = '''create or replace view numero_posti_prenotati_e_incasso_per_proiezione(id_proiezione, data, ora_inizio, sala, id_film, num_posti, incasso) as
                select pr.id_proiezione, pr.data, pr.ora_inizio, pr.sala, pr.film, count(po.id_posto), sum(po.prezzo)
                from proiezioni pr natural join posti po
                group by pr.id_proiezione, pr.film'''

    select = '''select *
                from film f natural join numero_posti_prenotati_e_incasso_per_proiezione n
                where n.incasso = (select max(incasso)
                                  from numero_posti_prenotati_e_incasso_per_proiezione)'''
    conn = manager_engine.connect()
    conn.execute(view)
    result = conn.execute(select)
    dict_list = []
    for row in result:
        dizionario = dict()
        dizionario["titolo"] = row["titolo"]
        dizionario["data"] = str(row["data"])
        dizionario["ora_inizio"] = str(row["ora_inizio"])
        dizionario["sala"] = row["sala"]
        dizionario["incasso"] = row["incasso"]
        dict_list.append(dizionario)
    return dict_list


def STAT_orario_piu_prenotato():
    view = '''create or replace view numero_posti_prenotati_per_orario(ora_inizio, num_posti) as
                select pr.ora_inizio, count(po.id_posto)
                from proiezioni pr natural join posti po
                group by pr.ora_inizio'''

    select = '''select *
                from numero_posti_prenotati_per_orario n
                where n.num_posti = (select max(num_posti)
                                     from numero_posti_prenotati_per_orario)'''
    conn = manager_engine.connect()
    conn.execute(view)
    result = conn.execute(select)
    dict_list = []
    for row in result:
        dizionario = dict()
        dizionario["ora_inizio"] = str(row["ora_inizio"])
        dizionario["num_posti"] = row["num_posti"]
        dict_list.append(dizionario)
    return dict_list


def STAT_attore_in_piu_film():
    view = '''create or replace view attori_film(id_persona, num_film) as
                select a.id_persona, count(f.id_film)
                from attori a natural join film f
                group by a.id_persona'''

    select = '''select *
                from persone natural join attori_film n
                where n.num_film = (select max(num_film)
                                    from attori_film)'''

    conn = manager_engine.connect()
    conn.execute(view)
    result = conn.execute(select)
    dict_list = []
    for row in result:
        dizionario = dict()
        dizionario["nome"] = row["nome"]
        dizionario["cognome"] = row["cognome"]
        dizionario["num_film"] = row["num_film"]
        dict_list.append(dizionario)
    return dict_list


def STAT_regista_di_piu_film():
    view = '''create or replace view registi_film(id_persona, num_film) as
                select r.id_persona, count(f.id_film)
                from registi r natural join film f
                group by r.id_persona'''

    select = '''select *
                from persone natural join registi_film n
                where n.num_film = (select max(num_film)
                                    from registi_film)'''
    conn = manager_engine.connect()
    conn.execute(view)
    result = conn.execute(select)
    dict_list = []
    for row in result:
        dizionario = dict()
        dizionario["nome"] = row["nome"]
        dizionario["cognome"] = row["cognome"]
        dizionario["num_film"] = row["num_film"]
        dict_list.append(dizionario)
    return dict_list


def STAT_numero_clienti_iscritti():
    select = '''select count(*) as numutenti
                from utenti
                where not is_admin and not is_manager'''
    conn = manager_engine.connect()
    result = conn.execute(select)
    dict_list = []
    for row in result:
        dizionario = dict()
        dizionario["numutenti"] = row["numutenti"]
        dict_list.append(dizionario)
    return dict_list


def STAT_numero_posti_medio_prenotati_da_un_cliente():
    view = '''create or replace view utente_prenotazioni(email, num_prenotazioni) as
                select u.email, count(po.id_posto)
                from posti po join utenti u on po.prenotato = u.email
                group by u.email'''

    select = '''select avg(num_prenotazioni) as num_prenotazioni_media
                from utente_prenotazioni'''
    conn = manager_engine.connect()
    conn.execute(view)
    result = conn.execute(select)
    dict_list = []
    for row in result:
        dizionario = dict()
        dizionario["num_prenotazioni_media"] = round(float(row["num_prenotazioni_media"]), 2)
        dict_list.append(dizionario)
    return dict_list


def STAT_eta_media_utenti():
    view = '''create or replace view utente_eta(email, eta) as
                select u.email, (current_date-u.data_nascita)/365.25
                from utenti u
                group by u.email'''

    select = '''select avg(eta) as eta_media
                from utente_eta'''
    conn = manager_engine.connect()
    conn.execute(view)
    result = conn.execute(select)
    dict_list = []
    for row in result:
        dizionario = dict()
        dizionario["eta_media"] = round(float(row["eta_media"]), 2)
        dict_list.append(dizionario)
    return dict_list


def STAT_numero_proiezioni_per_sala():
    select = '''select n_sala, count(*) as num_proiezioni
                from proiezioni pr join sale s on pr.sala = s.n_sala
                group by n_sala
                order by n_sala'''
    conn = manager_engine.connect()
    result = conn.execute(select)
    dict_list = []
    for row in result:
        dizionario = dict()
        dizionario["n_sala"] = row["n_sala"]
        dizionario["num_proiezioni"] = row["num_proiezioni"]
        dict_list.append(dizionario)
    return dict_list


def STAT_durata_media_dei_film_per_sala():
    view = '''create or replace view sala_film_durata(n_sala, num_film, tot_durata) as
                select s.n_sala, count(f.id_film), sum(f.durata)
                from sale s join proiezioni pr on s.n_sala = pr.sala join film f on pr.film = f.id_film
                group by s.n_sala'''

    select = '''select n_sala, tot_durata / num_film as durata_media
                from sala_film_durata
                order by n_sala'''
    conn = manager_engine.connect()
    conn.execute(view)
    result = conn.execute(select)
    dict_list = []
    for row in result:
        dizionario = dict()
        dizionario["n_sala"] = row["n_sala"]
        dizionario["durata_media"] = row["durata_media"]
        dict_list.append(dizionario)
    return dict_list
