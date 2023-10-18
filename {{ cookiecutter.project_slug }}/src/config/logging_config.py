import logging
import os


def get_logger(name, path=None, filename="logs.log", show=False, reset=False):
    """
    Configure and return a logger.

    Parameters:
    - name (str): The name of the logger.
    - path (str, optional): The directory where the log file will be stored.
                            If None, the log file will not be saved. Defaults to None.
    - filename (str, optional): The name of the log file. Must end with '.log'. Defaults to 'logs.log'.
    - show (bool, optional): Whether to print logs to the console. Defaults to False.
    - reset (bool, optional): Whether to overwrite the existing log file. Defaults to False.

    Returns:
    - logging.Logger: A configured logger instance.

    Example:
    >>> logger = get_logger(__name__, path="/path/to/logs", filename="my_log.log", show=True, reset=True)
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(module)s | %(message)s"
    )

    if path:
        # Create the directory if it doesn't exist
        if not os.path.exists(path):
            os.makedirs(path)

        file_mode = "w" if reset else "a"
        file_handler = logging.FileHandler(os.path.join(path, filename), mode=file_mode)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    if show:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    return logger
