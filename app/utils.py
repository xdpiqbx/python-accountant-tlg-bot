from datetime import datetime


def reformat_datetime_from_db(dt):
    # Original datetime string
    # dt = "2025-03-14 13:09:59.498756"
    # Parse the string into a datetime object
    dt_obj = datetime.strptime(str(dt), "%Y-%m-%d %H:%M:%S.%f")
    # Format the datetime object into the desired format
    # return dt_obj.strftime("%d.%m.%Y %H:%M")
    return dt_obj.strftime("%d.%m.%Y")
