
import requests
import time
import logging

from datetime import datetime
from logging.handlers import RotatingFileHandler

from config import REQUEST_TIMEOUT, LOG_FILE, MAX_LOG_SIZE, BACKUP_COUNT


# Configure rotating log handler
logger = logging.getLogger("website_monitor")
logger.setLevel(logging.INFO)

if not logger.handlers:

    handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=MAX_LOG_SIZE,
        backupCount=BACKUP_COUNT
    )

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)


def check_website(url):

    print("\nChecking website:", url)

    start_time = time.perf_counter()

    try:

        response = requests.get(
            url,
            timeout=REQUEST_TIMEOUT
        )

        response_time = round(
            (time.perf_counter() - start_time) * 1000, 2
        )

        status_code = response.status_code

        if 200 <= status_code < 400:

            status = "ONLINE"

            logger.info(
                "%s | %s | HTTP %s | %s ms",
                url, status, status_code, response_time
            )

            success = True

        elif 400 <= status_code < 500:

            status = "CLIENT ERROR"

            logger.warning(
                "%s | %s | HTTP %s | %s ms",
                url, status, status_code, response_time
            )

            success = False

        else:

            status = "SERVER ERROR"

            logger.error(
                "%s | %s | HTTP %s | %s ms",
                url, status, status_code, response_time
            )

            success = False

        print("Status:", status)
        print("HTTP Code:", status_code)
        print("Response Time:", response_time, "ms")
        print("Checked At:", datetime.now())

        return success

    except requests.exceptions.Timeout:

        elapsed = round(
            (time.perf_counter() - start_time) * 1000, 2
        )

        print("ERROR: Request timed out!")

        logger.error(
            "%s | TIMEOUT | %s ms", url, elapsed
        )

        return False

    except requests.exceptions.ConnectionError:

        print("ERROR: Connection failed!")

        logger.exception(
            "%s | CONNECTION ERROR", url
        )

        return False

    except requests.exceptions.RequestException:

        print("ERROR: Request failed!")

        logger.exception(
            "%s | REQUEST ERROR", url
        )

        return False

    except Exception:

        print("ERROR: Unexpected failure!")

        logger.exception(
            "%s | UNEXPECTED ERROR", url
        )

        return False
