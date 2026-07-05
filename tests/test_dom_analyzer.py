import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch, ANY
from bs4 import BeautifulSoup
from agents.prototype.dom_parser import DOMParser
from agents.prototype.dom_classifier import DOMClassifier
from agents.prototype.semantic_detector import SemanticDetector
from agents.prototype.section_detector import SectionDetector
from agents.prototype.navigation_detector import NavigationDetector
from agents.prototype.cta_detector import CTADetector
from agents.prototype.form_detector import FormDetector
from agents.prototype.layout_analyzer import LayoutAnalyzer
from agents.prototype.hierarchy_builder import HierarchyBuilder
from agents.prototype.component_mapper import ComponentMapper
from agents.prototype.dom_analyzer import DOMAnalyzer
from agents.prototype.prototype_models import PrototypeDOMAnalysis

# ---------------------------------------------------------
# DOM Preprocessing Tests
# ---------------------------------------------------------
def test_dom_parser_noise_removal():
    raw_html = """
    <html>
      <head>
        <style>body { background: red; }</style>
        <script>alert('track');</script>
      </head>
      <body>
        <!-- This is a comment -->
        <header id="main-header">
          <nav class="tracker-active navbar">Home</nav>
        </header>
        <div style="display: none;">Hidden content</div>
        <div id="banner-ad">Advertisement block</div>
        <main>
          <h1>Content</h1>
        </main>
      </body>
    </html>
    """
    soup = DOMParser.parse_and_clean(raw_html)
    
    assert not soup.find("script")
    assert not soup.find("style")
    assert not soup.find(string=lambda t: "comment" in t)
    assert not soup.find(id="banner-ad")
    assert not soup.find("div", style=lambda s: s and "display: none" in s)
    assert soup.find("header") is not None
    assert soup.find("nav") is None  # Classified class containing 'tracker-active' got stripped!

# ---------------------------------------------------------
# Semantic Tag Detection Tests
# ---------------------------------------------------------
def test_semantic_tag_detector():
    raw_html = "<html><body><header></header><main><section></section><article></article><footer></footer></main></body></html>"
    soup = BeautifulSoup(raw_html, "html.parser")
    elements = SemanticDetector.detect_semantic_elements(soup)
    
    assert "header" in elements
    assert len(elements["header"]) == 1
    assert "main" in elements
    assert "section" in elements
    assert "article" in elements

# ---------------------------------------------------------
# Section Detection Tests
# ---------------------------------------------------------
def test_section_detector_categories():
    raw_html = """
    <html>
      <body>
        <header class="main-header">Brand</header>
        <section id="hero-banner" class="hero">Welcome</section>
        <section class="services-grid">Our Services</section>
        <section class="pricing-plans">Plans</section>
        <footer class="site-footer">Footer</footer>
      </body>
    </html>
    """
    soup = BeautifulSoup(raw_html, "html.parser")
    sections = SectionDetector.detect_sections(soup)
    
    categories = [s["category"] for s in sections]
    assert "header" in categories
    assert "hero" in categories
    assert "services" in categories
    assert "pricing" in categories
    assert "footer" in categories

# ---------------------------------------------------------
# Navigation & CTA Detection Tests
# ---------------------------------------------------------
def test_navigation_and_cta_detector():
    raw_html = """
    <html>
      <body>
        <nav class="sticky navbar">
          <a href="/">Home</a>
          <a href="/about">About</a>
        </nav>
        <main>
          <button class="btn btn-primary btn-submit">Primary CTA</button>
          <a href="https://wa.me/12345" class="cta-whatsapp">WhatsApp Chat</a>
        </main>
      </body>
    </html>
    """
    soup = BeautifulSoup(raw_html, "html.parser")
    nav = NavigationDetector.detect_navigation(soup)
    ctas = CTADetector.detect_ctas(soup)
    
    assert nav["type"] == "sticky-header"
    assert "Home" in nav["links"]
    
    whatsapp_cta = [c for c in ctas if c["type"] == "whatsapp"]
    assert len(whatsapp_cta) == 1
    assert whatsapp_cta[0]["priority"] == "primary"

# ---------------------------------------------------------
# Form Detection Tests
# ---------------------------------------------------------
def test_form_detector():
    raw_html = """
    <html>
      <body>
        <form id="contact-form">
          <input type="text" name="username" placeholder="Your Name" />
          <input type="email" name="useremail" />
          <textarea name="message"></textarea>
          <button type="submit">Send</button>
        </form>
      </body>
    </html>
    """
    soup = BeautifulSoup(raw_html, "html.parser")
    forms = FormDetector.detect_forms(soup)
    
    assert len(forms) == 1
    assert forms[0]["type"] == "contact"
    assert forms[0]["fields_count"] == 3
    assert forms[0]["fields"][0]["name"] == "username"

# ---------------------------------------------------------
# Hierarchy & Node Overflow Protection Tests
# ---------------------------------------------------------
def test_hierarchy_size_limit_guards():
    # Construct highly nested page (depth > 100)
    nested_html = "<div>" * 150 + "Deep Text" + "</div>" * 150
    soup = BeautifulSoup(nested_html, "html.parser")
    
    builder = HierarchyBuilder(max_nodes=1000, max_depth=100)
    tree = builder.build_hierarchy(soup)
    
    # Assert depth reaches exactly 100 and truncates
    def check_max_depth(node, current_depth=0):
        assert current_depth <= 100
        max_d = current_depth
        for child in node.get("children", []):
            max_d = max(max_d, check_max_depth(child, current_depth + 1))
        return max_d
        
    resolved_depth = check_max_depth(tree)
    assert resolved_depth == 100

def test_hierarchy_node_count_limit_guards():
    # Construct wide page with > 6000 sibling div elements
    wide_html = "<body>" + "<div></div>" * 6000 + "</body>"
    soup = BeautifulSoup(wide_html, "html.parser")
    
    builder = HierarchyBuilder(max_nodes=5000, max_depth=50)
    tree = builder.build_hierarchy(soup)
    
    # Assert node_count limit guard was hit
    assert builder.node_count == 5001

# ---------------------------------------------------------
# DOM Analyzer Database Operations Tests
# ---------------------------------------------------------
@pytest.mark.asyncio
async def test_dom_analyzer_pipeline_and_db_upsert():
    html_content = "<html><body><header></header><section>Welcome</section></body></html>"
    analyzer = DOMAnalyzer()

    mock_session = AsyncMock()
    mock_session.__aenter__.return_value = mock_session
    mock_session.add = MagicMock()
    mock_session.delete = MagicMock()
    mock_session.flush = AsyncMock()
    
    mock_session.begin = MagicMock()
    mock_begin_context = MagicMock()
    mock_begin_context.__aenter__ = AsyncMock(return_value=None)
    mock_begin_context.__aexit__ = AsyncMock(return_value=False)
    mock_session.begin.return_value = mock_begin_context
    
    # Mock query results (no existing record)
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = None
    mock_session.execute.return_value = mock_result
    
    mock_session_factory = MagicMock()
    mock_session_factory.return_value.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session_factory.return_value.__aexit__ = AsyncMock(return_value=False)
    
    with patch("agents.prototype.dom_analyzer.db_manager") as mock_db_mgr:
        mock_db_mgr.session_factory = mock_session_factory
        
        # Execute analysis and database storage
        res = await analyzer.analyze(html_content, job_id=88)
        
        assert res["success"] is True
        assert res["status"] == "ANALYZED"
        assert len(res["sections"]) == 2  # header and section elements
        
        # Verify db insert called
        assert mock_session.add.called
        added_obj = mock_session.add.call_args[0][0]
        assert isinstance(added_obj, PrototypeDOMAnalysis)
        assert added_obj.job_id == 88
        assert added_obj.section_count == 2

@pytest.mark.asyncio
async def test_dom_analyzer_deduplication():
    html_content = "<html><body><header></header><section>Welcome</section></body></html>"
    analyzer = DOMAnalyzer()

    mock_session = AsyncMock()
    mock_session.__aenter__.return_value = mock_session
    mock_session.add = MagicMock()
    mock_session.delete = MagicMock()
    mock_session.flush = AsyncMock()
    
    mock_session.begin = MagicMock()
    mock_begin_context = MagicMock()
    mock_begin_context.__aenter__ = AsyncMock(return_value=None)
    mock_begin_context.__aexit__ = AsyncMock(return_value=False)
    mock_session.begin.return_value = mock_begin_context
    
    # Mock existing record (deduplication update check)
    existing_record = PrototypeDOMAnalysis(id=99, job_id=12, section_count=1, cta_count=0)
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = existing_record
    mock_session.execute.return_value = mock_result
    
    mock_session_factory = MagicMock()
    mock_session_factory.return_value.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session_factory.return_value.__aexit__ = AsyncMock(return_value=False)
    
    with patch("agents.prototype.dom_analyzer.db_manager") as mock_db_mgr:
        mock_db_mgr.session_factory = mock_session_factory
        
        res = await analyzer.analyze(html_content, job_id=12)
        
        assert res["success"] is True
        # Verify it updated existing instead of creating new
        assert not mock_session.add.called
        assert existing_record.section_count == 2  # updated count
        assert existing_record.status == "ANALYZED"
