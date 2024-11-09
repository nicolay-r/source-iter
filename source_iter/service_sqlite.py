import sqlite3


class SQLite3Service(object):

    @staticmethod
    def __create_table(table_name, columns, id_column_name,
                       id_column_type, cur, sqlite3_column_types=None):

        # Setting up default column types.
        if sqlite3_column_types is None:
            types_count = len(columns) if id_column_name in columns else len(columns) - 1
            sqlite3_column_types = ["TEXT"] * types_count

        # Provide the ID column.
        sqlite3_column_types = [id_column_type] + sqlite3_column_types

        # Compose the whole columns list.
        content = ", ".join([f"[{item[0]}] {item[1]}" for item in zip(columns, sqlite3_column_types)])
        cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name}({content})")
        cur.execute(f"CREATE INDEX IF NOT EXISTS [{id_column_name}] ON {table_name}([{id_column_name}])")

    @staticmethod
    def write_missed(data_it, target, table_name, columns=None, data2col_func=None, id_column_name="id",
                     id_column_type="INTEGER", sqlite3_column_types=None, it_type='dict',
                     create_table_if_not_exist=True, **connect_kwargs):

        need_set_column_id = True
        need_initialize_columns = columns is None

        # Setup default columns.
        columns = [] if columns is None else columns

        with sqlite3.connect(target, **connect_kwargs) as con:
            cur = con.cursor()

            for content in data_it:

                if it_type == 'dict':
                    # Extracting columns from data.
                    data = content
                    uid = data[id_column_name]
                    row_columns = list(data.keys())
                    row_params_func = lambda: [data2col_func(c, data) if data2col_func is not None else data[c]
                                               for c in row_columns]
                    # Append columns if needed.
                    if need_initialize_columns:
                        columns = list(row_columns)
                elif it_type is None:
                    # Setup row columns.
                    uid, data = content
                    row_columns = columns
                    row_params_func = lambda: [uid] + data
                else:
                    raise Exception(f"it_type {it_type} does not supported!")

                if need_set_column_id:
                    # Register ID column.
                    if id_column_name not in columns:
                        columns.append(id_column_name)
                    # Place ID column first.
                    columns.insert(0, columns.pop(columns.index(id_column_name)))
                    need_set_column_id = False

                if create_table_if_not_exist:
                    SQLite3Service.__create_table(
                        columns=columns, table_name=table_name, cur=cur,
                        id_column_name=id_column_name, id_column_type=id_column_type,
                        sqlite3_column_types=sqlite3_column_types)

                # Check that each rows satisfies criteria of the first row.
                [Exception(f"{column} is expected to be in row!") for column in row_columns if column not in columns]

                r = cur.execute(f"SELECT EXISTS(SELECT 1 FROM {table_name} WHERE [{id_column_name}]='{uid}');")
                ans = r.fetchone()[0]
                if ans == 1:
                    continue

                params = ", ".join(tuple(['?'] * (len(columns))))
                row_columns_str = ", ".join([f"[{col}]" for col in row_columns])
                cur.execute(f"INSERT INTO {table_name}({row_columns_str}) VALUES ({params})", row_params_func())
                con.commit()

            cur.close()

    @staticmethod
    def read(src, table="content", **connect_kwargs):
        with sqlite3.connect(src, **connect_kwargs) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table}")
            for row in cursor:
                yield row

    @staticmethod
    def read_columns(target, table="content", **connect_kwargs):
        with sqlite3.connect(target, **connect_kwargs) as conn:
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA table_info({table})")
            return [row[1] for row in cursor.fetchall()]
