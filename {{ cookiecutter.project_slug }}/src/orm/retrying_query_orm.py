from sqlalchemy.orm.query import Query as _Query
from sqlalchemy.exc import OperationalError, StatementError
from time import sleep
from dotenv import load_dotenv
import os
load_dotenv()


class RetryingQuery(_Query):

    __retry_count__ = 10
    __retry_sleep_interval_sec__ = 60

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __iter__(self):
        attempts = 0
        while True:
            attempts += 1
            try:
                return super().__iter__()
            except OperationalError as ex:
                if "Lost connection to MySQL server during query" not in str(ex):
                    raise
                if attempts < self.__retry_count__:
                    print(f"MySQL connection lost - sleeping for {self.__retry_sleep_interval_sec__}"
                          f" sec and will retry (attempt {attempts})")
                    sleep(self.__retry_sleep_interval_sec__)
                    continue
                else:
                    raise
            except StatementError as ex:
                if "reconnect until invalid transaction is rolled back" not in str(ex):
                    raise
                self.session.rollback()
