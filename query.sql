--Numero di film:
select count(*) as numfilm
from film;


--Film con più proiezioni:
create or replace view numero_proiezioni_per_film(id_film, num_proiezioni) as
select id_film, count(id_proiezione)
from film left join proiezioni on film.id_film = proiezioni.film
group by id_film;

select *
from film f natural join numero_proiezioni_per_film n
where n.num_proiezioni = (select max(num_proiezioni)
                          from numero_proiezioni_per_film);


--Film con più posti prenotati totali:
create or replace view numero_posti_totali_prenotati_per_film(id_film, num_posti) as
select pr.film, count(po.id_posto)
from proiezioni pr natural join posti po
group by pr.film;

select *
from film f natural join numero_posti_totali_prenotati_per_film n
where n.num_posti = (select max(num_posti)
                  from numero_posti_totali_prenotati_per_film);


--Film con più incassi totali:
create or replace view incasso_per_ogni_film(id_film, incasso) as
select film, sum(prezzo)
from proiezioni natural join posti
group by film;

select *
from film f natural join incasso_per_ogni_film n
where n.incasso = (select max(incasso)
                  from incasso_per_ogni_film);

-------------------------------------------------------------------------------------------------------------
--Genere con più posti prenotati:
create or replace view numero_posti_totali_prenotati_e_incasso_per_genere(tipo_genere, num_posti, incasso) as
select gf.tipo_genere, count(po.id_posto), sum(po.prezzo)
from proiezioni pr natural join posti po join film f on pr.film = f.id_film natural join genere_film gf
group by gf.tipo_genere;

select *
from numero_posti_totali_prenotati_e_incasso_per_genere n
where n.num_posti = (select max(num_posti)
                  from numero_posti_totali_prenotati_e_incasso_per_genere);

--Genere con più incassi:
select *
from numero_posti_totali_prenotati_e_incasso_per_genere n
where n.incasso = (select max(incasso)
                  from numero_posti_totali_prenotati_e_incasso_per_genere);

-------------------------------------------------------------------------------------------------------------
--Numero di proiezioni totale
select count(*) as numproiezioni
from proiezioni;

--Proiezione più prenotata:
create or replace view numero_posti_prenotati_e_incasso_per_proiezione(id_proiezione, id_film, num_posti, incasso) as
select pr.id_proiezione, pr.film, count(po.id_posto), sum(po.prezzo)
from proiezioni pr natural join posti po
group by pr.id_proiezione, pr.film;

select *
from film f natural join numero_posti_prenotati_e_incasso_per_proiezione n
where n.num_posti = (select max(num_posti)
                  from numero_posti_prenotati_e_incasso_per_proiezione);

--Proiezione con l'incasso più alto:
select *
from film f natural join numero_posti_prenotati_e_incasso_per_proiezione n
where n.incasso = (select max(incasso)
                  from numero_posti_prenotati_e_incasso_per_proiezione);

--Orario in cui ci sono state più prenotazioni
create or replace view numero_posti_prenotati_per_orario(ora_inizio, num_posti) as
select pr.ora_inizio, count(po.id_posto)
from proiezioni pr natural join posti po
group by pr.ora_inizio;

select *
from numero_posti_prenotati_per_orario n
where n.num_posti = (select max(num_posti)
                  from numero_posti_prenotati_per_orario);

-------------------------------------------------------------------------------------------------------------
--Attore che appare in più film
create or replace view attori_film(id_persona, num_film) as
select a.id_persona, count(f.id_film)
from attori a natural join film f
group by a.id_persona;

select *
from persone natural join attori_film n
where n.num_film = (select max(num_film)
                    from attori_film);


--Regista che ha diretto più film
create or replace view registi_film(id_persona, num_film) as
select r.id_persona, count(f.id_film)
from registi r natural join film f
group by r.id_persona;

select *
from persone natural join registi_film n
where n.num_film = (select max(num_film)
                    from registi_film);
-------------------------------------------------------------------------------------------------------------
--Numero di clienti iscritti
select count(*) as numutenti
from utenti
where not is_admin and not is_manager;

--Numero di posti prenotati in media da un utente
create or replace view utente_prenotazioni(email, num_prenotazioni) as
select u.email, count(po.id_posto)
from posti po join utenti u on po.prenotato = u.email
group by u.email;

select avg(num_prenotazioni) as num_prenotazioni_media
from utente_prenotazioni;

--Età media utenti
create or replace view utente_eta(email, eta) as
select u.email, (current_date-u.data_nascita)/365.25
from utenti u
group by u.email;

select avg(eta) as eta_media
from utente_eta;
-------------------------------------------------------------------------------------------------------------
--Numero proiezioni per sala
select n_sala, count(*) as num_proiezioni
from proiezioni pr join sale s on pr.sala = s.n_sala
group by n_sala
order by n_sala;

--Durata media dei film per sala
create or replace view sala_film_durata(n_sala, num_film, tot_durata) as
select s.n_sala, count(f.id_film), sum(f.durata)
from sale s join proiezioni pr on s.n_sala = pr.sala join film f on pr.film = f.id_film
group by s.n_sala;

select n_sala, tot_durata / num_film as durata_media
from sala_film_durata
order by n_sala;
