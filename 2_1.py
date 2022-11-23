import argparse
import os
import shutil
import subprocess
import time

MEGABYTE = 1048576

EXPECTED_FREE_SPACE = 512
NEW_FILE_SIZE = 1
NEW_FILE_COUNT = 2
WORK_FOLDER = "/Users/i.zykov/code/temp"


def byte_to_mb(bytes):
    return bytes / MEGABYTE


def mb_to_byte(mb):
    return mb * MEGABYTE


def check_mount(expected_free_space_mb, path, device):
    if not os.path.ismount(path):
        return False

    _, _, free = shutil.disk_usage(path)
    if byte_to_mb(free) < expected_free_space_mb:
        return False

    # example of non-local path: i.zykov@host1@host.ru:/dev/disk
    if device.find(":") != -1:
        return False

    return True


def fill_file(expected_file_size_mb, input, output):
    expected_file_size = mb_to_byte(expected_file_size_mb)
    dd_command = f"dd if={input} of={output} bs={expected_file_size}"
    subprocess.run(dd_command, shell=True)


def getDisks():
    p = subprocess.run(["mount"],
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)

    lines = p.stdout.splitlines()

    disks = []
    for line in lines:
        temp = line.decode("utf-8").split(' ')
        device = temp[0]
        path = temp[2]
        if path != '/':
            disks.append([device, path])

    return disks


def get_disk(expected_free_space):
    disks = getDisks()
    for disk in disks:
        path = disk[1]
        device = disk[0]
        if check_mount(expected_free_space, path, device):
            return path


def create_isos(input_disk):
    for i in range(NEW_FILE_COUNT):
        output_file = os.path.join(WORK_FOLDER, "dd_{}.iso".format(str(i)))
        fill_file(NEW_FILE_SIZE, input_disk, output_file)


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('--free-space', type=int, default=512)
    parser.add_argument('--new-file-size', type=int, default=1)
    parser.add_argument('--new-file-count', type=int, default=2)
    parser.add_argument('--work-folder', type=str, default="/Users/i.zykov/code/temp")

    args = parser.parse_args()
    return args


def main():
    args = parse_arguments()

    input_disk = get_disk(args.free)

    start_time = time.time()
    create_isos(input_disk)
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main()
