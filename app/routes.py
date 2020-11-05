import json
import time
from flask import request
from functools import wraps
from SPARQLWrapper import SPARQLWrapper, JSON

from flask import Blueprint, abort, current_app, jsonify, redirect, render_template, request, session, url_for

app = Blueprint('app', __name__, url_prefix='/')


@app.route('/')
@app.route('/index')
def index():

    results = get_genes(count=request.args.get('count'))
    return render_template('home.html', title='Home', data=results["results"]["bindings"])

@app.route('/genes/<id>', methods=['GET'])
def get_gene_pathways(id):
    data = get_gene_data(id)
    return render_template('gene.html', title='Gene reactions', data=data, gene=id)

@app.route('/genes_ortho/<id>', methods=['GET'])
def get_gene_ortho_pathways(id):
    data = get_gene_ortholog_data(id)
    return render_template('gene_ortho.html', title='Gene orthologs reactions', data=data, gene=id)


@app.route('/gene-autocomplete', methods=['GET'])
def gene_autocomplete():
    results = get_genes(start=request.args.get('term'))
    data = [gene['label']['value'] for gene in results["results"]["bindings"]]
    return jsonify(data)

def get_genes(count=0, start=""):
    sparql = SPARQLWrapper(current_app.config["SPARQL_ENDPOINT"])
    start_query = ""
    if start:
        # Meh...
        start = start.lower()
        start_query = "FILTER(strstarts(lcase(str(?label)), '{}'))".format(start)
    count_query = ""
    if count:
        count_query = "OFFSET {}".format(count)

    query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT DISTINCT ?label WHERE {
            ?gene1_uri rdf:type <http://askomics.org/data/gene> . ?gene1_uri rdfs:label ?label .
            %s
        }
        LIMIT 10
        %s
    """ % (start_query, count_query)

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    return results


# Get all results? Might take some time? -> Paginate?
def get_gene_data(gene_id):
    sparql = SPARQLWrapper(current_app.config["SPARQL_ENDPOINT"])

    sparql.setQuery("""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT DISTINCT ?gene1_Label ?reaction1_Label ?pathway1_Label ?pathway1_COMMON_NAME WHERE {
            ?rxn_gene_recData16_uri <http://askomics.org/data/is_linked_to> ?gene1_uri .
            ?rxn_gene_recData16_uri <http://askomics.org/data/concerns> ?reaction25_uri .
            ?rxn_pwy61_uri <http://askomics.org/data/concerns> ?reaction25_uri .
            ?rxn_pwy61_uri <http://askomics.org/data/is_included_in> ?pathway80_uri .
            ?gene1_uri rdf:type <http://askomics.org/data/gene> .
            ?gene1_uri rdfs:label ?gene1_Label .
            ?rxn_gene_recData16_uri rdf:type <http://askomics.org/data/rxn_gene_recData> .
            ?reaction25_uri rdf:type <http://askomics.org/data/reaction> .
            ?reaction25_uri rdfs:label ?reaction1_Label .
            ?rxn_pwy61_uri rdf:type <http://askomics.org/data/rxn_pwy> .
            ?pathway80_uri rdf:type <http://askomics.org/data/pathway> .
            ?pathway80_uri rdfs:label ?pathway1_Label .
            ?pathway80_uri <http://askomics.org/data/COMMON-NAME> ?pathway1_COMMON_NAME .
            VALUES ?gene1_Label { '%s' } .
        } """ % (gene_id))

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results["results"]["bindings"]

def get_gene_ortholog_data(gene_id):
    sparql = SPARQLWrapper(current_app.config["SPARQL_ENDPOINT"])
    sparql.setQuery("""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT DISTINCT ?gene1_Label ?gene2_Label ?reaction1_Label WHERE {
            ?gene203_uri <http://askomics.org/data/ortholog_of> ?gene1_uri .
            ?rxn_gene_recData302_uri <http://askomics.org/data/is_linked_to> ?gene203_uri .
            ?rxn_gene_recData302_uri <http://askomics.org/data/concerns> ?reaction311_uri .
            ?gene1_uri rdf:type <http://askomics.org/data/gene> .
            ?gene1_uri rdfs:label ?gene1_Label .
            ?gene203_uri rdf:type <http://askomics.org/data/gene> .
            ?gene203_uri rdfs:label ?gene2_Label .
            ?rxn_gene_recData302_uri rdf:type <http://askomics.org/data/rxn_gene_recData> .
            ?reaction311_uri rdf:type <http://askomics.org/data/reaction> .
            ?reaction311_uri rdfs:label ?reaction1_Label .
            VALUES ?gene1_Label { '%s' } .
        }""" % (gene_id))
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results["results"]["bindings"]
