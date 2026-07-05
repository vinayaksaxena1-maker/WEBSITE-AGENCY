import re
from typing import Dict, List, Set, Any
from urllib.parse import urljoin, urlparse
from agents.contact.email_extractor import EmailExtractor
from agents.contact.phone_extractor import PhoneExtractor
from agents.contact.social_extractor import SocialExtractor
from agents.contact.normalizer import ContactNormalizer
from agents.contact.validator import ContactValidator

class ContactParser:
    def __init__(self):
        self.email_extractor = EmailExtractor()
        self.phone_extractor = PhoneExtractor()
        self.social_extractor = SocialExtractor()
        
        # Subpage keywords to search for in links
        self.target_keywords = ["about", "contact", "team", "support", "footer", "privacy", "terms"]

    def extract_internal_links(self, html_content: str, base_url: str) -> List[str]:
        if not html_content or not base_url:
            return []
            
        parsed_base = urlparse(base_url)
        base_domain = parsed_base.netloc.lower()
        
        # Simple regex to find hrefs
        href_pattern = re.compile(r'href=["\']([^"\']+)["\']', re.IGNORECASE)
        internal_links: Set[str] = set()
        
        for match in href_pattern.finditer(html_content):
            href = match.group(1).strip()
            if not href or href.startswith(("#", "javascript:", "mailto:", "tel:")):
                continue
                
            # Resolve relative link
            full_url = urljoin(base_url, href)
            try:
                parsed_url = urlparse(full_url)
                # Domain Lock check
                if parsed_url.netloc.lower() != base_domain:
                    continue
                    
                path = parsed_url.path.lower()
                # Check if path or full url matches target keywords
                if any(keyword in path or keyword in href.lower() for keyword in self.target_keywords):
                    # Clean fragment and query parameters
                    cleaned_url = urljoin(full_url, parsed_url.path)
                    internal_links.add(cleaned_url)
            except Exception:
                continue
                
        return sorted(list(internal_links))

    def parse_site_data(self, pages_content: Dict[str, str], base_url: str) -> Dict[str, Any]:
        """
        Processes HTML content from multiple pages, extracts contacts, normalizes,
        validates, and calculates quality status.
        pages_content: Dictionary mapping URL -> HTML text.
        """
        all_emails: Set[str] = set()
        all_phones: Set[str] = set()
        all_socials: Dict[str, Set[str]] = {
            "whatsapp": set(),
            "facebook": set(),
            "instagram": set(),
            "linkedin": set(),
            "twitter": set(),
            "youtube": set()
        }
        
        # Parse each page
        for url, html in pages_content.items():
            # Emails
            for email in self.email_extractor.extract(html):
                norm_email = ContactNormalizer.normalize_email(email)
                if ContactValidator.validate_email(norm_email):
                    all_emails.add(norm_email)
                    
            # Phones
            for phone in self.phone_extractor.extract(html):
                norm_phone = ContactNormalizer.normalize_phone(phone)
                if ContactValidator.validate_phone(norm_phone):
                    all_phones.add(norm_phone)
                    
            # Socials
            social_dict = self.social_extractor.extract(html, base_url)
            for platform, urls in social_dict.items():
                if platform in all_socials:
                    for s_url in urls:
                        norm_url = ContactNormalizer.normalize_social(s_url)
                        if ContactValidator.validate_social(norm_url, platform):
                            all_socials[platform].add(norm_url)
                            
        # Sort and convert to lists
        sorted_emails = sorted(list(all_emails))
        sorted_phones = sorted(list(all_phones))
        
        # Map primary and secondary emails
        primary_email = sorted_emails[0] if len(sorted_emails) > 0 else None
        secondary_email = sorted_emails[1] if len(sorted_emails) > 1 else None
        phone = sorted_phones[0] if len(sorted_phones) > 0 else None
        
        whatsapp = sorted(list(all_socials["whatsapp"]))[0] if len(all_socials["whatsapp"]) > 0 else None
        facebook = sorted(list(all_socials["facebook"]))[0] if len(all_socials["facebook"]) > 0 else None
        instagram = sorted(list(all_socials["instagram"]))[0] if len(all_socials["instagram"]) > 0 else None
        linkedin = sorted(list(all_socials["linkedin"]))[0] if len(all_socials["linkedin"]) > 0 else None
        twitter = sorted(list(all_socials["twitter"]))[0] if len(all_socials["twitter"]) > 0 else None
        youtube = sorted(list(all_socials["youtube"]))[0] if len(all_socials["youtube"]) > 0 else None
        
        contact_record = {
            "primary_email": primary_email,
            "secondary_email": secondary_email,
            "phone": phone,
            "whatsapp": whatsapp,
            "facebook": facebook,
            "instagram": instagram,
            "linkedin": linkedin,
            "twitter": twitter,
            "youtube": youtube,
            "website": base_url
        }
        
        # Determine contact quality
        contact_record["status"] = ContactValidator.determine_quality(contact_record)
        
        return contact_record
