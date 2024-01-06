FROM stevenacoffman/pyinstaller-alpine

RUN pip install --upgrade setuptools
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt