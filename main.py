import utils.utils as utils
import ddl_to_appwrite as converter
import json
import sys

DB_ID = "test_db"


def main():
    print("Process started...")
    try:
        print("Reading ddl.sql...")
        sql_files = utils.list_sql_files()
        for file in sql_files:
            file_name = file.split(".")[0]
            ddl_script = utils.read_file(f"../sql/{file}")
            ddl_refined = utils.remove_backtick(ddl_script)
            ddl_refined = utils.fix_enum(ddl_refined)
            table_list = converter.list_ddl_tables(ddl_refined)

            collections_result = {"collections": []}

            for table in table_list:
                json_schema = converter.ddl_table_to_json(table, DB_ID)
                json_schema = json.loads(json_schema)
                collections_result["collections"].append(json_schema)

            # Uncomment this to print the result
            # print(json.dumps(collections_result, indent=2))

            print("Writing to result.json...")
            utils.write_file(f"../result/{file_name}.json", json.dumps(collections_result, indent=2))

        print("Process completed...")
    except Exception as e:
        print(e)
        print("Process failed...")
        sys.exit(1)


if __name__ == "__main__":
    main()
