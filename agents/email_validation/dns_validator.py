import socket
import asyncio
from core.logger import logger

class DNSValidator:
    @staticmethod
    async def validate_domain(domain: str, timeout: float = 2.0) -> bool:
        """
        Verify if the domain resolves to a valid IP address.
        """
        if not domain:
            return False
            
        def lookup():
            try:
                socket.gethostbyname(domain)
                return True
            except Exception:
                return False

        try:
            resolved = await asyncio.wait_for(asyncio.to_thread(lookup), timeout=timeout)
            logger.debug(f"DNS check for domain '{domain}': resolved={resolved}")
            return resolved
        except asyncio.TimeoutError:
            logger.warning(f"DNS check: Timeout resolving domain '{domain}'")
            return False
        except Exception as e:
            logger.warning(f"DNS check: Exception resolving domain '{domain}': {e}")
            return False
