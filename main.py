from tables import *
import cli


def main():
    connection = connect_to_db()
    if connection is None:
        return

    create_tables(connection)
    cli.run()
    connection.close()


if __name__ == "__main__":
    main()
