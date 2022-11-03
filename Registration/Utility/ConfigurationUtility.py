import datetime


def convert_db_datetime(req_date_time):
    try:
        req_date_time = req_date_time.strftime("%Y-%m-%d %H:%M:%S")
        date_time = datetime.datetime.strptime(req_date_time, "%Y-%m-%d %H:%M:%S")
        return date_time

    except Exception as err:
        print(str(err))
        return None