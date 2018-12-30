Bootstrap_base
Everything connected to flask-bootstrap

usage:
- manager:
python vlab.py runserver -d # to run server
python vlab.py shell # for interactive session

- migration in flask (command line)
export FLASK_APP=vlab
flask db migrate -m "migration name"
flask db upgrade

- allow acces to apps in you Gmail security setting for mail sending