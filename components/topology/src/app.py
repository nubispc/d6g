from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List

# Define your data models
class Node(BaseModel):
    site_id: str
    cpu: int         # Number of CPUs
    mem: int         # Memory in GB
    storage: int     # Storage in GB
    iml_endpoint: str  # Endpoint for IML


class Link(BaseModel):
    source: str
    destination: str
    latency_ms: float  # Latency in milliseconds


# Database Simulation
nodes_db: Dict[str, Node] = {}
links_db: Dict[str, Link] = {}

tags_metadata = [
    {
        "name": "nodes",
        "description": "Operations with nodes in the topology",
    },
    {
        "name": "links",
        "description": "Operations with links in the topology",
    }
]
app = FastAPI(openapi_tags=tags_metadata)


@app.post("/nodes/", tags=["nodes"])
def add_node(node: Node):
    '''
    Add a node to the topology.
    If the node already exists, it raises a 400 error.
    '''
    if node.site_id in nodes_db:
        raise HTTPException(
            status_code=400, detail=f"Node {node.site_id} already exists.")
    nodes_db[node.site_id] = node
    return {"message": "Node added successfully."}


@app.get("/nodes/", tags=["nodes"])
def get_nodes():
    '''
    Get all nodes in the topology.
    Returns a list of all nodes.
    '''
    return {"nodes": list(nodes_db.values())}


@app.get("/nodes/{site_id}", tags=["nodes"])
def get_node(site_id: str):
    '''
    Get a specific node by site_id.
    If the node does not exist, it raises a 404 error.
    '''
    if site_id not in nodes_db:
        raise HTTPException(status_code=404, detail="Node not found.")
    return nodes_db[site_id]


@app.delete("/nodes/{site_id}", tags=["nodes"])
def delete_node(site_id: str):
    '''
    Delete a node from the topology.
    If the node does not exist, it raises a 404 error.
    '''
    if site_id not in nodes_db:
        raise HTTPException(status_code=404, detail="Node not found.")
    del nodes_db[site_id]
    return {"message": f"Node {site_id} deleted successfully."}


@app.post("/links/", tags=["links"])
def add_link(link: Link):
    '''
    Add a link between two nodes.
    The source and destination nodes must already exist in the nodes database.
    If the link already exists, it will get updated.
    '''
    if link.source not in nodes_db:
        raise HTTPException(
            status_code=404, detail=f"Source node '{link.source}' not found.")
    if link.destination not in nodes_db:
        raise HTTPException(
            status_code=404, detail=f"Destination node '{link.destination}' not found.")

    key = f"{link.source}-{link.destination}"
    links_db[key] = link
    return {"message": "Link added successfully."}


@app.get("/links/", tags=["links"])
def get_links():
    '''
    Get all links in the topology.
    Returns a list of all links.
    '''
    return {"links": list(links_db.values())}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
