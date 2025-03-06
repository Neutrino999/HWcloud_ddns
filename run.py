import os
import time
import subprocess
from datetime import datetime

def run_script():
    result = subprocess.run(['python', 'getip.py'], capture_output=True, text=True)
    print(f"Execution Time: {datetime.now()}")
    print(f"Script Output:\n{result.stdout}")

def clear_output():
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    while True:
        run_script()
        time.sleep(1800)  # Run every 30 minutes
        clear_output()
