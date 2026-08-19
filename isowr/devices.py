import json
import subprocess


def get_devices():
    result = subprocess.run(
        ["lsblk", "--bytes", "--json"],
        capture_output=True,
        text=True,
        check=True
    )

    data = json.loads(result.stdout)

    return data["blockdevices"]

def get_disks():
    devices = get_devices()

    return [
        device
        for device in devices
        if device["type"] == "disk"
    ]

def get_device_path(device):
    return f"/dev/{device['name']}"

def format_size(size):
    units = ["B", "KB", "MB", "GB", "TB"]

    for unit in units:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024

    return f"{size:.1f} PB"

if __name__ == "__main__":
    print(get_disks())