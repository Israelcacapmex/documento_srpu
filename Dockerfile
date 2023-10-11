FROM python:3.9.10-slim-buster
WORKDIR /app
COPY requirements.txt /app
# We copy just the requirements.txt first to leverage Docker cache
# RUN apt-get update 
# RUN apt-get install -y libxrender1 libfontconfig1 libjpeg62-turbo libxtst6
# RUN apt-get install -y wkhtmltopdf

# RUN apt-get install -y libqt5webkit5

RUN apt-get update && apt-get install -y \
    xz-utils \
    libfontconfig1 \
    libxrender1 \
    wget \
    gdebi-core 
RUN apt-get install libjpeg62-dev
RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.focal_amd64.deb
RUN gdebi --n wkhtmltox_0.12.6-1.focal_amd64.deb

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