# d6g

This repository contains the required code, deployment files and instructions
to deploy the Desire6G framework in an existing Kubernetes cluster.

## Deployment

### Build the images

To build the Docker images for the DESIRE6G components:

```bash
git clone git@github.com:nubispc/d6g.git
cd d6g
make images
```

### Generate the K8S YAMLs

```bash
make deploy
```

### Deploy the components

```bash
kubectl apply -f deployment/deploy/
```

> Note: Before deploying make sure you edit the `servicecatalog-creds.yaml` file to contain your base64 encoded Github credentials.

## Usage

TODO: Update README.md with demo instructions and add demo service graph YAMLs.
