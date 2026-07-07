import re
from agents.email.email_contracts import ValidatedEmailDraft, FormattedEmailPackage

class OutputFormatter:
    @staticmethod
    def format_output(validated_email: ValidatedEmailDraft) -> FormattedEmailPackage:
        """
        Wraps email content in clean, compliant HTML templates, normalizing spacing.
        """
        subject = validated_email.subject.strip()
        body_text = validated_email.body.strip()
        target_email = validated_email.target_email
        
        # Spacing Normalization: trim line spaces, collapse 3+ consecutive newlines into 2
        lines = [line.strip() for line in body_text.split('\n')]
        normalized_body = "\n".join(lines)
        normalized_body = re.sub(r'\n{3,}', '\n\n', normalized_body)
        
        # Convert line breaks to HTML paragraphs
        html_paragraphs = "".join([f"<p style='margin: 0 0 1em 0;'>{p.replace('\n', '<br>')}</p>" for p in normalized_body.split("\n\n") if p.strip()])
        
        html_layout = (
            "<!DOCTYPE html>\n"
            "<html>\n"
            "<head>\n"
            "  <meta charset='utf-8'>\n"
            "  <style>\n"
            "    body { font-family: sans-serif; line-height: 1.5; color: #333333; margin: 0; padding: 20px; }\n"
            "    .container { max-width: 600px; margin: 0 auto; background: #ffffff; padding: 20px; border: 1px solid #e0e0e0; border-radius: 8px; }\n"
            "  </style>\n"
            "</head>\n"
            "<body>\n"
            "  <div class='container'>\n"
            f"    {html_paragraphs}\n"
            "  </div>\n"
            "</body>\n"
            "</html>"
        )
        
        return FormattedEmailPackage(
            subject=subject,
            html_body=html_layout,
            text_body=normalized_body,
            target_email=target_email
        )
