import re
import json
from typing import Tuple
from config.config import settings
from core.logger import logger
from agents.niche.interfaces import INicheClassifier

try:
    import google.generativeai as genai
except ImportError:
    genai = None

class RuleEngineClassifier(INicheClassifier):
    def __init__(self):
        # Category keywords defined in SDD-004
        self.keywords = {
            "Hospital": ["hospital", "clinic", "medical", "doctor", "health", "care", "patient", "treatment", "physician", "healthcare"],
            "Clinic": ["clinic", "dentist", "dental", "orthodontic", "pediatric", "therapy", "chiropractor", "medical"],
            "School": ["school", "academy", "college", "university", "education", "course", "degree", "student", "classroom"],
            "Education": ["education", "tuition", "coaching", "learning", "tutorial", "syllabus", "academy"],
            "Gym": ["gym", "fitness", "workout", "crossfit", "train", "bodybuilding", "yoga", "coaching", "pilates", "aerobic"],
            "Restaurant": ["restaurant", "food", "cafe", "dining", "menu", "chef", "bistro", "eatery", "cuisine", "pizza"],
            "Hotel": ["hotel", "resort", "suite", "stay", "motel", "accommodation", "hostel", "inn"],
            "Law Firm": ["lawyer", "attorney", "law firm", "advocate", "legal", "counsel", "solicitor", "justice", "lawsuit"],
            "Real Estate": ["real estate", "realtor", "property", "apartment", "house", "villa", "condo", "mortgage", "brokerage"],
            "NGO": ["ngo", "charity", "nonprofit", "volunteer", "donation", "foundation", "cause", "community"],
            "Travel": ["travel", "tourism", "vacation", "trip", "flight", "booking", "tour", "destination", "adventure"],
            "Portfolio": ["portfolio", "creative", "designer", "developer", "resume", "gallery", "exhibition", "showcase"]
        }

    def classify(self, html_content: str) -> Tuple[str, float]:
        if not html_content:
            return "Unknown", 0.0

        content_lower = html_content.lower()
        best_category = "Unknown"
        max_matches = 0
        
        # Count matches for each category
        for category, kw_list in self.keywords.items():
            count = 0
            for kw in kw_list:
                # Simple word/substring occurrences count
                count += content_lower.count(kw)
            if count > max_matches:
                max_matches = count
                best_category = category

        # Calculate confidence ratio
        if max_matches == 0:
            return "Unknown", 0.0
        elif max_matches == 1:
            confidence = 0.50
        elif max_matches == 2:
            confidence = 0.80
        else:
            confidence = 0.95

        return best_category, confidence


class GeminiClassifier(INicheClassifier):
    def classify(self, html_content: str) -> Tuple[str, float]:
        # Graceful checks for missing or dummy API key
        if not settings.GEMINI_API_KEY or settings.GEMINI_API_KEY == "dummy_gemini_key":
            logger.warning("Gemini API key is not configured or is a dummy key. Skipping AI classification...")
            return "Business", 0.50

        if not genai:
            logger.warning("google-generativeai library is not installed. Skipping AI classification...")
            return "Business", 0.50

        try:
            # Extract plain text elements from HTML to minimize prompt tokens (FinOps compliant)
            title = ""
            title_match = re.search(r"<title[^>]*>(.*?)</title>", html_content, re.IGNORECASE | re.DOTALL)
            if title_match:
                title = title_match.group(1).strip()

            desc = ""
            desc_match = re.search(r"<meta[^>]*name=[\"']description[\"'][^>]*content=[\"'](.*?)[\"']", html_content, re.IGNORECASE)
            if desc_match:
                desc = desc_match.group(1).strip()

            # Clean and slice body snippet (max 1000 characters to prevent token degradation)
            body_text = re.sub(r"<[^>]*>", " ", html_content)
            body_text = re.sub(r"\s+", " ", body_text).strip()
            body_snippet = body_text[:1000]

            prompt = (
                "You are an expert business niche classifier.\n"
                "Analyze the following metadata and text snippet from a business website:\n"
                f"Page Title: {title}\n"
                f"Description: {desc}\n"
                f"Body Snippet: {body_snippet}\n\n"
                "Classify this business into exactly one of these industries:\n"
                "Publisher, School, Hospital, Clinic, Restaurant, Hotel, Travel, Law Firm, Real Estate, NGO, Gym, Education, Portfolio, Business, Corporate.\n\n"
                "Return the result ONLY as a valid JSON string with the keys 'industry' and 'confidence'. Example:\n"
                "{\"industry\": \"Law Firm\", \"confidence\": 0.95}"
            )

            genai.configure(api_key=settings.GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            
            # Extract JSON block
            response_text = response.text.strip()
            json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group(0))
                industry = data.get("industry", "Business")
                confidence = float(data.get("confidence", 0.80))
                return industry, confidence
            
            return "Business", 0.60
        except Exception as e:
            logger.error(f"Gemini API call failed with exception: {e}. Falling back to default...")
            return "Business", 0.50


class HybridClassifier(INicheClassifier):
    def __init__(self):
        self.rule_engine = RuleEngineClassifier()
        self.ai_engine = GeminiClassifier()

    def classify(self, html_content: str) -> Tuple[str, float]:
        # Step A: Run local rules engine first
        industry, confidence = self.rule_engine.classify(html_content)
        
        logger.info(f"Local Rule Engine Output: industry='{industry}', confidence={confidence}")
        
        # Step B: AI Fallback triggers only if rules confidence is low (< 0.85)
        if confidence < 0.85 or industry == "Unknown":
            logger.info("Local confidence is below threshold. Invoking Gemini AI fallback classifier...")
            ai_industry, ai_confidence = self.ai_engine.classify(html_content)
            logger.info(f"Gemini AI Output: industry='{ai_industry}', confidence={ai_confidence}")
            return ai_industry, ai_confidence
            
        return industry, confidence
