import subprocess
import asyncio
from core.logger import logger

class MXValidator:
    @staticmethod
    async def validate_mx(domain: str, timeout: float = 2.0) -> bool:
        """
        Verify if the domain has active MX records using nslookup.
        """
        if not domain:
            return False
            
        # Standard loopback check
        if domain in ["localhost", "127.0.0.1", "0.0.0.0"] or "provider" in domain:
            return False

        def run_nslookup():
            try:
                # startupinfo is used to hide console popups on Windows
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                
                result = subprocess.run(
                    ["nslookup", "-query=mx", domain],
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    startupinfo=startupinfo
                )
                output = result.stdout.lower()
                
                # Check for indicators of MX records
                if "mail exchanger" in output or "mx preference" in output or "exchanger" in output:
                    return True
                return False
            except Exception as e:
                logger.warning(f"MX lookup: Error executing nslookup for '{domain}': {e}")
                return False

        try:
            has_mx = await asyncio.wait_for(asyncio.to_thread(run_nslookup), timeout=timeout + 0.5)
            logger.debug(f"MX lookup for domain '{domain}': active={has_mx}")
            return has_mx
        except asyncio.TimeoutError:
            logger.warning(f"MX lookup: Timeout querying MX records for '{domain}'")
            return False
        except Exception as e:
            logger.warning(f"MX lookup: Exception checking MX for '{domain}': {e}")
            return False
