# DEMO local Installation

```bash
git clone git@github.com:oarepo/oarepo-micro-api.git

pipenv install
pipenv shell
pip install -e .

INSTANCE_DIR=$VIRTUAL_ENV/var/instance
```

## Docker

## No docker

In case your elasticsearch / database is not in docker

```bash

sudo -u postgres createuser oarepo-micro-api -P -l
sudo -u postgres createdb oarepo-micro-api -O oarepo-micro-api


mkdir -p $INSTANCE_DIR
cat >${INSTANCE_DIR}/invenio.cfg <<'EOF'
SEARCH_ELASTIC_HOSTS = [
    dict(host='127.0.0.1', port=9207),
]

SQLALCHEMY_DATABASE_URI = \
    'postgresql+psycopg2://oarepo-micro-api:oarepo-micro-api@localhost:5433/oarepo-micro-api'
EOF
```

## Initialization and demo data

```bash
invenio index init
invenio db create

mkdir -p ${INSTANCE_DIR}/data
invenio files location --default 'default-location' ${INSTANCE_DIR}/data

invenio demo data
```

## Debug run


```bash
export FLASK_DEBUG=true
export SERVER_NAME=127.0.0.1:5000
export FLASK_APP=oarepo_micro_api.wsgi:application
invenio run
```

An check in browser that all links point to ```/api/```:

```json5
// http://127.0.0.1:5000/api/records/
{
   aggregations: { },
   hits: {
      // a lot of stuff here
   },
   links: {
      next: "http://127.0.0.1:5000/api/records/?size=10&page=2",
      self: "http://127.0.0.1:5000/api/records/?size=10&page=1"
   }
}
```

## UWSGI run

```bash

uwsgi --ini uwsgi.ini -H $VIRTUAL_ENV

```

Make the same request and check that URLs stay the same.
