# Progetto basi di dati 2020 - Tema Cinema
# Gruppo: ArceCity
# Membri: Casarotti Giulio, Ferrari Simone, Trolese Gulio

# File: user_route.py
# Descrizione: applicazione principale
#---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---#
from flask import Flask, Blueprint, render_template, url_for, redirect, request, session, flash
from sqlalchemy import create_engine, MetaData, Table, select

user_app = Blueprint('user_app', __name__)

@user_app.route('/biglietti', methods=['GET', 'POST'])
def biglietti():

        return render_template('registrazione.html', errore=False)
