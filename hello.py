# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "requests",
# ]
# ///

import requests


def main() -> None:
    print(requests.get("https://ipinfo.io/ip").text)
    print("Hello from hello.py!")


if __name__ == "__main__":
    main()
