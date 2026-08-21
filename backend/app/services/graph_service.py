import networkx as nx
from typing import Dict, Any, List


class KnowledgeGraphService:
    """
    Knowledge Graph service mapping relationships between Papers, Methods,
    Datasets, Tasks, and Authors.
    """

    def __init__(self):
        self.graph = nx.DiGraph()
        self._populate_sample_graph()

    def _populate_sample_graph(self):
        sample_papers = [
            {
                "id": "paper-1",
                "title": "Vision Transformers for Retinal Image Analysis",
                "year": 2024,
                "authors": ["A. Sharma", "M. Chetri"],
                "method": "Vision Transformer",
                "dataset": "EyePACS",
                "task": "Diabetic Retinopathy Grading",
            },
            {
                "id": "paper-2",
                "title": "Multimodal Deep Learning in Brain MRI Segmentation",
                "year": 2025,
                "authors": ["R. Chen", "K. Patel"],
                "method": "U-Net Segmentation Network",
                "dataset": "BraTS",
                "task": "Brain Tumor Segmentation",
            },
            {
                "id": "paper-3",
                "title": "Contrastive Learning on Dermoscopy Images",
                "year": 2023,
                "authors": ["J. Smith", "A. Sharma"],
                "method": "Contrastive Self-Supervised Learning",
                "dataset": "ISIC",
                "task": "Melanoma Skin Cancer Classification",
            },
            {
                "id": "paper-4",
                "title": "EEG Pupillometry Integration for Migraine Detection",
                "year": 2025,
                "authors": ["M. Chetri", "E. Davis"],
                "method": "ResNet Architecture",
                "dataset": "MIMIC Clinical Database",
                "task": "Migraine Detection & Biomarker Analysis",
            },
        ]

        for p in sample_papers:
            # Paper Node
            self.graph.add_node(p["id"], label=p["title"], type="Paper", year=p["year"])

            # Method Node & Edge
            self.graph.add_node(p["method"], label=p["method"], type="Method")
            self.graph.add_edge(p["id"], p["method"], relation="USES_METHOD")

            # Dataset Node & Edge
            self.graph.add_node(p["dataset"], label=p["dataset"], type="Dataset")
            self.graph.add_edge(p["id"], p["dataset"], relation="TESTED_ON")

            # Task Node & Edge
            self.graph.add_node(p["task"], label=p["task"], type="Task")
            self.graph.add_edge(p["id"], p["task"], relation="SOLVES_TASK")

            # Author Nodes & Edges
            for author in p["authors"]:
                self.graph.add_node(author, label=author, type="Author")
                self.graph.add_edge(author, p["id"], relation="AUTHORED")

        # Citation link between paper-1 and paper-3
        self.graph.add_edge("paper-1", "paper-3", relation="CITES")



    def get_graph_data(self) -> Dict[str, List[Dict[str, Any]]]:
        nodes = []
        for node_id, attrs in self.graph.nodes(data=True):
            nodes.append({
                "id": node_id,
                "label": attrs.get("label", node_id),
                "type": attrs.get("type", "Entity"),
                "year": attrs.get("year"),
            })

        edges = []
        for source, target, attrs in self.graph.edges(data=True):
            edges.append({
                "source": source,
                "target": target,
                "relation": attrs.get("relation", "CONNECTED_TO"),
            })

        return {"nodes": nodes, "edges": edges}


knowledge_graph_service = KnowledgeGraphService()
