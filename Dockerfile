FROM python:3.9.10-slim-buster
WORKDIR /app
COPY requirements.txt /app

# We copy just the requirements.txt first to leverage Docker cache
# RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y wget build-essential cmake libssl-dev libfontconfig1 libxrender1 libjpeg62-turbo xorg-dev libx11-dev libxcb1-dev libxtst6 libxext6 libfreetype6 libxml2 libicu-dev libxslt1-dev


# Download and install wkhtmltopdf with patched Qt
RUN wget https://github.com/wkhtmltopdf/packaging/archive/master.tar.gz -O packaging.tar.gz
RUN tar -xvf packaging.tar.gz
# WORKDIR /app/packaging-master
# RUN bash build.py

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