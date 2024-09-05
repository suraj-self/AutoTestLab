import schedule
import time
from auto_pilot_code import run_selenium_script  # Import the function directly

def schedule_selenium_script():
    print("Running Selenium script...")
    try:
        run_selenium_script()  # Call the function directly
        print("Selenium script execution completed.")
    except Exception as e:
        print(f"Error running Selenium script: {e}")

# Schedule the job to run every 60 minute
schedule.every(60).minutes.do(schedule_selenium_script)

# Main loop to keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
