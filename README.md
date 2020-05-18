# OARepo Micro API

[![image](https://img.shields.io/travis/CESNET/video-repository-api.svg)](https://travis-ci.org/CESNET/video-repository-api)
[![image](https://img.shields.io/coveralls/CESNET/video-repository-api.svg)](https://coveralls.io/r/CESNET/video-repository-api)
[![image](https://img.shields.io/github/license/CESNET/video-repository-api.svg)](https://github.com/CESNET/video-repository-api/blob/master/LICENSE)

CESNET Video Repository API microservice

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

- Python >=3.6
- Docker

### Installing development environment

Clone the repository
```
git clone --recursive https://github.com/CESNET/video-repository-api
```

or, if already cloned, update the submodules
```
git submodule update --init --recursive
```


Prepare virtualenv for the project
```
mkvirtualenv video-repository-api
workon video-repository-api
```
_Note: when using `direnv`, virtualenv will be created automatically for you._

Install the app with all the dependencies
```
./scripts/bootstrap
```

Start a minimal required infrastructure in Docker
```
docker-compose -f docker-compose.min.yml up -d
```

Run a script to initialize database and search indexes for the project:
```
./scripts/setup
```

And finally, start the development server
```
./scripts/server
```

Verify, that everything worked out by:
```
curl -k https://localhost:5000/api/records/
```

## Deployment

Start by building a docker image for the service
```
./docker/build-images.sh
```

### Docker deployment

To deploy the service in docker run the following
```
docker-compose -f docker-compose.full.yml up -d
```
This will expose the API service on a standard HTTPS(443) port

### Kubernetes deployment

To deploy the service in a kubernetes cluster, you will want to edit
and apply the following manifests:

- [k8s/001-deployment.yml](k8s/001-deployment.yml)
- [k8s/002-services.yml](k8s/002-services.yml)

Doing so will expose an API service on port 5000 in your cluster.

## Admin

### Manage access

To allow log in for a certain federated EINFRA account use the following CLI command:
```
invenio proxyidp create-account <eduPersonUniqueId> <email> --username <username> --dn <displayname>
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
