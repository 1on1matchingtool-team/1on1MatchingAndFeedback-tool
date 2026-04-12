from datetime import datetime, date

def parse_date(date_str):
    if not date_str:
        return None
    return datetime.strptime(date_str, "%Y-%m-%d").date()

def parse_db_date(value):
    if not value:
        return None

    # Case 1: Already a date object
    if isinstance(value, date) and not isinstance(value, datetime):
        return value

    # Case 2: Already a datetime object
    if isinstance(value, datetime):
        return value.date()

    # Case 3: Flask JSON datetime string
    if isinstance(value, str):
        try:
            return datetime.strptime(value, "%a, %d %b %Y %H:%M:%S GMT").date()
        except:
            pass

        # Case 4: ISO format (YYYY-MM-DD)
        try:
            return datetime.fromisoformat(value).date()
        except:
            pass

    # If all fails
    return None