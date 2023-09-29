import copy
import glob
import io
import json
import os
from datetime import datetime
from pathlib import Path

import jinja2
import pdfkit
from dotenv import load_dotenv
from flask import Blueprint, Flask, Response, request, send_file, render_template, make_response
from flask_cors import CORS


import tempfile

load_dotenv()

pdf_requerimientos = Blueprint('pdf_requerimientos', __name__)
Variable_entorno = os.environ.get('Variable_entorno')
debug_mode = os.environ.get('DEBUG')


CORS(pdf_requerimientos)
@pdf_requerimientos.route('/documento_srpu_requerimientos',  methods=['POST'])

def get_data():
    print(request)
    for pdf in glob.iglob('*.pdf', recursive=True):#Elimina los documentos pdf para borrar el cache 
         os.remove(pdf)
        
    data = request.data
    data = json.loads(data)
    
    return documento(data)


def documento(data):
    servidorPublico = data["servidorPublico"]
    cargo = data["cargo"]
    organismo = data["organismo"]
    oficioSolicitud = data["oficioSolicitud"]
    fechaSolicitud = data["fechaSolicitud"]
    entidad = data["entidad"]
    institucionBancaria = data["institucionBancaria"]
    fechaContrato = data["fechaContrato"]
    monto = data["monto"]
    comentarios = data["comentarios"]

    template_loader = jinja2.FileSystemLoader(searchpath='./')
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template('./templates/template_requerimientos.html')



    info ={
        "servidorPublico":servidorPublico, 
        "cargo":cargo, 
        "organismo":organismo, 
        "oficioSolicitud":oficioSolicitud, 
        "fechaSolicitud":fechaSolicitud, 
        "entidad":entidad, 
        "institucionBancaria":institucionBancaria, 
        "fechaContrato":fechaContrato, 
        "monto":monto, 
        "comentarios":comentarios, }

  
    output_text = template.render(info)

    options={
        "enable-local-file-access": "",
        'page-size': 'Letter',
        'margin-top': '0.50in',
        'margin-right': '0.50in',
        'margin-bottom': '0.50in',
        'margin-left': '0.5in',
        'encoding': "UTF-8",
        'javascript-delay' : '550',
        'footer-center': "Edificio Víctor Gómez Garza Gral. Mariano Escobedo 333 Zona Centro Monterrey, Nuevo León \n C.P. 64000   Tel: (55) 8120201300   https://www.nl.gob.mx/tesoreria",
        'footer-right': "Página [page] de [topage]",
        'footer-font-size': "7",
        'no-outline': None}
    
    add_pdf_header(options, bar)
    add_pdf_footer(options)

  
    config = pdfkit.configuration(wkhtmltopdf=Variable_entorno)
    pdf_file = pdfkit.from_string(output_text, 'srpu_document.pdf', 
                                  configuration=config, 
                                  options= options,
                                      ) 

    

    pdf = open('srpu_document.pdf', 'rb').read()
    

    return Response(
        pdf,
        mimetype="application/pdf",
        headers={
            "Content-disposition": "attachment; filename=" + "srpu_document.pdf",
            "Content-type": "application/force-download"
        }
    ) 

def add_pdf_header(options, bar):
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as header:
        options['--header-html'] = header.name
        header.write(
            render_template('header.html', bar=bar).encode('utf-8')
        )
    return

def add_pdf_footer(options):
    # same behaviour as add_pdf_header but without passing any variable
    return