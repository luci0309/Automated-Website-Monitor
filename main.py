
import schedule
import time
import logging

from monitor import check_website, logger
from config import WEBSITES, CHECK_INTERVAL


def monitor_all_websites():

    print("\n" + "=" * 45)
    print("AUTOMATED WEBSITE MONITORING")
    print("=" * 45)

    total = len(WEBSITES)
    successful = 0
    failed = 0

    for website in WEBSITES:

        result = check_website(website)

        if result:
            successful += 1
        else:
            failed += 1

    # Display monitoring summary
    print("\nMONITORING SUMMARY")
    print("-" * 30)
    print("Total Websites:", total)
    print("Successful:", successful)
    print("Failed:", failed)
    print("-" * 30)

    logger.info(
    "Monitoring summary | Total: %s | Successful: %s | Failed: %s",
    total, successful, failed
)


def start_monitoring():

    print("Website Monitoring System Started!")
    print("Monitoring Interval:", CHECK_INTERVAL, "seconds")
    print("Press CTRL + C to stop.")

    # Perform first check immediately
    monitor_all_websites()

    # Schedule future checks
    schedule.every(CHECK_INTERVAL).seconds.do(
        monitor_all_websites
    )

    try:

        while True:

            schedule.run_pending()

            time.sleep(1)

    except KeyboardInterrupt:

        print("\nMonitoring stopped by user.")

        logging.info("Monitoring stopped by user.")


if __name__ == "__main__":

    start_monitoring()
