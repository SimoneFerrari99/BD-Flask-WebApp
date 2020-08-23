# Progetto basi di dati 2020 - Tema Cinema
# Gruppo: ArceCity
# Membri: Casarotti Giulio, Ferrari Simone, Trolese Gulio

# File: admin_route.py
# Descrizione: applicazione principale
#---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---#
from flask import Flask, Blueprint, render_template, url_for, redirect, request, session, flash
from sqlalchemy import create_engine, MetaData, Table, select

admin_app = Blueprint('admin_app', __name__)

@admin_app.route('/admin', methods=['GET', 'POST'])
def admin():

        return render_template('registrazione.html', errore=False)
