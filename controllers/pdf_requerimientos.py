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
from flask import Blueprint, Flask, Response, request, send_file
from flask_cors import CORS

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
    #print("Entre al servicio")
    return documento(data)

def documento(data):
    print(data)
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
    

    # if "organismo" in data == '' :
    #     entepublicoobligado = data["organismo"] 
    #     #entepublicoobligado = 'No aplica'
    # else:
    #    entepublicoobligado = data["organismo"]  

    today_date = datetime.today().strftime("%d %b, %Y")
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

  
    config = pdfkit.configuration(wkhtmltopdf=Variable_entorno)
    pdf_file = pdfkit.from_string(output_text, 'srpu_document.pdf', configuration=config, options={"enable-local-file-access": "",'page-size': 'Letter',
                    'margin-top': '0.50in',
                    'margin-right': '0.50in',
                    'margin-bottom': '0.50in',
                    'margin-left': '0.5in',
                    'encoding': "UTF-8",
                    'javascript-delay' : '550',
                    'no-outline': None}) 

    

    pdf = open('srpu_document.pdf', 'rb').read()
    

    return Response(
        pdf,
        mimetype="application/pdf",
        headers={
            "Content-disposition": "attachment; filename=" + "srpu_document.pdf",
            "Content-type": "application/force-download"
        }
    ) 
    
#send_file(pdf, as_attachment=True, mimetype="application/pdf", download_name="documento_srpu.pdf")#regresa el documento para su descarga
    #response, 200, {
    #     'Content-Type': 'application/pdf',
    #     'Content-Disposition': 'inline; filename="name_of_file.pdf"'} 
    # bytes(bytes_file), 200, {
    # 'Content-Type': 'application/pdf',
    # 'Content-Disposition': 'inline; filename="nameofyourchoice.pdf"'}
#

    
