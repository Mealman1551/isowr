import argparse
from pathlib import Path
from .devices import get_disks, get_device_path, format_size, get_safety_reason, get_writable_device

VERSION = "0.1.5"


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


def validate_image(image):
    path = Path(image)

    if not path.exists():
        return f"image not found: {image}"

    if not path.is_file():
        return f"not a file: {image}"

    if not is_iso9660(path):
        return f"not a valid ISO 9660 image: {image}"

    return None

def validate_write(device):
    target = get_writable_device(device)

    if target is None:
        return f"device not found: {device}"

    reason = get_safety_reason(target)

    if reason:
        return f"unsafe device: {reason}"

    return None

def write(image, device):

    error = validate_image(image)

    if error:
        print(f"ERROR: {error}")
        print("Write aborted.")
        return 1


    
    print(f"Image:  {image}")
    print(f"Target: {device}")
    print()

    error = validate_write(device)

    if error:
        print(f"ERROR: {error}")
        print("Write aborted.")
        return 1

    print("DRY RUN: no data will be written.")
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

    write_parser = subparsers.add_parser(
    "write",
    help="Write an image to a disk"
    )

    write_parser.add_argument(
    "image",
    help="Path to the image"
    )

    write_parser.add_argument(
    "device",
    help="Target disk device"
    )

    args = parser.parse_args()

    if args.command == "write":
        return write(args.image, args.device)

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