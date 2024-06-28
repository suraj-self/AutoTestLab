import schedule
import time
import subprocess

def run_selenium_script():
    print("Running Selenium script...")
    try:
        subprocess.run(['python', 'ecom.py'])  # Replace 'python' with your Python interpreter path if needed
        print("Selenium script execution completed.")
    except Exception as e:
        print(f"Error running Selenium script: {e}")

# Schedule the job to run every 5 minutes
schedule.every(1).minutes.do(run_selenium_script)

# Main loop to keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
