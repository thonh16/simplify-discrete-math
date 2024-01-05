# pyinstaller -p . -w -F --add-data "templates:templates" --add-data "static:static" --clean app.py

docker run --rm -v "${PWD}:/code" -e PYTHONHASHSEED=42 coopermaa/pyinstaller -p . -w -F --add-data "templates:templates" --add-data "static:static" app.py
