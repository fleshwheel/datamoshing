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

def generate_temp_mp4(source_filename):
    dest_filename = path.join(tempfile.mktemp() + ".mp4")
    shutil.copyfile(source_filename, dest_filename)
    return dest_filename

def corrupt_section(filename, block_size = 1):
    """
    corruptes a section of the input file, and returns
    the filename to a temporary file which has been corrupted.
    """
    
    output_filename = generate_temp_mp4(filename)
    file_size = path.getsize(filename)
    with open(output_filename, "r+b") as f:
        f.seek(random.randint(0, file_size - block_size))
        f.write(generate_random_block(block_size))
    return output_filename

def attempt_transcode(input_filename):
    output_filename = generate_temp_mp4(input_filename)
    try:
        subprocess.check_output(["ffmpeg", "-i", input_filename,
                                 "-c", "copy", output_filename],
                                stderr = subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        # exception is thrown if anything appears on stderr,
        # so the transcode did not necessarily fail.
        pass

def is_valid(input_filename, try_fix = True):
    """
    given a path to an mp4 video, checks whether ffmpeg
    reports any decoding errors. if it does, see if it can
    be fixed by re-encoding. returns boolean value corresponding
    to whether or not the file is irreperably corrupted.
    """

    try:
        subprocess.check_output(["ffmpeg", "-v", "error",
                                 "-i", input_filename,
                                 "-f", "null", "-"],
                                stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        if try_fix:
            fixed_filename = attempt_transcode(input_filename)
            os.remove(input_filename)
            return validate(fixed_filename)
        else:
            return False

def corrupt_iteration(input_filename, block_size = 1):
    """
    perform a single corrupt iteration.
    """

    corrupted_filename = corrupt_section(input_filename)
    if is_valid(corrupted_filename):
        os.remove(input_filename)
        return corrupted_filename
    else:
        return input_filename

@click.command()
@click.option("-f", "--filename", required = True, help = "input file to corrupt.")
@click.option("-i", "--iterations", default = 1, help = "Number of corrupt iterations to perform.")
@click.option("-b", "--block_size", default = 1, help = "number of bytes to corrupt at a time.")
def corrupt_mp4(filename, iterations, block_size):
    current_filename = generate_temp_mp4(filename)
    for i in tqdm(range(iterations)):
        current_filename = corrupt_iteration(current_filename, block_size)
    shutil.copy(current_filename, os.getcwd())

if __name__ == '__main__':
    corrupt_mp4()
