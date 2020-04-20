# Local development

Install the dependencies:
```bash
git clone git@github.com:oarepo/oarepo-micro-api.git
mkvirtualenv --python=/usr/bin/python3 oarepo-micro-api

./scripts/bootstrap
```

In case your db is not in docker, create the following user and database:
```bash
sudo -u postgres createuser oarepo-micro-api -P -l
sudo -u postgres createdb oarepo-micro-api -O oarepo-micro-api
```

Otherwise, run the minimal infrastructure in docker:
```bash
docker-compose -f docker-compose.min.yml up -d
```

Setup the Invenio instance. This will create all the DB tables and ES mappings and fill
database with demo data:
```bash
./scripts/setup
```

Run the invenio server:
```bash
# Run in invenio built-in server
./scripts/server

# --or--

# Run in uwsgi
./scripts/uwsgi
```

Test it out:
```bash
curl http://localhost:5000/api/records/ | jq
```

See that all record links are prefixed with ```/api/```:

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

## Docker development

Build the API images:
```bash
./docker/build-images.sh
```

Spawn the full stack API deployment
```bash
docker-compose -f docker-compose.full.yml up -d
```

Run the API instance setup:
```bash
./scripts/setup
```

Test it out. Now the service will be exposed on https (443):
```bash
curl -k https://localhost/api/records/ | jq
```
