import psycopg2
from config import config


def create_script():
    create_script = """CREATE TABLE IF NOT EXISTS perfect_srcl (
                results int
            )
            """
    return create_script


def table_check():
    drop_table = "DROP TABLE IF EXISTS perfect_srcl"
    return drop_table


def inserting():
    insert_script = "INSERT INTO perfect_srcl( " \
                    "results" \
                    ") VALUES (%s)"
    return insert_script


def connect():
    connection = None
    try:
        params = config()
        print("Connecting to postgreSQL database...")
        connection = psycopg2.connect(**params)

        crsr = connection.cursor()
        print("PostgreSQL database version: ")
        crsr.execute('SELECT version()')
        db_version = crsr.fetchone()
        print(db_version)

        crsr.execute(table_check())

        crsr.execute(create_script())
        # Example
        # insert_value = [
        #     (16000),
        #     (26000),
        #     (63000)]
        # for record in insert_value:
        #     crsr.execute(inserting(), record)

        crsr.execute('SELECT * FROM perfect_srcl')
        print(crsr.fetchall())

        connection.commit()
        crsr.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
            print("Database connection terminated")

