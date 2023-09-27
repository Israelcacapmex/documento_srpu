from flask import Flask
from flask_cors import CORS

from controllers.pdf_corto_plazo import pdf_corto
from controllers.pdf_largo_plazo import pdf_largo
from controllers.pdf_requerimientos import pdf_requerimientos

app = Flask(__name__)
CORS(app)

app.register_blueprint(pdf_corto)
app.register_blueprint(pdf_largo)
app.register_blueprint(pdf_requerimientos)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000, debug= True)