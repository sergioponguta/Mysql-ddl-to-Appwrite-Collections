import datetime
import os


def generate_datetime_now():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%dT%H:%M:%S.%f+00:00")


def remove_backtick(text):
    text = text.replace('`', '')
    return text


def fix_enum(text):
    # Needed
    text = text.replace('ENUM (', 'ENUM(')
    return text


def list_sql_files():
    sql_files = []
    for file in os.listdir("./sql"):
        if file.endswith(".sql"):
            sql_files.append(file)
    return sql_files


def read_file(file_name):
    with open(file_name, "r") as f:
        return f.read()


def write_file(file_name, content):
    with open(file_name, "w") as f:
        f.write(content)
