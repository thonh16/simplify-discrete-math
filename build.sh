# pyinstaller -p . -w -F --add-data "templates:templates" --add-data "static:static" --clean app.py

docker run --rm -v "${PWD}:/src" -e PYTHONHASHSEED=42 stevenacoffman/pyinstaller-alpine -p . -w -F --add-data "templates:templates" --add-data "static:static" app.py
