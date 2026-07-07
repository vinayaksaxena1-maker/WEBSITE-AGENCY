class PipelineValidator:
    @staticmethod
    def verify_pipeline_stages() -> bool:
        """
        Validates pipeline sequencing flow.
        """
        from agents.prototype.prototype_pipeline import PrototypePipeline
        pipeline = PrototypePipeline()
        
        stages = [
            ("browser", pipeline.browser),
            ("screenshot_engine", pipeline.screenshot_engine),
            ("dom_analyzer", pipeline.dom_analyzer),
            ("visual_analyzer", pipeline.visual_analyzer),
            ("theme_engine", pipeline.theme_engine),
            ("layout_engine", pipeline.layout_engine),
            ("component_engine", pipeline.component_engine),
            ("responsive_engine", pipeline.responsive_engine),
            ("html_generator", pipeline.html_generator),
            ("preview_generator", pipeline.preview_generator),
            ("quality_analyzer", pipeline.quality_analyzer)
        ]
        
        for name, stage in stages:
            if stage is None:
                return False
        return True
