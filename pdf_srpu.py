import copy
import glob
import io
import json
import os
from datetime import datetime
from os import remove
from pathlib import Path

import jinja2
import pdfkit
from dotenv import load_dotenv
from flask import Blueprint, Flask, Response, request, send_file
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)

pdf_corto = Blueprint('pdf_corto', __name__)
Variable_entorno = os.environ.get('Variable_entorno')
debug_mode = os.environ.get('DEBUG')


CORS(pdf_corto)
@pdf_corto.route('/documento_srpu',  methods=['POST'])

def get_data():
    for pdf in glob.iglob('*.pdf', recursive=True):#Elimina los documentos pdf para borrar el cache 
         os.remove(pdf)
        
    data = request.data
    data = json.loads(data)
    #print("Entre al servicio")
    return documento(data)

def documento(data):
    #print("data: ",data)
    nombre = data["nombre"]
    oficionum = data["oficionum"]
    cargo = data["cargoServidorPublicoSolicitante"]
    organismo = data["organismo"]
    InstitucionBancaria = data["InstitucionBancaria"]
    monto = data["monto"]
    fechaContrato = data["fechaContrato"]
    destino = data["destino"]
    dias = data["dias"]
    fechaVencimiento = data["fechaVencimiento"]
    
    tipoEntePublicoObligado = data["tipoEntePublicoObligado"]
    tipocomisiones = data["tipocomisiones"]
    tasaefectiva = data["tasaefectiva"]
    servidorpublico = data["servidorpublico"]
    contrato = data["contrato"]
    periodopago = data["periodoPago"] 
    organoDeGobierno = data["organismo"]
    obligadoSolidarioAval = data["obligadoSolidarioAval"]
    reglas = data["reglas"]
    tasadeInteres = data["tasaInteres"]
    Documentos = data["Documentos"]
    print(Documentos)

    if "organismo" in data == '' :
        entepublicoobligado = data["organismo"] 
        #entepublicoobligado = 'No aplica'
    else:
       entepublicoobligado = data["organismo"]   
    

    #if entepublicoobligado == '' :
     #       entepublicoobligado = 'No aplica'
        
    if tipoEntePublicoObligado =='':
            tipoEntePublicoObligado ='No aplica'

    
    

    today_date = datetime.today().strftime("%d %b, %Y")
    template_loader = jinja2.FileSystemLoader(searchpath='./')
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template('./templates/template_corto.html')

    info ={"num":"10", "fecha":today_date, "nombre":nombre, "cargo":cargo, "organismo":organismo, 
            "fechacontrato":fechaContrato, "InstitucionBancaria":InstitucionBancaria, "monto":monto,
            "fechavencimiento":fechaVencimiento, "destino":destino, "dias":dias, "oficionum":oficionum,
            "entepublicoobligado":entepublicoobligado, "tasadeinteres":tasadeInteres, "organodegobierno":organismo,
            "servidorpublico":servidorpublico, "contrato":contrato, "periodopago": periodopago, "obligadoSolidarioAval":obligadoSolidarioAval,
             "reglas":reglas, "tipocomisiones":tipocomisiones, "tasaefectiva":tasaefectiva,"tipoEntePublicoObligado": tipoEntePublicoObligado ,"Documentos":Documentos  }

  
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
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000, debug= True)