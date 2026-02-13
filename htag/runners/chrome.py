import time
import subprocess
import threading
import logging
import uvicorn
from .base import BaseRunner

logger = logging.getLogger("htagravity")

class ChromeApp(BaseRunner):
    """
    Executes an App in a Chrome/Chromium kiosk window.
    Features auto-cleanup of temporary browser profiles.
    """
    def __init__(self, app: "App", kiosk=True, width=800, height=600):
        super().__init__(app)
        self.kiosk = kiosk
        self.width = width
        self.height = height

    def run(self, host="127.0.0.1", port=8000):
        if self.kiosk:
            def launch():
                time.sleep(1)  # Give the server a second to start
                
                import tempfile
                import shutil
                import atexit
                tmp_dir = tempfile.mkdtemp(prefix="htagravity_")
                
                def cleanup():
                    try:
                        shutil.rmtree(tmp_dir)
                        logger.info("Cleaned up temporary browser profile: %s", tmp_dir)
                    except:
                        pass
                
                atexit.register(cleanup)
                # Cleanup logic will be attached to instances via on_instance callback
                self._cleanup_func = cleanup
                
                browsers = ["google-chrome", "chromium-browser", "chromium", "chrome"]
                found = False
                
                for browser in browsers:
                    try:
                        subprocess.Popen([
                            browser, 
                            f"--app=http://{host}:{port}", 
                            f"--window-size={self.width},{self.height}",
                            f"--user-data-dir={tmp_dir}",
                            "--no-first-run",
                            "--no-default-browser-check"
                        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        logger.info("Launched %s with window size %dx%d", browser, self.width, self.height)
                        found = True
                        break
                    except FileNotFoundError:
                        continue
                    except Exception as e:
                        logger.error("Error launching %s: %s", browser, e)
                        continue
                
                if not found:
                    logger.warning("Could not launch any browser (tried: %s)", ", ".join(browsers))

            threading.Thread(target=launch, daemon=True).start()

        from ..server import WebServer
        # Use on_instance to attach cleanup if it's defined (kiosk mode only)
        on_inst = None
        if hasattr(self, "_cleanup_func"):
            on_inst = lambda inst: setattr(inst, "_browser_cleanup", self._cleanup_func)
            
        ws = WebServer(self.app, on_instance=on_inst)
        uvicorn.run(ws.app, host=host, port=port)
