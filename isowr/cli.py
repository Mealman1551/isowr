import argparse


VERSION = "0.1.0"


def main():
    parser = argparse.ArgumentParser(
        prog="isowr",
        description="ISO writing utility"
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"ISOWR v{VERSION}"
    )

    parser.parse_args()


if __name__ == "__main__":
    main()