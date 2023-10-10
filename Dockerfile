FROM python:3.9.10-slim-buster
WORKDIR /app
COPY requirements.txt /app
# We copy just the requirements.txt first to leverage Docker cache
RUN apt-get update 
RUN apt-get install -y libxrender1 libfontconfig1 libjpeg62-turbo libxtst6
# RUN apt-get install -y wkhtmltopdf

RUN apt-get install wget
RUN wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
RUN tar xvf wkhtmltox*.tar.xz
RUN mv wkhtmltox/bin/wkhtmlto* /usr/bin
RUN apt-get install -y openssl build-essential libssl-dev libxrender-dev git-core libx11-dev libxext-dev libfontconfig1-dev libfreetype6-dev fontconfig



RUN apt-get install -y libqt5webkit5
RUN apt --fix-broken install
RUN apt install -y binutils
RUN apt-get install -y build-essential python3-dev
RUN pip install pdfkit
RUN pip install flask
RUN pip install flask-cors
RUN pip install --upgrade pip
RUN pip install python-dotenv
RUN pip install PyJWT
RUN apt-get install -y swig
RUN pip install --no-cache-dir setuptools
RUN pip install --verbose --no-cache-dir -r requirements.txt
RUN pip install Pillow
RUN strip --remove-section=.note.ABI-tag /usr/lib/x86_64-linux-gnu/libQt5Core.so.5

COPY . /app
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]