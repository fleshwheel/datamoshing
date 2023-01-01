#!/usr/bin/env python3

import os
import click
import shutil
import random
import tempfile
import subprocess
from tqdm import tqdm
from os import path

generate_random_block = os.urandom

def generate_temp_jpg(source_filename):
    dest_filename = path.join(tempfile.mktemp() + ".jpg")
    shutil.copyfile(source_filename, dest_filename)
    return dest_filename

def corrupt_section(filename, block_size = 1, swap = False):
    """
    corruptes a section of the input file, and returns
    the filename to a temporary file which has been corrupted.
    """
    
    output_filename = generate_temp_jpg(filename)
    file_size = path.getsize(filename)
    with open(output_filename, "r+b") as f:
        block1_idx = random.randint(0, file_size - block_size)
        f.seek(block1_idx)
        if swap:
            block2_idx = random.randint(0, file_size - block_size)
            block1 = f.read(block_size)
            f.seek(block2_idx)
            block2 = f.read(block_size)
            f.seek(block1_idx)
            f.write(block2)
            f.seek(block2_idx)
            f.write(block1)
        else:
            f.write(generate_random_block(block_size))
    return output_filename

def is_valid(input_filename):
    try:
        subprocess.check_output(["jpeginfo", "-c", input_filename])
        return True
    except subprocess.CalledProcessError:
        return False

def corrupt_iteration(input_filename, block_size, swap):
    """
    perform a single corrupt iteration.
    """

    corrupted_filename = corrupt_section(input_filename, block_size, swap)
    if is_valid(corrupted_filename):
        os.remove(input_filename)
        return corrupted_filename
    else:
        return input_filename

@click.command()
@click.option("-f", "--filename", required = True, help = "input file to corrupt.")
@click.option("-i", "--iterations", default = 1, help = "number of corrupt iterations to perform.")
@click.option("-b", "--block_size", default = 1, help = "number of bytes to corrupt at a time.")
@click.option("-s", "--swap", is_flag = True, help = "corrupt file by swapping bytes instead of adding random ones.")
def corrupt_jpg(filename, iterations, block_size, swap):
    current_filename = generate_temp_jpg(filename)
    for i in tqdm(range(iterations)):
        current_filename = corrupt_iteration(current_filename, block_size, swap)
    shutil.copy(current_filename, os.getcwd())

if __name__ == '__main__':
    corrupt_jpg()
