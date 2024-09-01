#!/bin/bash
# The purpose of this bash script is to automate the execution of a Puppeteer script (ecom.js) using Node.js. 
# It sets up a scheduled task (cron job) to run the Puppeteer script periodically.
# Navigate to the directory where your script is located
cd /home/suraj/sentiment-analysis/puppeteer/ || exit 1

# Run your Puppeteer script using Node.js
/home/suraj/.nvm/versions/node/v22.3.0/bin/node ecom.js >> /home/suraj/sentiment-analysis/puppeteer/cron.log 2>&1