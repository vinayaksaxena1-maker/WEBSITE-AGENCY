import re
from typing import Dict, Any
from agents.audit.interfaces import IAuditScoreStrategy

class SeoScoreStrategy(IAuditScoreStrategy):
    def evaluate(self, page_data: Dict[str, Any]) -> int:
        html = page_data.get("html", "")
        score = 0
        
        # 1. Title validation
        title_match = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
        if title_match:
            title_text = title_match.group(1).strip()
            if 10 <= len(title_text) <= 60:
                score += 30
            else:
                score += 15
                
        # 2. Meta description validation
        meta_desc = re.search(r"<meta[^>]*name=[\"']description[\"'][^>]*content=[\"'](.*?)[\"']", html, re.IGNORECASE)
        if not meta_desc:
            meta_desc = re.search(r"<meta[^>]*content=[\"'](.*?)[\"'][^>]*name=[\"']description[\"']", html, re.IGNORECASE)
        if meta_desc:
            score += 30
            
        # 3. H1 count check
        h1_tags = re.findall(r"<h1[^>]*>.*?</h1>", html, re.IGNORECASE | re.DOTALL)
        h1_count = len(h1_tags)
        if h1_count == 1:
            score += 20
        elif h1_count > 1:
            score += 10
            
        # 4. H2/H3 structural check
        h2_h3_tags = re.findall(r"<h[23][^>]*>.*?</h[23]>", html, re.IGNORECASE | re.DOTALL)
        if len(h2_h3_tags) > 0:
            score += 20
            
        return score

class MobileScoreStrategy(IAuditScoreStrategy):
    def evaluate(self, page_data: Dict[str, Any]) -> int:
        html = page_data.get("html", "")
        score = 0
        
        # 1. Viewport tag check
        viewport_match = re.search(r"<meta[^>]*name=[\"']viewport[\"']", html, re.IGNORECASE)
        if viewport_match:
            score += 60
            
        # 2. Responsive style pattern checks
        style_pattern = re.search(r"@media|flex|grid|box-sizing", html, re.IGNORECASE)
        if style_pattern:
            score += 40
            
        return score

class SpeedScoreStrategy(IAuditScoreStrategy):
    def evaluate(self, page_data: Dict[str, Any]) -> int:
        # Evaluate based on Response time (TTFB) in page data
        ttfb = page_data.get("response_time_ms", 1000)
        
        if ttfb < 500:
            return 100
        elif ttfb <= 1500:
            return 75
        elif ttfb <= 3000:
            return 50
        else:
            return 25

class TrustScoreStrategy(IAuditScoreStrategy):
    def evaluate(self, page_data: Dict[str, Any]) -> int:
        html = page_data.get("html", "")
        score = 0
        
        # 1. SSL Valid
        if page_data.get("ssl_valid", False):
            score += 40
            
        # 2. Policy / Terms links
        policy_link = re.search(r"href=[\"'][^\"']*(privacy|terms|policy|legal)[^\"']*[\"']", html, re.IGNORECASE)
        if policy_link:
            score += 40
            
        # 3. Contact indicators
        contact_info = re.search(r"tel:|phone|email|contact|map|address", html, re.IGNORECASE)
        if contact_info:
            score += 20
            
        return score

class DesignScoreStrategy(IAuditScoreStrategy):
    def evaluate(self, page_data: Dict[str, Any]) -> int:
        html = page_data.get("html", "")
        score = 0
        
        # 1. CTA check
        cta_match = re.search(r"(book|appointment|contact|sign-up|register|get-started|buy|order|submit)", html, re.IGNORECASE)
        if cta_match:
            score += 50
            
        # 2. Semantic structure check
        structure_match = re.search(r"<header|<main|<footer", html, re.IGNORECASE)
        if structure_match:
            score += 50
            
        return score
