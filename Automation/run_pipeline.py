import subprocess

def run_script(script_name):
    result = subprocess.run(['python', script_name], capture_output=True, text=True)
    print(f"Running {script_name}:\n{result.stdout}\n{result.stderr}")

if __name__ == "__main__":
    scripts = ['scraper.py', 'sanitise.py', 'feature_transformation.py', 'labeling_data.py', 'model.py', 'cleanup_files.py']
    
    for script in scripts:
        run_script(script)
