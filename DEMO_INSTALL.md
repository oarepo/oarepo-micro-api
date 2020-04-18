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
