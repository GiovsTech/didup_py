from datetime import datetime

def format(date):
    ## Date argument can be in these different types: "str", int or float, datetime object
    if isinstance(date, (int,float)):
        date = datetime.fromtimestamp(date)
    elif isinstance(date, str):
        date = datetime.fromisoformat(date)
    elif not isinstance(date, datetime):
        raise ValueError("Invalid date format")
    return date.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

if __name__ == '__main__':
    print(format("2021-09-02T17:16:49.330690"))
