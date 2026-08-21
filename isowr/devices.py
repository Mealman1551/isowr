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

def get_disk(device_path):
    device_name = device_path.removeprefix("/dev/")

    for device in get_disks():
        if device["name"] == device_name:
            return device

    return None
    
def get_safety_reason(device):
    if device["ro"]:
        return "read-only"

    for partition in device.get("children", []):
        for mountpoint in partition.get("mountpoints", []):
            if mountpoint == "/":
                return "system root"
            if mountpoint == "[SWAP]":
                return "swap"

    return None

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
    for device in get_disks():
        print(get_device_path(device), get_safety_reason(device))