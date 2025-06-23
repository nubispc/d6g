# DESIRE6G Topology

This component provides a RESTful API to manage topology nodes and links between nodes.

## Build the Docker image

To build the Docker image:

```bash
git clone git@github.com:nubispc/d6g.git
cd d6g/components/topology
TAG=$(git describe --dirty --long --always)
docker build -t harbor.nbfc.io/desire6g/desire6g-topology:$TAG .
```
