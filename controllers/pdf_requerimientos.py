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
from flask import (Blueprint, Flask, Response, make_response, render_template,
                   request, send_file)
from flask_cors import CORS


load_dotenv()

pdf_requerimientos = Blueprint('pdf_requerimientos', __name__)
Variable_entorno = os.environ.get('Variable_entorno')
debug_mode = os.environ.get('DEBUG')


CORS(pdf_requerimientos)
@pdf_requerimientos.route('/documento_srpu_requerimientos',  methods=['POST'])

def get_data():
    for pdf in glob.iglob('*.pdf', recursive=True):
         os.remove(pdf)
        
    data = request.data
    data = json.loads(data)
    
    return documento(data)


def documento(data):
    oficioRequerimiento = data["oficioRequerimiento"]
    servidorPublico = data["servidorPublico"]
    cargo = data["cargo"]
    organismo = data["organismo"]
    oficioSolicitud = data["oficioSolicitud"]
    fechaSolicitud = data["fechaSolicitud"]
    fechaContratacion = data["fechaContratacion"]
    entePublicoObligado = data["entePublicoObligado"]
    institucionFinanciera = data["institucionFinanciera"]
    montoOriginalContratado = data["montoOriginalContratado"]
    comentarios = data["comentarios"]
    directorGeneral = data["directorGeneral"]
    cargoDirectorGeneral = data["cargoDirectorGeneral"]

    template_loader = jinja2.FileSystemLoader(searchpath='./')
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template('./templates/template_requerimientos.html')



    info ={
        "oficioRequerimiento" : oficioRequerimiento,
        "servidorPublico" : servidorPublico,
        "cargo" : cargo,
        "organismo" : organismo,
        "oficioSolicitud" : oficioSolicitud,
        "fechaSolicitud" : fechaSolicitud,
        "fechaContratacion" : fechaContratacion,
        "entePublicoObligado" : entePublicoObligado,
        "institucionFinanciera" : institucionFinanciera,
        "montoOriginalContratado" : montoOriginalContratado,
        "directorGeneral" : directorGeneral,
        "cargoDirectorGeneral" : cargoDirectorGeneral,
        "comentarios":comentarios 
        }

  
    output_text = template.render(info)

    options={
        "enable-local-file-access": "",
        'page-size': 'Letter',
        'margin-top': '0.90in',
        'margin-right': '0.50in',
        'margin-bottom': '0.90in',
        'margin-left': '0.5in',
        'encoding': "UTF-8",
        'javascript-delay' : '550',
        'enable-internal-links': '',
        'header-html': './templates/header.html',#Modifique aqui
        'footer-html': './templates/footer.html',#Modifique aqui
        'footer-right': "Página [page] de [topage]",
        'footer-font-size': "7",
        'no-outline': None}
    

  
    config = pdfkit.configuration(wkhtmltopdf=Variable_entorno)
    pdf_file = pdfkit.from_string(output_text, 'sgcm_requerimientos.pdf', #agregue aqui la prueba
                                  configuration=config, 
                                  options= options,
                                      )

    

    pdf = open('sgcm_requerimientos.pdf', 'rb').read()
    

    return Response(
        pdf,
        mimetype="application/pdf",
        headers={
            "Content-disposition": "attachment; filename=" + "sgcm_requerimientos.pdf",
            "Content-type": "application/force-download"
        }
    ) 
