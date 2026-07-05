import logging
import json
import sys
from datetime import datetime, timezone
import contextvars

# Context variable to hold the correlation ID for request tracing
correlation_id_ctx = contextvars.ContextVar("correlation_id", default="SYSTEM")

class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_payload = {
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "level": record.levelname,
            "module": record.name,
            "message": record.getMessage(),
            "correlation_id": correlation_id_ctx.get()
        }
        
        # Check if an explicit correlation_id was passed via extra
        if hasattr(record, "correlation_id"):
            log_payload["correlation_id"] = record.correlation_id
            
        if record.exc_info:
            log_payload["exception"] = self.formatException(record.exc_info)
            
        return json.dumps(log_payload)

def setup_logger(name: str = "agency", level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Prevent handler duplication
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JSONFormatter())
        logger.addHandler(handler)
        logger.propagate = False
        
    return logger

logger = setup_logger()
