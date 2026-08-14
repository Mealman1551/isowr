import argparse
from pathlib import Path


VERSION = "0.1.0"


def info(image):
    path = Path(image)

    if not path.exists():
        print(f"Error: file not found: {path}")
        return 1

    if not path.is_file():
        print(f"Error: not a file: {path}")
        return 1

    size = path.stat().st_size

    print(f"File: {path}")
    print(f"Size: {size} bytes")

    return 0


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

    subparsers = parser.add_subparsers(dest="command")

    info_parser = subparsers.add_parser(
        "info",
        help="Show information about an image"
    )

    info_parser.add_argument(
        "image",
        help="Path to the image"
    )

    args = parser.parse_args()

    if args.command == "info":
        return info(args.image)


if __name__ == "__main__":
    raise SystemExit(main())