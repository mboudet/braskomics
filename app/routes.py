import json
import time
from functools import wraps
from SPARQLWrapper import SPARQLWrapper, JSON

from flask import Blueprint, abort, current_app, jsonify, redirect, render_template, request, session, url_for

app = Blueprint('app', __name__, url_prefix='/')


@app.route('/')
@app.route('/index')
def index():
    sparql = SPARQLWrapper("http://0.0.0.0:80/virtuoso/sparql")
    sparql.setQuery("""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT DISTINCT ?label WHERE {
            ?gene1_uri rdf:type <http://askomics.org/data/gene> . ?gene1_uri rdfs:label ?label .
        }
        LIMIT 10
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    return render_template('home.html', title='Home', data=results["results"]["bindings"])


@app.route('/groups/view/<id>', methods=['GET', 'POST'])
def view_group(id):
    pass


@app.route('/groups/create', methods=['GET', 'POST'])
def create_group():
    pass

@app.route('/groups/<group_id>/add_orga_access/<orga_id>', methods=['GET', 'POST'])
def add_orga_group(group_id, orga_id):
    pass
