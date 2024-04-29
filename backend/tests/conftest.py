import logging


def pytest_configure(config):
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
