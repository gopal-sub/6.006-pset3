class RollingHash:
    def __init__(self, s):
        self.HASH_BASE = 7
        self.seqlen = len(s)
        n = self.seqlen - 1
        h = 0
        for c in s:
            h += ord(c) * (self.HASH_BASE ** n)
            n -= 1
        self.curhash = h

    # Returns the current hash value.
    def current_hash(self):
        return self.curhash

    # Updates the hash by removing previtm and adding nextitm.  Returns the updated
    # hash value.
    def slide(self, previtm, nextitm):
        self.curhash = (self.curhash * self.HASH_BASE) + ord(nextitm)
        self.curhash -= ord(previtm) * (self.HASH_BASE ** self.seqlen)
        return self.curhash


def intervalSubsequenceHashes(seq, k, m):
    if len(seq) == 0:
        raise Exception("The sequence is length 0")
    if k <= 0 or k > len(seq):
        raise ValueError("Invalid value of k")
    if m <= 0 or m > len(seq):
        raise ValueError("invalid value of m")

    for pointer in range(0, len(seq) - k + 1, m):
        sequence = seq[pointer:pointer + k]
        if pointer == 0:
            rolling_hash = RollingHash(sequence)
        else:
            rolling_hash.slide(seq[pointer - 1], seq[pointer + k - 1])
        hash_val = rolling_hash.current_hash()
        send_back = (sequence, hash_val)
        yield send_back


my_obj = intervalSubsequenceHashes("abcde",2,2)
for i in my_obj:
    print(i[1])


