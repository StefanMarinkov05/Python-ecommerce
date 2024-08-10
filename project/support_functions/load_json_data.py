import json


def main():
    load_test_data("../test_data.json")


def load_test_data(file_path):
    """
    Loads test data from a JSON file.

    :param file_path: Path to the JSON file containing test data
    :type file_path: str
    :return: Data loaded from the JSON file
    :rtype: dict
    """
    with open(file_path, "r") as file:
        return json.load(file)


if __name__ == "__main__":
    main()
