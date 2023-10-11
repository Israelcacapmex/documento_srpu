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

load_dotenv()

header_path = os.path.abspath('./templates/header.html')
footer_path = os.path.abspath('./templates/footer.html')

pdf_constancia = Blueprint('pdf_constancia', __name__)
Variable_entorno = os.environ.get('Variable_entorno')
debug_mode = os.environ.get('DEBUG')


CORS(pdf_constancia)
@pdf_constancia.route('/documento_srpu_constancia',  methods=['POST'])

def get_data():
    print(request)
    for pdf in glob.iglob('*.pdf', recursive=True):
         os.remove(pdf)
        
    data = request.data
    data = json.loads(data)
    
    return documento(data)


def documento(data):
    oficioConstancia = data["oficioConstancia"]
    servidorPublico = data["servidorPublico"]
    cargo = data["cargo"]
    organismo = data["organismo"]
    oficioSolicitud = data["oficioSolicitud"]
    fechaSolicitud = data["fechaSolicitud"]
    tipoDocumento = data["tipoDocumento"]
    fechaContratacion = data["fechaContratacion"]
    claveInscripcion = data["claveInscripcion"]
    fechaClave = data["fechaClave"]
    entePublicoObligado = data["entePublicoObligado"]
    obligadoSolidarioAval = data["obligadoSolidarioAval"]
    institucionFinanciera = data["institucionFinanciera"]
    montoOriginalContratado = data["montoOriginalContratado"]
    destino = data["destino"]
    plazo = data["plazo"]
    amortizaciones = data["amortizaciones"]
    tasaInteres = data["tasaInteres"]
    tasaEfectiva = data["tasaEfectiva"]
    mecanismoVehiculoDePago = data["mecanismoVehiculoDePago"]
    fuentePago = data["fuentePago"]
    garantiaDePago = data["garantiaDePago"]
    instrumentoDerivado = data["instrumentoDerivado"]
    financiamientosARefinanciar = data["financiamientosARefinanciar"]
    directorGeneral = data["directorGeneral"]
    cargoDirectorGeneral = data["cargoDirectorGeneral"]

    template_loader = jinja2.FileSystemLoader(searchpath='./')
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template('./templates/template_constancia.html')



    info = {
        "oficioConstancia" : oficioConstancia,
        "servidorPublico" : servidorPublico,
        "cargo" : cargo,
        "organismo" : organismo,
        "oficioSolicitud" : oficioSolicitud,
        "fechaSolicitud" : fechaSolicitud,
        "tipoDocumento" : tipoDocumento,
        "fechaContratacion" : fechaContratacion,
        "claveInscripcion" : claveInscripcion,
        "fechaClave" : fechaClave,
        "entePublicoObligado" : entePublicoObligado,
        "obligadoSolidarioAval" : obligadoSolidarioAval,
        "institucionFinanciera" : institucionFinanciera,
        "montoOriginalContratado" : montoOriginalContratado,
        "destino" : destino,
        "plazo" : plazo,
        "amortizaciones" : amortizaciones,
        "tasaInteres" : tasaInteres,
        "tasaEfectiva" : tasaEfectiva,
        "mecanismoVehiculoDePago" : mecanismoVehiculoDePago,
        "fuentePago" : fuentePago,
        "garantiaDePago" : garantiaDePago,
        "instrumentoDerivado" : instrumentoDerivado,
        "financiamientosARefinanciar" : financiamientosARefinanciar,
        "directorGeneral" : directorGeneral,
        "cargoDirectorGeneral" : cargoDirectorGeneral
        }

  
    output_text = template.render(info)

    options={
        "enable-local-file-access": "",
        'page-size': 'Letter',
        # 'margin-top': '1in',
        'margin-right': '0.50in',
        # 'margin-bottom': '1in',
        'margin-left': '0.5in',
        'encoding': "UTF-8",
        'javascript-delay' : '550',
        'header-html': header_path, #Modifique aqui
        'footer-html': footer_path, #Modifique aqui
        'footer-right': "Página [page] de [topage]",
        'footer-font-size': "7",
        'no-outline': None
        }
    

  
    config = pdfkit.configuration(wkhtmltopdf=Variable_entorno)
    pdfkit.from_string(output_text, 'sgcm_constancia.pdf', #agregue aqui la prueba
                                  configuration=config, 
                                  options= options,
                                      ) 

    

    pdf = open('sgcm_constancia.pdf', 'rb').read()
    

    return Response(
        pdf,
        mimetype="application/pdf",
        headers={
            "Content-disposition": "attachment; filename=" + "sgcm_constancia.pdf",
            "Content-type": "application/force-download"
        }
    ) 
