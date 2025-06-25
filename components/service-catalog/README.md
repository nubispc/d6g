# DESIRE6G Service Catalog

This component uses Github as a backend to store service graphs and network functions.
It provides a simple RESTful API to perform create, list, view and delete
service graphs and network functions.

## Build the Docker image

To build the Docker image:

```bash
git clone git@github.com:nubispc/d6g.git
cd d6g/components/service-catalog
TAG=$(git describe --dirty --long --always)
docker build -t harbor.nbfc.io/desire6g/desire6g-service-catalog:$TAG .
```

## Required ENV variables

To run this component, the user must define the following ENV variables:

- `GITHUB_ORG`: The Github organization owning the Catalog repository
- `GITHUB_REPO`: The Github repository used as a storage backend for the Catalog
- `GITHUB_ACCESS_TOKEN`: A Github Access Token with read & write privileges to the Catalog repository

If any of the listed variables are not set, the Service Catalog will fallback to a local storage backend.
