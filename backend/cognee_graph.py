from typing import Dict, List, Any

class CausalMemoryGraph:
    """Pure-Python Causal Knowledge Graph for ZeroDog, mirroring Cognee topology."""
    def __init__(self):
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.edges: List[Dict[str, str]] = []
        self.adj: Dict[str, List[str]] = {}

    def load_from_incident(self, nodes: List[Dict[str, Any]], edges: List[Dict[str, str]]):
        self.nodes = {n["id"]: n for n in nodes}
        self.edges = list(edges)
        self.adj = {n["id"]: [] for n in nodes}
        for e in edges:
            src, tgt = e["source"], e["target"]
            if src in self.adj:
                self.adj[src].append(tgt)
            if tgt in self.adj:
                self.adj[tgt].append(src)

    def find_connected_subgraph(self, query: str) -> List[str]:
        q = query.lower()
        matched_ids = set()
        for node_id, node in self.nodes.items():
            if q in node.get("label", "").lower() or q in node.get("node_type", "").lower() or q in str(node.get("metadata", "")).lower():
                matched_ids.add(node_id)
                for neighbor in self.adj.get(node_id, []):
                    matched_ids.add(neighbor)
        return list(matched_ids) if matched_ids else list(self.nodes.keys())

    def get_serialized_topology(self) -> Dict[str, Any]:
        return {
            "nodes": list(self.nodes.values()),
            "edges": self.edges
        }
