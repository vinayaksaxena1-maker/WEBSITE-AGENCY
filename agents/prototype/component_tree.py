from typing import List, Dict, Any
from core.logger import logger

class ComponentTree:
    @staticmethod
    def build_tree(components: List[Dict[str, Any]], max_depth: int = 10) -> Dict[str, Any]:
        """
        Assembles component trees hierarchies with parent-child linkages.
        Enforces maximum depth safeguards (< 10 levels) to block stack overflows.
        """
        logger.info("ComponentTree: Building nested layout tree from components...")

        root = {
            "instance_id": "WebsiteRoot",
            "name": "WebsiteRoot",
            "children": [],
            "depth": 0
        }

        # Simulate tree hierarchy building
        current_parent = root
        for comp in components:
            # Enforce deep nested loop safeguards
            if current_parent["depth"] >= max_depth - 1:
                logger.warning(f"ComponentTree: Maximum hierarchy depth limit ({max_depth}) exceeded! Halting nesting.")
                break

            node = {
                "instance_id": comp["instance_id"],
                "name": comp["name"],
                "priority": comp["priority"],
                "order": comp["order"],
                "children": [],
                "depth": current_parent["depth"] + 1
            }

            # Nested links simulation:
            # Header and Footer are placed directly under Root, other sections might nest buttons/cards
            if comp["name"] in ("HeaderComponent", "FooterComponent"):
                root["children"].append(node)
            else:
                # Add child components as dependencies
                for dep in comp.get("dependencies", []):
                    dep_node = {
                        "instance_id": f"{dep}_{comp['order']}",
                        "name": dep,
                        "children": [],
                        "depth": node["depth"] + 1
                    }
                    node["children"].append(dep_node)

                root["children"].append(node)

        return root
