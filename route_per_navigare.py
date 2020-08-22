# Progetto basi di dati 2020 - Tema Cinema
# Gruppo: ArceCity
# Membri: Casarotti Giulio, Ferrari Simone, Trolese Gulio

# File: app.py
# Descrizione: applicazione principale
#---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---#
from flask import Flask, render_template, url_for, redirect, request, session, flash
from sqlalchemy import create_engine, MetaData, Table, select
