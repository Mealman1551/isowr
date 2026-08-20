import argparse
from pathlib import Path
from .devices import get_disks, get_device_path, format_size, get_safety_reason

VERSION = "0.1.4"


def is_iso9660(path):
    with path.open("rb") as file:
        file.seek(32769)
        identifier = file.read(5)

    return identifier == b"CD001"

def info(image):
    path = Path(image)

    if is_iso9660(path):
        print("Type: ISO 9660")
    else:
        print("Type: Unknown")

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

    devices_parser = subparsers.add_parser(
    "devices",
    help="List available disk devices"
)

    args = parser.parse_args()

    if args.command == "info":
        return info(args.image)

    if args.command == "devices":
        for device in get_disks():
            path = get_device_path(device)
            size = format_size(device["size"])
            reason = get_safety_reason(device)

            if reason:
                print(f"{path}\t{size}\tUNSAFE: {reason}")
            else:
                print(f"{path}\t{size}\tNo safety issues detected")


if __name__ == "__main__":
    raise SystemExit(main())