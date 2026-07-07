from bs4 import BeautifulSoup

class VisualScoreCalculator:
    @staticmethod
    def calculate_score(soup: BeautifulSoup, colors_count: int) -> int:
        """
        Calculates layout density, styles variety, and compiles a layout complexity score (0-100).
        """
        score = 50  # baseline score

        # 1. Check total interactive and layout components count
        elements_count = len(soup.find_all(True))
        if elements_count > 100:
            score += 15
        elif elements_count > 30:
            score += 8

        # 2. Check color variety variety
        if colors_count >= 4:
            score += 10
        elif colors_count >= 2:
            score += 5

        # 3. Check media nodes density (images/videos)
        media_count = len(soup.find_all(["img", "video", "picture", "svg"]))
        if media_count > 5:
            score += 15
        elif media_count > 1:
            score += 8

        # 4. Check layouts structures (tables, forms, buttons)
        struct_count = len(soup.find_all(["table", "form", "button"]))
        if struct_count > 3:
            score += 10
        elif struct_count > 0:
            score += 5

        # Bound score between 0 and 100
        return max(0, min(100, score))
