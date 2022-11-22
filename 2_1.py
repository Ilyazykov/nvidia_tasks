import shutil
import subprocess
import os
import time

MEGABYTE = 1048576

EXPECTED_FREE_SPACE = 512
NEW_FILE_SIZE = 1
NEW_FILE_COUNT = 2
WORKFOLDER = "/Users/i.zykov/code/temp"


def byteToMb(bytes):
    return bytes / MEGABYTE

def mbToByte(mb):
    return mb * MEGABYTE


def checkMount(expectedFreeSpaceMb, path, device):
    if not os.path.ismount(path):
        return False
    
    _, _, free = shutil.disk_usage(path)
    if byteToMb(free) < expectedFreeSpaceMb:
        return False
    
    # example of non-local path: i.zykov@host1@host.ru:/dev/disk
    if device.find(":") != -1:
        return False
    
    return True


def fillFile(expectedFileSizeMb, input, output):
    expectedFileSize = mbToByte(expectedFileSizeMb)
    dd_command = f"dd if={input} of={output} bs={expectedFileSize}"
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
        if (path != '/'):
            disks.append([device, path])

    return disks


def getDisk(expectedFreeSpace):
    disks = getDisks()
    for disk in disks:
        path = disk[1]
        device = disk[0]
        if checkMount(expectedFreeSpace, path, device):
            return path


def main():
    input = getDisk(EXPECTED_FREE_SPACE)

    start_time = time.time()

    for i in range(NEW_FILE_COUNT):
        output_file = os.path.join(WORKFOLDER, "dd_{}.iso".format(str(i)))
        fillFile(NEW_FILE_SIZE, input, output_file)
    
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main()