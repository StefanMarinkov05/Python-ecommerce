import os
from tabulate import tabulate


def main():
    print_stylized_table()


def print_stylized_table(table=[], headers=[]):
    """
    Print a table in a stylized format using the tabulate library.

    :param table: The table data as a list of lists.
    :type table: list of list
    :param headers: The table headers as a list of strings.
    :type headers: list of str
    :return: None
    :rtype: None
    """
    os.system("cls" if os.name == "nt" else "clear")

    print(
        tabulate(table, headers, tablefmt="grid", stralign="center", numalign="center")
    )


if __name__ == "__main__":
    main()
