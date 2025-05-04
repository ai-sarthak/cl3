from collections import Counter
from multiprocessing import Pool
import os

def map_char_count(chunk):
    print(chunk)
    print(Counter(chunk))
    return Counter(chunk)

def reduce_counts(counts):
    total = Counter()
    for count in counts:
        total.update(count)
    return total

def read_in_chunks(filename, chunk_size=100):
    with open(filename, 'r', encoding='utf-8') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk

def character_count(filename):
    print(os.cpu_count())
    with Pool(os.cpu_count()) as pool:
        chunks = list(read_in_chunks(filename))
        mapped = pool.map(map_char_count, chunks)
        print("MAPPED::::",mapped)
        result = reduce_counts(mapped)
    return result



def map_word_count(chunk):
    words = chunk.lower().split()
    print(words)
    return Counter(words)

def word_count(filename):
    with Pool(os.cpu_count()) as pool:
        chunks = list(read_in_chunks(filename))
        mapped = pool.map(map_word_count, chunks)
        result = reduce_counts(mapped)
    return result

# Example usage
# 


# Example usage
print(character_count("lorem.txt"))
print(word_count("lorem.txt"))


