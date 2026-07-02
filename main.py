#!/usr/bin/env python3
"""
Main entry point that runs both Flask API and Telegram bot simultaneously.
Works around asyncio event loop conflicts on Render.
"""

import os
import sys
import signal
import logging
from multiprocessing import Process
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import Flask app
from expense_bot import flask_app, run_telegram_bot, FLASK_PORT

def run_flask_process():
    """Run Flask in a separate process"""
    logger.info(f"Starting Flask API on port {FLASK_PORT}...")
    flask_app.run(host="0.0.0.0", port=FLASK_PORT, debug=False, use_reloader=False)

def run_telegram_process():
    """Run Telegram bot in a separate process"""
    logger.info("Starting Telegram bot...")
    run_telegram_bot()

def main():
    """Start both Flask and Telegram bot processes"""
    # Create processes
    flask_process = Process(target=run_flask_process, name="Flask")
    telegram_process = Process(target=run_telegram_process, name="Telegram")

    # Set as daemon processes
    flask_process.daemon = True
    telegram_process.daemon = True

    try:
        # Start both processes
        logger.info("Launching Flask API and Telegram bot...")
        flask_process.start()
        time.sleep(1)  # Give Flask a moment to start
        telegram_process.start()

        # Wait for both processes
        flask_process.join()
        telegram_process.join()

    except KeyboardInterrupt:
        logger.info("Shutting down...")
        flask_process.terminate()
        telegram_process.terminate()
        flask_process.join()
        telegram_process.join()
        logger.info("Shutdown complete")

if __name__ == "__main__":
    main()
