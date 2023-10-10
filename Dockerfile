FROM python:3.9.10-slim-buster
WORKDIR /app
COPY requirements.txt /app
# We copy just the requirements.txt first to leverage Docker cache

RUN apt-get update -y && apt-get install -y wget xvfb libfontconfig1 libxrender1
RUN wget -q -O wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox-0.12.6-1.centos8.x86_64.rpm
RUN ln -s /usr/local/bin/wkhtmltopdf /usr/bin

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
# RUN strip --remove-section=.note.ABI-tag /usr/lib/x86_64-linux-gnu/libQt5Core.so.5

COPY . /app
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]