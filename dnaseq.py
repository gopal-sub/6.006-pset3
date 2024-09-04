#!/usr/bin/env python2.7
import sys
import unittest
from dnaseqlib import *



### Utility classes ###

# Maps integer keys to a set of arbitrary values.
class Multidict:
    # Initializes a new multi-value dictionary, and adds any key-value
    # 2-tuples in the iterable sequence pairs to the data structure.
    def __init__(self, pairs=[]):
        self.dict = {}
        for p in pairs:
            self.put(p[0],p[1])
#        raise Exception("Not implemented!")
    # Associates the value v with the key k.
    def put(self, k, v):
        '''Take key and a value as input and inserts it in the dictionary if already exists then chains it'''
        if k not in self.dict:
            val = []
            val.append(v)
            self.dict[k] = val
        else:
            self.dict[k].append(v)

    # Gets any values that have been associated with the key k; or, if
    # none have been, returns an empty sequence.
    def get(self, k):
        '''finds if key k is in dictionary if yes returns values associated with k else returns empty list'''
        if k not in self.dict:
            return []
        return self.dict[k]
#        raise Exception("Not implemented!")
# Given a sequence of nucleotides, return all k-length subsequences
# and their hashes.  (What else do you need to know about each
# subsequence?)
def subsequenceHashes(seq, k):
    '''Given a sequence of nucleotides, return all k-length subsequences
     and their hashes'''


    subseq = ''
    position = 0
    first_elem = True
    for s in seq:
        subseq += s
        if len(subseq) == k:
            if first_elem == True:
                r_hash = RollingHash(subseq)
                first_elem = False
            else:
                new = s
                r_hash.slide(old, new)
            yield (subseq, r_hash.current_hash(), position)
            old = subseq[0]
            subseq = subseq[1:]
            position += 1

# Similar to subsequenceHashes(), but returns one k-length subsequence
# every m nucleotides.  (This will be useful when you try to use two
# whole data files.)
def intervalSubsequenceHashes(seq, k, m):
    subseq = ''
    position = -1
    marker = -1
    for s in seq:
        marker += 1
        position += 1
        if k > marker:
            if len(subseq) < k:
                subseq += s
            elif len(subseq) == k:
                r_hash = RollingHash(subseq)
                yield (subseq, r_hash.current_hash(), position)
                subseq = ''
        if marker >= m - 1:
            marker = 0




# Searches for commonalities between sequences a and b by comparing
# subsequences of length k.  The sequences a and b should be iterators
# that return nucleotides.  The table is built by computing one hash
# every m nucleotides (for m >= k).
def getExactSubmatches(a, b, k, m):
    hashmap = Multidict()
    for subseq_a in intervalSubsequenceHashes(a, k, m):
        #    for subseq_a in subsequenceHashes(a,k):
        a_sequence = subseq_a[0]
        a_r_hash = subseq_a[1]
        a_position = subseq_a[2]
        #        hashmap.put(a_sequence, a_position)
        hashmap.put(a_r_hash, (a_position, a_sequence))
    for subseq_b in subsequenceHashes(b, k):
        b_sequence = subseq_b[0]
        b_r_hash = subseq_b[1]
        b_position = subseq_b[2]
        #        matches = hashmap.get(b_sequence)
        matches = hashmap.get(b_r_hash)
        for m in matches:
            m_position = m[0]
            m_sequence = m[1]
            if b_sequence == m_sequence:
                yield (m_position, b_position)








if __name__ == '__main__':
    if len(sys.argv) != 4:
        print(sys.argv)
        print('Usage: {0} [file_a.fa] [file_b.fa] [output.png]'.format(sys.argv[0]))
        sys.exit(1)

    # The arguments are, in order: 1) Your getExactSubmatches
    # function, 2) the filename to which the image should be written,
    # 3) a tuple giving the width and height of the image, 4) the
    # filename of sequence A, 5) the filename of sequence B, 6) k, the
    # subsequence size, and 7) m, the sampling interval for sequence
    # A.

    compareSequences(getExactSubmatches, sys.argv[3], (500,500), sys.argv[1], sys.argv[2], 8, 100)
