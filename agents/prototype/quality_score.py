from typing import Dict

class QualityScore:
    @staticmethod
    def calculate_overall_score(metrics: Dict[str, int]) -> int:
        """
        Calculates weighted average of quality metrics conforming to EDK weight rules.
        """
        # Weight Ratios:
        # html: 15%, accessibility: 15%, performance: 10%, responsive: 15%,
        # seo: 15%, ux: 10%, visual: 10%, component: 10%
        w_html = metrics.get("html", 100) * 0.15
        w_acc = metrics.get("accessibility", 100) * 0.15
        w_perf = metrics.get("performance", 100) * 0.10
        w_resp = metrics.get("responsive", 100) * 0.15
        w_seo = metrics.get("seo", 100) * 0.15
        w_ux = metrics.get("ux", 100) * 0.10
        w_vis = metrics.get("visual", 100) * 0.10
        w_comp = metrics.get("component", 100) * 0.10
        
        overall = w_html + w_acc + w_perf + w_resp + w_seo + w_ux + w_vis + w_comp
        return int(round(overall))
