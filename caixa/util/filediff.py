from zlib import crc32
from typing import Tuple

def pairwise_crc32(filepath1: str, filepath2: str) -> Tuple[int, int]:
    """
    Given two file paths, we return the CRC32 checksums on each.
    """
    with open(filepath1, "rb") as f1, open(filepath2, "rb") as f2:
        bytes1 = f1.read()
        bytes2 = f2.read()
        check1 = crc32(bytes1)
        check2 = crc32(bytes2)
        return (check1, check2)

def compare_files_crc32(filepath1: str, filepath2: str) -> bool: 
    """
    Returns True if the files under each respective path appear to be identical 
    (in the sense of having equal CRC32 checksums), False otherwise. 
    """
    (check1, check2) = pairwise_crc32(filepath1, filepath2) 
    return check1 == check2

