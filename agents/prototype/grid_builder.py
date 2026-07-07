from typing import Dict, Any

class GridBuilder:
    @staticmethod
    def get_tailwind_classes(columns: int) -> str:
        """
        Translates raw grid column counts to Tailwind CSS column spanning class matrices.
        """
        if columns == 1:
            return "grid-cols-1 col-span-12"
        elif columns == 2:
            return "grid-cols-1 md:grid-cols-2 lg:col-span-6 md:col-span-6 col-span-12"
        elif columns == 3:
            return "grid-cols-1 md:grid-cols-2 lg:grid-cols-3 lg:col-span-4 md:col-span-6 col-span-12"
        elif columns == 4:
            return "grid-cols-1 md:grid-cols-2 lg:grid-cols-4 lg:col-span-3 md:col-span-6 col-span-12"
        
        return "col-span-12"
