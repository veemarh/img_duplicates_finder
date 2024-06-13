from algorithms.find_duplicates_hash import find_duplicates_use_hash
from algorithms.find_duplicates_orb import find_duplicates_use_orb

# arg 'quick' only for bhash - parameter 'Fast' = True, 'Precise' = False
# arg 'size' oly for bhash - parameter 'Comparison area' (128x128, 256x256, 512x512)
def find_duplicates(input_folder, duplicates_folder, hash_size=16, perc_similarity=100, method='aHash', quick=False, size=16):
    match method:
        case 'ORB':
            find_duplicates_use_orb(input_folder, duplicates_folder, perc_similarity)
        case 'aHash' | 'bHash' | 'dHash' | 'mHash' | 'pHash' | 'MD5' | 'SHA-1 (160-bit)' | 'SHA-2 (256-bit)' | 'SHA-2 (384-bit)' | 'SHA-2 (512-bit)':
            find_duplicates_use_hash(input_folder, duplicates_folder, hash_size, perc_similarity, method, quick, size)
        case _:
            return "Error: method not found"
            
# Example of work
# find_duplicates('images/', 'result/', perc_similarity=70, method='ORB')
# find_duplicates('images/', 'result/', perc_similarity=100, method='aHash')
# find_duplicates('images/', 'result/', perc_similarity=100, method='bHash', quick=False, size=256) # 26s - 8 duplicates
# find_duplicates('images/', 'result/', perc_similarity=100, method='mHash', size=16) # 16s - 8 duplicates
# find_duplicates('images/', 'result/', method='SHA-2 (512-bit)')
