import hashlib
import os
from tqdm import tqdm
import time

folder = "ENTER FOLDER NAME HERE"


t0 = time.time()
def hash_file(filename):
    """This function returns the SHA-1 hash of the file passed into it"""
    h = hashlib.sha1()
    with open(filename, 'rb') as file:
        chunk = 0
        while chunk != b'':
            chunk = file.read(1024)
            h.update(chunk)
    return h.hexdigest()

def walkdir(folder):
    """Walk through each file in a directory"""
    for dirpath, dirs, files in os.walk(folder):
        for filename in files:
            yield os.path.abspath(os.path.join(dirpath, filename))

def count_string_occurrences(input_list, target_string):
    count = 0
    for item in input_list:
        if item == target_string:
            count += 1
    return count

hash_list = []
file_set = set()  # Keep track of unique files
file_counter = 0

for filepath in walkdir(folder):
    file_counter += 1

for file in tqdm(walkdir(folder), desc="Calculating file hashes", total=file_counter, unit=" files"):
    file_hash = hash_file(file)
    hash_list.append(file_hash)

# Identify duplicate files
duplicates_to_delete = []
for file_hash in tqdm(set(hash_list), desc="Identifying duplicates", total=len(set(hash_list)), unit=" files"):
    count = count_string_occurrences(hash_list, file_hash)
    
    if count > 1:
        duplicates = [file for file, hash_value in zip(walkdir(folder), hash_list) if hash_value == file_hash]
        duplicates_to_delete.extend(duplicates[1:])

# Delete duplicate files
total_doubles = 0
for duplicate_file in duplicates_to_delete:
    os.remove(duplicate_file)
    total_doubles += 1

t1 = time.time()
total_time = t1-t0
print(f"Total duplicates deleted: {total_doubles}")
print(f"Total time: {round(total_time,1)}s")
print(f"Total files processed: {file_counter}")
