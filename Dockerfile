FROM python:3.9.10-slim-buster
WORKDIR /app
COPY requirements.txt /app
# We copy just the requirements.txt first to leverage Docker cache
RUN apt-get update 
RUN apt-get install -y libxrender1 libfontconfig1 libjpeg62-turbo libxtst6
RUN apt-get install -y wkhtmltopdf
RUN apt-get install -y build-essential python3-dev
RUN pip install pdfkit
RUN pip install --upgrade pip
RUN pip install python-dotenv
RUN pip install PyJWT
RUN apt-get install -y swig
RUN pip install --no-cache-dir setuptools
RUN pip install --verbose --no-cache-dir -r requirements.txt
RUN pip install Pillow
RUN pip install -U flask-cors
COPY . /app
ENTRYPOINT [ "python" ]
CMD [ "pdf_srpu.py" ]