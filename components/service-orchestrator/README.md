# DESIRE6G Service Orchestrator

This component is responsible for accepting service deployment requests
from the user, cross-checking the requests with the Topology and
Service Catalog components, forwarding the requests to the Optimization Engine
and finally deploying the optimized services to the relevant IML endpoint.

## Build the Docker image

To build the Docker image:

```bash
git clone git@github.com:nubispc/d6g.git
cd d6g/components/service-orchestrator
TAG=$(git describe --dirty --long --always)
docker build -t harbor.nbfc.io/desire6g/desire6g-so:$TAG .
```

## Required ENV variables

To run this component, the user must define the following ENV variables:

- `TOPOLOGY_MODULE_HOST`: The hostname or IP address of the Topology component
- `TOPOLOGY_MODULE_PORT`: The port of the Topology component
- `SERVICE_CATALOG_HOST`: The hostname or IP address of the Service Catalog component
- `SERVICE_CATALOG_PORT`: The port of the Service Catalog component
- `MESSAGING_SYSTEM`: The messaging system in use (Kafka or RabbitMQ)
- `KAFKA_BOOTSTRAP_SERVERS`: The Kafka bootstrap server (only applicable when using Kafka messaging system)
- `RABBITMQ_HOST`: The hostname or IP address of the RabbitMQ broker (only applicable when using RabbitMQ messaging system)
- `RABBITMQ_MAX_RETRIES`: The max retries that will try to receive a message (only applicable when using RabbitMQ messaging system)
- `INPUT_TOPIC`: The topic that Service Orchestrator will use the send the unoptimized Service Graph to the Optimization Engine
- `FINAL_TOPIC`: The topic that Service Orchestrator expects to receive the optimized Service Grahps

## Usage

```bash
curl -X 'POST' \
  'http://0.0.0.0:8000/services' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "demo_nsd.sg.yaml",
  "site_id": "SITEID1"
}'
```
