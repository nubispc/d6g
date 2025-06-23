CONTAINER_TOOL ?= docker
TAG ?= $(shell git describe --dirty --long --always)

.DEFAULT_GOAL: images

so:
	$(CONTAINER_TOOL) build --push -t harbor.nbfc.io/desire6g/desire6g-so:$(TAG) -f components/service-orchestrator/Dockerfile components/service-orchestrator

sc:
	$(CONTAINER_TOOL) build --push -t harbor.nbfc.io/desire6g/desire6g-service-catalog:$(TAG) -f components/service-catalog/Dockerfile components/service-catalog

oe:
	$(CONTAINER_TOOL) build --push -t harbor.nbfc.io/desire6g/desire6g-oe:$(TAG) -f components/optimization-engine/Dockerfile components/optimization-engine

topology:
	$(CONTAINER_TOOL) build --push -t harbor.nbfc.io/desire6g/desire6g-topology:$(TAG) -f components/topology/Dockerfile components/topology

images: so sc oe topology
	@echo "Images built and pushed successfully:"
	@echo "- harbor.nbfc.io/desire6g/desire6g-so:$(TAG)"
	@echo "- harbor.nbfc.io/desire6g/desire6g-service-catalog:$(TAG)"
	@echo "- harbor.nbfc.io/desire6g/desire6g-oe:$(TAG)"
	@echo "- harbor.nbfc.io/desire6g/desire6g-topology:$(TAG)"

# TODO: Add a target to replace the tag in the deployment files