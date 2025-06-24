# Optimization Engine Module Core Flow

# Python Modules
import json
import logging
import yaml
# Local Modules
import library.translator as translator

# Demo Selector Pool
import library.selector_pool.random_selection as random_selection

# Demo Model Pool
import library.model_pool.partition as partition
import library.model_pool.autologic as autologic
import library.model_pool.greedysplit as greedysplit

# Demo Data
import library.resources.topology as topology
import library.resources.monitoring as monitoring
import library.resources.functions as functions

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Model Pool Demo Configuration
algorithms = {
    "partition.py": {"enabled": False},
    "autologic.py": {"enabled": True},
    "greedysplit.py": {"enabled": True},
}

# Model Selector Demo Configuration
selectors = {
    "spinwheel.py (Default)": {"enabled": True},
    "intelligence.py": {"enabled": False},
}

def optimization_engine(data, d6g_site):

    # Fetch VNF data from Service Catalog
    logger.info("Fetching functions information from the Service Catalog module...")
    # TODO: Do we really want to have a hardcoded graph name here?
    function_info = functions.fetch_service_catalog_info(funtions_graph_name = "apps.nf.yaml", data = data)
    if function_info is None:
        logger.info("Error: Failed to fetch function information, check configuration.")
        error_payload = {"Error": "Failed to fetch function information, check configuration."}
        return json.dumps(error_payload).encode('utf-8')
    else:
        logger.info("Function information fetched successfully from the Service Catalog module.")

    function_info = yaml.safe_load(function_info)
    # Fetch topology from Topology Module
    logger.info("Fetching topology from Topology module...")
    topologyGraph, domains, site_resources = topology.fetch_d6g_site_info(d6g_site)
    if topologyGraph is None:
        logger.info("Error: Failed to fetch topology, check configuration.")
        error_payload = {"Error": "Failed to fetch topology, check configuration."}
        return json.dumps(error_payload).encode('utf-8')
    else:
        logger.info("Topology fetched successfully from Topology module.")
    if domains is None:
        logger.info("Error: Failed to fetch domains, check configuration.")
        error_payload = {"Error": "Failed to fetch domains, check configuration."}
        return json.dumps(error_payload).encode('utf-8')
    # Fetch topology resources from monitoring (Disabled for now)
    # logger.info("Fetching topology resources from monitoring module...")
    # topology_resources = monitoring.fetchTopologyResources(d6g_site)
    # logger.info("Topology resources fetched successfully from monitoring module.")

    # Translate NSD to internal structure
    logger.info("Translating service request to internal graph...")
    serviceGraph, decorations = translator.request2graph(data, function_info)
    if serviceGraph is None:
        logger.info("Error: Failed to translate service request, check syntax.")
        error_payload = {"Error": "Failed to translate service request, check syntax."}
        return json.dumps(error_payload).encode('utf-8')
    else:
        logger.info("Service request decoded successfully.")

    # Check for local D6G site resource availability
    logger.info("Checking resource availability...")
    if monitoring.check_resources(function_info, site_resources):
        logger.info("Ok: There are enough resources to host the service in the current region.")
    else:
        logger.info("Failed: The local region does not have enough resources to host the service.")
        error_payload = {"Failed": "The local region does not have enough resources to host the service. Relaying service request to the next region."}
        return json.dumps(error_payload).encode('utf-8')
    
    logger.info("Checking if there is only one D6G node in the site...")
    # Check if only one D6G node in site, if yes forward the request to back to the local SO
    if domains == 1:
        logger.info("Success: There is only one D6G node in the site. Forwarding request to the local SO.")
        # Decode bytes to string if data is in bytes format
        if isinstance(data, bytes):
            data = data.decode('utf-8')
        return json.dumps(data).encode('utf-8')

    # Route to enabled autoselector from Selector Pool
    pick = random_selection.spinwheel(algorithms)
    logger.info("Model Selector: " + str(pick))

    # Route to selected Model from the Model Pool
    subgraphs = []
    try:
        if pick == "partition.py (Default)":
            subgraphs = partition.partition(serviceGraph, topologyGraph, domains)
        elif pick == "autologic.py":
            subgraphs = autologic.autologic(serviceGraph, topologyGraph, domains)
        elif pick == "greedysplit.py":
            subgraphs = greedysplit.greedysplit(serviceGraph, topologyGraph, domains)
        else:
            logger.info("Error: Unknown model selected, check Model Pool configuration.")
            error_payload = "Error: Unknown model selected, check Model Pool configuration."
            return json.dumps(error_payload).encode('utf-8')
    except Exception as e:
        logger.error("Internal error occurred in selected model: " + str(e))
        error_payload = {"Error": "Internal error occurred in selected model: " + str(e)}
        return json.dumps(error_payload).encode('utf-8')
    
    # Verify if partitioning was successfull
    if subgraphs is None or subgraphs == []:
        logger.info("Error: Unknown partitioning error.")
    elif subgraphs == -1:
        logger.info("Service partitioning has failed, not enough resources to allocate.")
        error_payload = {"Failed": "Service partitioning has failed, not enough resources to allocate."}
        return json.dumps(error_payload).encode('utf-8')
    else:
        logger.info("Partitioning executed successfully. Count: " + str(len(subgraphs)) + " subgraphs: " + str(subgraphs))

    # Translate internal structure to YAML for SO
    encoded_subgraphs = []
    for subgraph in subgraphs:
        encoded_subgraph = translator.graph2request(subgraph, data)
        if encoded_subgraph is None:
            logger.info("Error: Failed to encode subgraph, check syntax: " + str(subgraph))
            error_payload = {"Error": "Failed to encode subgraph, check syntax: " + str(subgraph)}
            return json.dumps(error_payload).encode('utf-8')
        else:
            encoded_subgraphs.append(encoded_subgraph)
            logger.info("Subgraph encoded successfully.")
    logger.info("Combined subgraphs encoded successfully.")

    # Combine Response
    try:
        combined_response = []
        for domain in range(0, domains-1):
            combined_response.append({f"s{domain+1}e": encoded_subgraphs[domain], "site_id": f"SITEID{domain+1}"})
        logger.info("Combined response ready.")
    except Exception as e:
        logger.exception("An error occurred while combining the response: %s", e)
        error_payload = {"Error": "An error occurred while combining the response: " + str(e)}
        return json.dumps(error_payload).encode('utf-8')

    # Return Partitioned Request
    logger.info("Returning optimized service request.")
    return json.dumps(combined_response).encode('utf-8')