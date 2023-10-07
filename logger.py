import pathlib
from typing import Optional, List, Any
from datetime import datetime
import subprocess
import logging
import sys

EXPERIMENT_DIR: Optional[pathlib.Path] = None

class Logger:
    def __init__(self, handle: str = 'sandbox'):
        self.handle = handle

    def _run_subprocess(self, command: List[str]):
        """Execute command in shell and return output"""
        return subprocess.check_output(command).decode("utf-8").strip()
    
    def get_git_root(self):
        """Get git root directory"""
        return self._run_subprocess(["git", "rev-parse", "--show-toplevel"])
    
    def init_experiment(
            self,
            experiments: Optional[pathlib.Path] = None,
            log_to_file=True,
            log_to_stdout=True,
        ):

        if experiments is None:
            experiments = pathlib.Path(self.get_git_root()) / "experiments"

        global EXPERIMENT_DIR
        # assert EXPERIMENT_DIR is None
        datetime_now = datetime.now()
        date = datetime_now.strftime("%Y%m%d")
        timestamp = int(datetime_now.timestamp())
        EXPERIMENT_DIR = experiments / self.handle / f"{date}-{timestamp}"
        EXPERIMENT_DIR.mkdir(parents=True)     
        logfile = EXPERIMENT_DIR / "default.log"
        handlers = []
        if log_to_file:
            handlers.append(logging.FileHandler(filename=logfile))
        if log_to_stdout:
            handlers.append(logging.StreamHandler(sys.stdout))
        logging.basicConfig(
            level=logging.INFO,
            format="{asctime} {levelname} [{filename:s}:{lineno:d}] {message}",
            datefmt="%Y-%m-%d %H:%M:%S",
            handlers=handlers,
            style="{",
        )
        if log_to_file:
            logging.info(f"Logging to {logfile}")
        
    def save_to_file(self, response: str, output_dir: str = None, file_name: str = "output.txt"):
        if output_dir is None:
            output_dir = EXPERIMENT_DIR

        with open(output_dir / file_name, 'w') as f:
            f.write(response)