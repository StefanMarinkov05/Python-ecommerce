import urllib.request


def main():
    get_ipv4()


def get_ipv4():
    return urllib.request.urlopen("https://ident.me").read().decode("utf8")


if __name__ == "__main__":
    main()
