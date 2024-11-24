import subprocess
import logging
import os

def run_script(script_name, logger):
    logger.info(f"Starting script: {script_name}")
    result = subprocess.run(
        ['C:\\Users\\yapte\\AppData\\Local\\Programs\\Python\\Python310\\python.exe', script_name],
        capture_output=True,
        text=True
    )
    if result.stdout:
        logger.info(f"Output of {script_name}:\n{result.stdout}")
    if result.stderr:
        logger.error(f"Errors in {script_name}:\n{result.stderr}")



if __name__ == "__main__":
    # Configure logging
    log_file = os.path.join(os.path.dirname(__file__), 'pipeline.log')
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger()

    scripts = ['scraper.py', 'sanitise.py', 'feature_transformation.py']
    # scripts = ['scraper.py', 'sanitise.py', 'feature_transformation.py', 'labeling_data.py', 'model.py', 'cleanup_files.py']
    for script in scripts:
        run_script(script, logger)