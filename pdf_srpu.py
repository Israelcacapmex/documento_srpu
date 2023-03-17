import jinja2
import pdfkit
from datetime import datetime
from flask import Flask, request, send_file, Response
from flask_cors import CORS
from pathlib import Path
from os import remove
import os
import glob
import json
from pathlib import Path
from PyPDF2 import  PdfReader
import copy

app = Flask(__name__)
CORS(app)

@app.route('/documento_srpu',  methods=['POST'])

def get_data():
    for pdf in glob.iglob('*.pdf', recursive=True):#Elimina los documentos pdf para borrar el cache 
         os.remove(pdf)
    data = request.data
    data = json.loads(data)
    print(request.data)
    return documento(data)

def documento(data):

    #data =  data["body"]
    nombre = data["nombre"]
    oficionum = data["oficionum"]
    cargo = data["cargo"]
    organismo = data["organismo"]
    InstitucionBancaria = data["InstitucionBancaria"]
    monto = data["monto"]
    fechacontrato = data["fechacontrato"]
    destino = data["destino"]
    dias = data["dias"]
    fechavencimiento = data["fechavencimiento"]
    # entepublicoobligado = data["entepublicoobligado"]
    # tasadeinteres = data["tasadeinteres"]

    #comisiones

    today_date = datetime.today().strftime("%d %b, %Y")
    template_loader = jinja2.FileSystemLoader(searchpath='./')
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template('./templates/template.html')

    info ={"num":"10", "fecha":today_date, "nombre":nombre, "cargo":cargo, "organismo":organismo, 
           "fechacontrato":fechacontrato, "InstitucionBancaria":InstitucionBancaria, "monto":monto,
           "fechavencimiento":fechavencimiento, "destino":destino, "dias":dias, "oficionum":oficionum,
           #"entepublicoobligado":entepublicoobligado, "tasadeinteres":tasadeinteres, 
               }

  
    output_text = template.render(info)



    
    
    config = pdfkit.configuration(wkhtmltopdf="C://Users//hp//Downloads//wkhtmltopdf//bin//wkhtmltopdf.exe")
    pdfkit.from_string(output_text, 'srpu_document.pdf', configuration=config) 


    pdf = open('srpu_document.pdf', 'rb')
    print("hola")
    
    # filename = Path('srpu_document.pdf')
    # filename.write_bytes(pdf)
    # print(filename)
    # filename.seek(0)

    return send_file(pdf, as_attachment=True, mimetype="application/pdf", download_name="documento_srpu.pdf")#regresa el documento para su descarga

    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000, debug= True)