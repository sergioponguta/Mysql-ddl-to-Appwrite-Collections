from utils.utils import generate_datetime_now
import re
import json


def list_ddl_tables(ddl):
    create_table_regex = r"CREATE TABLE (\w+) \(([\s\S]+?)\);"

    matches = re.findall(create_table_regex, ddl)
    table_list = []
    for match in matches:
        table_name = match[0]
        table_content = match[1]
        table_list.append(f"CREATE TABLE {table_name} ({table_content});")
    return table_list


def ddl_table_to_json(ddl, db_id: str):
    # Extract table name
    table_name = re.search(r'CREATE TABLE (\w+)', ddl).group(1)

    # Extract column definitions
    column_defs = re.findall(
        r'(\w+)\s+(\w+)(?:\((.*?)\))?(?:\s+NOT\s+NULL|\s+NULL)?(?:\s+DEFAULT\s+(.*?))?(?=.*?(?:\s+UNIQUE|\s+PRIMARY\s+KEY|\s+ENUM\((.*?)\)))?', ddl)

    # Create JSON schema
    json_schema = {
        "$id": table_name.lower(),
        "$createdAt": generate_datetime_now(),
        "$updatedAt": generate_datetime_now(),
        "$permissions": [],
        "databaseId": db_id,
        "name": table_name.upper(),
        "enabled": True,
        "attributes": []
    }

    # Initialize unique indexes and primary key list
    unique_indexes = []
    primary_key = []

    for col_def in column_defs:
        col_name, col_type, col_size, col_default, col_enum = col_def[:5]

        # Skip this
        if col_name in ['CREATE', 'PRIMARY', 'KEY', "UNIQUE"]:
            continue

        # Check if the column is an ENUM type
        if col_type == 'ENUM':
            col_enum = col_size
            col_size = None

        # Create JSON object for column
        col_schema = {
            "key": col_name,
            "type": col_type,
            "status": "available",
            "required": 'NOT NULL' in ddl.split(col_name)[1].split(',')[0],
            "array": False,
            "default": col_default.strip() if col_default else None
        }

        # Map SQL data types to JSON data types and handle ENUM values
        if col_type in ['INT', 'INTEGER', 'TINYINT', 'SMALLINT', 'MEDIUMINT', 'BIGINT']:
            col_schema["type"] = 'integer'
            col_schema["min"] = -9223372036854775808
            col_schema["max"] = 9223372036854775807
        elif col_type in ['FLOAT', 'DOUBLE', 'DECIMAL']:
            col_schema["type"] = 'double'
            col_schema["min"] = -1.7976931348623157e308
            col_schema["max"] = 1.7976931348623157e308
        elif col_type in ['CHAR', 'VARCHAR', 'TEXT', 'TINYTEXT', 'MEDIUMTEXT', 'LONGTEXT']:
            col_schema["type"] = 'string'
            col_schema["size"] = int(col_size) if col_size else None
        elif col_type in ['DATE', 'TIME', 'DATETIME', 'TIMESTAMP']:
            col_schema["type"] = 'datetime'
            col_schema["format"] = ""
        elif col_type == 'ENUM':
            col_schema["type"] = 'string'
            col_schema["format"] = "enum"
            col_schema["elements"] = col_enum.replace("'", "").split(",") if col_enum else None

        # Add column to JSON schema
        json_schema["attributes"].append(col_schema)

        # Check if the column has the UNIQUE keyword
        if 'UNIQUE' in ddl.split(col_name)[1].split(',')[0]:
            unique_indexes.append(col_name)

        # Check if the column has the PRIMARY KEY keyword
        if 'PRIMARY KEY' in ddl.split(col_name)[1].split(',')[0]:
            col_schema["required"] = True
            primary_key.append(col_name)

    # Add primary key index
    json_schema["indexes"] = [
        {
            "key": f"IDX_{table_name.upper()}_PK"[:35],
            "type": "unique",
            "status": "available",
            "attributes": primary_key,
            "orders": ["DESC"]
        }
    ]

    # Add unique indexes
    if unique_indexes:
        for col in unique_indexes:
            json_schema["indexes"].append({
                "key": f"IDX_{table_name.upper()}_UQ_{col.upper()}"[:35],
                "type": "unique",
                "status": "available",
                "attributes": [col],
                "orders": ["DESC"]
            })

    # Strip elements of ENUM values
    for i in json_schema["attributes"]:
        if "elements" in i:
            i["elements"] = [x.strip() for x in i["elements"]]

    # Convert JSON schema to string
    json_string = json.dumps(json_schema, indent=2)

    return json_string
