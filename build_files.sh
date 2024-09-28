apt upgrade && apt update
apt insall postgresql libpq-dev

pip install -r requirements.txt
python3.9 manage.py collectstatic