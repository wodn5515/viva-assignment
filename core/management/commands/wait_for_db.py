import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management import BaseCommand


class Command(BaseCommand):
    """docker 컨테이너에서 DB가 사용가능해질때까지 대기"""

    def handle(self, *args, **options):
        db_conn_default_check, db_conn_mongo_check = None, None
        while not (db_conn_default_check and db_conn_mongo_check):
            try:
                db_conn_default = connections["default"]
                db_conn_mongo = connections["mongo"]
                db_conn_default.cursor()
                db_conn_mongo.cursor()
            except OperationalError:
                time.sleep(1)
            else:
                db_conn_default_check, db_conn_mongo_check = True, True
