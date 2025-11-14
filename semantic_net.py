import networkx as nx
import matplotlib.pyplot as plt
from typing import List, Tuple


class SemanticNet:

    def __init__(self):
        # Directed graph to store nodes and labeled relations
        self.g = nx.DiGraph()

    # --------- basic node operations ---------
    def add_node(self, name: str, kind: str = "concept") -> None:
        """Add a node (concept/part/fuel/role/etc.)."""
        self.g.add_node(name, kind=kind)

    def remove_node(self, name: str) -> None:
        """Remove a node and all its relations."""
        if name in self.g:
            self.g.remove_node(name)

    # --------- basic relation operations ---------
    def add_relation(self, source: str, relation: str, target: str) -> None:
        """
        Add a labeled relation (edge) between two nodes.
        If the nodes do not exist, they will be created as 'concept' by default.
        """
        if source not in self.g:
            self.add_node(source)
        if target not in self.g:
            self.add_node(target)
        self.g.add_edge(source, target, relation=relation)

    def remove_relation(self, source: str, relation: str, target: str) -> None:
        """Remove a specific relation between two nodes if it exists."""
        if self.g.has_edge(source, target):
            if self.g[source][target].get("relation") == relation:
                self.g.remove_edge(source, target)

    # --------- convenience helpers for common relations ---------
    def add_is_a(self, child: str, parent: str) -> None:
        """Add an 'is-a' relation: child is-a parent."""
        self.add_node(child, kind="concept")
        self.add_node(parent, kind="concept")
        self.add_relation(child, "is-a", parent)

    def add_has_part(self, whole: str, part: str) -> None:
        """Add a 'has-part' relation: whole has-part part."""
        self.add_node(whole, kind="concept")
        self.add_node(part, kind="part")
        self.add_relation(whole, "has-part", part)

    def add_uses_fuel(self, vehicle: str, fuel: str) -> None:
        """Add a 'uses-fuel' relation: vehicle uses-fuel fuel."""
        self.add_node(vehicle, kind="concept")
        self.add_node(fuel, kind="fuel")
        self.add_relation(vehicle, "uses-fuel", fuel)

    # --------- query / search operations ---------
    def neighbors_with_relation(self, source: str, relation: str) -> List[str]:

        if source not in self.g:
            return []
        result: List[str] = []
        for _, target, data in self.g.out_edges(source, data=True):
            if data.get("relation") == relation:
                result.append(target)
        return result

    def incoming_with_relation(self, target: str, relation: str) -> List[str]:
        if target not in self.g:
            return []
        result: List[str] = []
        for source, _, data in self.g.in_edges(target, data=True):
            if data.get("relation") == relation:
                result.append(source)
        return result

    def nodes_of_kind(self, kind: str) -> List[str]:
        """Return all nodes that have a specific kind (concept, part, fuel, etc.)."""
        return [n for n, data in self.g.nodes(data=True) if data.get("kind") == kind]

    # --------- visualization ---------
    def draw(self, title: str = "Semantic Net") -> None:
        plt.figure(figsize=(10, 7))

        # layout for node positions
        pos = nx.spring_layout(self.g, k=1.5, seed=7)

        # choose node colors based on 'kind'
        colors = []
        for _, data in self.g.nodes(data=True):
            kind = data.get("kind", "concept")
            if kind == "concept":
                colors.append("lightblue")
            elif kind == "part":
                colors.append("lightgreen")
            elif kind == "fuel":
                colors.append("lightpink")
            else:
                colors.append("lightgray")

        nx.draw(
            self.g,
            pos,
            with_labels=True,
            node_color=colors,
            node_size=1800,
            font_size=10,
            arrows=True,
            arrowstyle="-|>",
            arrowsize=15,
        )

        edge_labels = nx.get_edge_attributes(self.g, "relation")
        nx.draw_networkx_edge_labels(self.g, pos, edge_labels=edge_labels, font_size=8)

        plt.axis("off")
        plt.title(title)
        plt.tight_layout()
        plt.show()

    # --------- helpers for advanced features ---------
    def has_fact(self, source: str, relation: str, target: str) -> bool:
        """Return True if there is an edge source -> target with the given relation."""
        if not self.g.has_edge(source, target):
            return False
        return self.g[source][target].get("relation") == relation

    def inherit_properties(self, property_relations: List[str]) -> List[Tuple[str, str, str]]:
     
        new_facts: List[Tuple[str, str, str]] = []

        # all "is-a" edges: (child, parent)
        isa_edges = [
            (child, parent)
            for child, parent, data in self.g.edges(data=True)
            if data.get("relation") == "is-a"
        ]

        for x, y in isa_edges:  # x is-a y
            # look at all outgoing relations from parent y
            for _, z, data in self.g.out_edges(y, data=True):
                r = data.get("relation")
                if r in property_relations and not self.has_fact(x, r, z):
                    # infer new fact: x r z
                    self.add_relation(x, r, z)
                    new_facts.append((x, r, z))

        return new_facts

    def find_conflicts(self, relation: str) -> List[Tuple[str, List[str]]]:
        conflicts: List[Tuple[str, List[str]]] = []

        mapping = {}
        for s, t, data in self.g.edges(data=True):
            if data.get("relation") == relation:
                mapping.setdefault(s, []).append(t)

        for src, targets in mapping.items():
            unique_targets = list(set(targets))
            if len(unique_targets) > 1:
                conflicts.append((src, unique_targets))

        return conflicts
