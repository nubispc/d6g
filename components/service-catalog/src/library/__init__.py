import os
from enum import Enum


SERVICE_GRAPH_FOLDER = 'service_graphs'
NETWORK_FUNCTION_FOLDER = 'network_functions'

# Create folders if they don't exist
if not os.path.exists(SERVICE_GRAPH_FOLDER):
    os.makedirs(SERVICE_GRAPH_FOLDER)
if not os.path.exists(NETWORK_FUNCTION_FOLDER):
    os.makedirs(NETWORK_FUNCTION_FOLDER)


class FileType(str, Enum):
    SERVICE_GRAPH = 'service_graph'
    NETWORK_FUNCTION = 'network_function'
