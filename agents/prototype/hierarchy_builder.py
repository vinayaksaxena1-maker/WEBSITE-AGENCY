from bs4 import BeautifulSoup, Tag
from typing import Dict, Any, Optional
from core.logger import logger

class HierarchyBuilder:
    def __init__(self, max_nodes: int = 5000, max_depth: int = 100):
        self.max_nodes = max_nodes
        self.max_depth = max_depth
        self.node_count = 0

    def build_hierarchy(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """
        Builds a parent-child hierarchical tree from the BeautifulSoup object,
        enforcing size and depth limits to prevent recursion memory exhaustion.
        """
        self.node_count = 0
        root = soup.find("html")
        if not root:
            root = soup.find("body")
        if not root:
            # Fallback to the soup wrapper itself if standard structure is missing
            root = soup

        logger.info("HierarchyBuilder: Generating DOM parent-child nesting index...")
        tree = self._build_node_tree(root, depth=0)
        logger.info(f"HierarchyBuilder: Hierarchy tree compiled. Total nodes parsed: {self.node_count}")
        return tree or {}

    def _build_node_tree(self, tag, depth: int) -> Optional[Dict[str, Any]]:
        if not isinstance(tag, Tag):
            return None

        self.node_count += 1
        
        # 1. Enforce node size limit guard
        if self.node_count > self.max_nodes:
            logger.warning(
                f"HierarchyBuilder: Total parsed elements exceeded size limit of {self.max_nodes} nodes! Truncating hierarchy."
            )
            return None

        # 2. Enforce recursion depth limit guard
        if depth > self.max_depth:
            logger.warning(
                f"HierarchyBuilder: Hierarchy depth exceeded limit of {self.max_depth} levels! Truncating branch."
            )
            return None

        # Compile details of this node
        node_id = tag.name
        id_attr = tag.get("id")
        classes = tag.get("class", [])
        
        node_repr = f"<{node_id}"
        if id_attr:
            node_repr += f" id='{id_attr}'"
        if classes:
            node_repr += f" class='{' '.join(classes)}'"
        node_repr += ">"

        children = []
        for child in tag.children:
            if isinstance(child, Tag):
                child_node = self._build_node_tree(child, depth + 1)
                if child_node:
                    children.append(child_node)
                
                # Check early exit if counter triggered inside child loop
                if self.node_count > self.max_nodes:
                    break

        return {
            "tag": tag.name,
            "id": id_attr,
            "classes": classes,
            "repr": node_repr,
            "depth": depth,
            "children": children
        }
