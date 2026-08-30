import os
def write_image(image, target, block_size=4 * 1024 * 1024, progress_callback=None):
    total = 0

    with open(image, "rb") as source, open(target, "wb") as destination:
        while chunk := source.read(block_size):
            destination.write(chunk)
            total += len(chunk)

            if progress_callback:
                progress_callback(total)

        destination.flush()
        os.fsync(destination.fileno())

    return total