FROM python:3.9.10-slim-buster
WORKDIR /app
COPY requirements.txt /app

# We copy just the requirements.txt first to leverage Docker cache
# RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y \
    libxrender1 \
    libxext6 \
    libssl-dev \
    libfontconfig1 \
    libfreetype6 \
    libjpeg62-turbo \
    libx11-6 \
    libxcb1 \
    libx11-xcb1 \
    libxcb1 \
    libxau6 \
    libxdmcp6 \
    libbsd0 \
    libharfbuzz0b \
    libfreetype6 \
    libpng16-16 \
    libxslt1.1 \
    libicu57

# Download and install wkhtmltopdf with patched Qt
RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.4-2/wkhtmltox_0.12.4-2.bionic_amd64.deb
RUN dpkg -i wkhtmltox_0.12.4-2.bionic_amd64.deb
RUN apt-get install -f

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