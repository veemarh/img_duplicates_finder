from algorithms.find_duplicates_hash import find_duplicates_use_hash
from algorithms.find_duplicates_orb import find_duplicates_use_orb

def find_duplicates(input_folder, duplicates_folder, hash_size = 16, perc_similarity = 100, method = 'aHash'):
    match method:
        case 'ORB':
            find_duplicates_use_orb(input_folder, duplicates_folder, perc_similarity)
        case 'aHash' | 'bHash' | 'dHash' | 'mHash' | 'pHash' | 'MD5' | 'SHA-1' | 'SHA-2':
            find_duplicates_use_hash(input_folder, duplicates_folder, hash_size, perc_similarity, method)
        case _:
            return "Error: method not found"
            
# Example of work
# find_duplicates('images/', 'result/', perc_similarity=70, method='ORB')
# find_duplicates('images/', 'result/', perc_similarity=100, method='pHash')
