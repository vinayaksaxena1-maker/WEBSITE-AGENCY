import http.server
import socketserver
import threading
from core.logger import logger

class PreviewServer:
    def __init__(self, directory: str = "output/prototypes", port: int = 8088):
        self.directory = directory
        self.port = port
        self.server = None
        self.thread = None

    def start(self) -> None:
        """
        Starts local HTTP server inside background daemon thread.
        """
        # Custom handler to map base directories
        class CustomHTTPHandler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=directory_alias, **kwargs)

        directory_alias = self.directory

        # Bind to randomized port if primary fails or standard ports
        socketserver.TCPServer.allow_reuse_address = True
        try:
            self.server = socketserver.TCPServer(("", self.port), CustomHTTPHandler)
            logger.info(f"PreviewServer: Spawning server context on port {self.port}")
        except Exception as e:
            # Fallback to random free port
            self.port = 8089
            self.server = socketserver.TCPServer(("", self.port), CustomHTTPHandler)
            logger.info(f"PreviewServer: Port occupied. Falling back to port {self.port}")

        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def stop(self) -> None:
        """
        Cleans up server socket connection context.
        """
        if self.server:
            logger.info("PreviewServer: Shutting down preview server session sockets...")
            self.server.shutdown()
            self.server.server_close()
            if self.thread:
                self.thread.join(timeout=1.0)
            logger.info("PreviewServer: Server stopped cleanly.")
