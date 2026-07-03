#!/usr/bin/env python3
"""
Main entry point that runs both Flask API and Telegram bot simultaneously.
Uses multiprocessing with proper signal handling.
"""

import os
import sys
import signal
import logging
from multiprocessing import Process
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import from expense_bot
from expense_bot import flask_app, run_telegram_bot, FLASK_PORT

# Global references for signal handler
processes = []

def shutdown(signum=None, frame=None, exit_code=0):
    """Terminate child processes gracefully"""
    logger.info("Shutting down child processes...")
    for p in processes:
        if p.is_alive():
            p.terminate()
            p.join(timeout=5)
            if p.is_alive():
                p.kill()
    logger.info("All processes terminated.")
    sys.exit(exit_code)

def run_flask_process():
    """Run Flask API (blocking)"""
    logger.info(f"Starting Flask API on port {FLASK_PORT}...")
    flask_app.run(host="0.0.0.0", port=FLASK_PORT, debug=False, use_reloader=False)

def run_telegram_process():
    """Run Telegram bot (blocking)"""
    logger.info("Starting Telegram bot...")
    run_telegram_bot()

def main():
    """Start both Flask and Telegram bot processes"""
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)

    # Create processes (non-daemon so they stay alive)
    flask_process = Process(target=run_flask_process, name="Flask")
    telegram_process = Process(target=run_telegram_process, name="Telegram")

    processes.extend([flask_process, telegram_process])

    try:
        logger.info("Launching Flask API and Telegram bot...")
        flask_process.start()
        time.sleep(1)  # let Flask bind port
        telegram_process.start()

        # Poll both processes. If either dies unexpectedly, tear the whole
        # service down and exit non-zero so Render restarts it cleanly --
        # previously this only ever joined on Flask, so a crashed Telegram
        # process went unnoticed forever while Flask kept running alone.
        while True:
            time.sleep(5)
            if not flask_process.is_alive():
                logger.error("Flask process died unexpectedly. Shutting down.")
                shutdown(exit_code=1)
            if not telegram_process.is_alive():
                logger.error("Telegram process died unexpectedly. Shutting down.")
                shutdown(exit_code=1)

    except KeyboardInterrupt:
        shutdown()
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        shutdown()

if __name__ == "__main__":
    main()
