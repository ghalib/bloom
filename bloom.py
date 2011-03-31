# Bloom filter example by Ghalib Suleiman <ghalib@sent.com>

# See http://www.internetmathematics.org/volumes/1/4/Broder.pdf for nice overview.


# Let n = number of keys our filter will accept = 5000
# Let epsilon = our accepted rate of false positives = 1% = 0.01

# Let m = size of our filter in bits = ceiling(n * log_2(e) *
# log_2(1/epsilon)) = 47926

# Let k = number of hash functions = ceiling(lg(2) * (m/n)) = 7 (we
# chop up a chunk of a SHA-1 hash into 7 segments)

"""
Bloom filter example.

Usage:

>>> MyFilter = bloom.Filter()
>>> MyFilter.add('hello')
'hello'
>>> 'hello' in MyFilter
True
>>> 'goodbye' in MyFilter
False
>>> MyFilter.add([1,2,3])
[1,2,3]
"""

import sha

class Filter:
    def __init__(self):
        # I suppose all these values can be parametrised...
        self.maxkeys = 5000
        self.m = 47926
        self.k = 7
        self.bitset = ((2 ** (self.m - 1)) ^ (2 ** (self.m - 1)))
        self.size = 0

    def _calc_digest(self, item):
        # Why do we slice up to 28?  Well, recall that m = 47926, and
        # so that is the number of indices we need.  Number of bits
        # needed for binary representation of m = floor(log_2(m)) + 1
        # = 16, which is 2 bytes.  In other words, we need each hash
        # function to produce 2 bytes of output.  Since we have 7 hash
        # functions, that is a total of 14 bytes.  Every two
        # characters in the output of hexdigest() constitute one byte,
        # so 2 * 14 = 28 chars in total.
        return sha.sha(repr(item)).hexdigest()[:28]

    def _is_set(self, bit_index):
        """Check if bit at BIT_INDEX is set to 1"""
 	return ((self.bitset & (1 << bit_index)) != 0)
    
    def _hashes(self, digest_string):
        """Generate our 7 hashes.  DIGEST_STRING is the string
        returned by .hexdigest()"""

        # We want 2 bytes at a time, i.e. 4 characters, for a total of
        # 7 times.  Recall that DIGEST_STRING is 28 characters.
        segments = (digest_string[i:i+4] for i in xrange(0, 25, 4))
        return ((int(x, 16) % 47926) for x in segments)

    def add(self, item):
        if (self.size == self.maxkeys):
            raise Exception("Filter is full -- size = 5000")
        else:
            digest = self._calc_digest(item)
            for index in self._hashes(digest):
                self.bitset |= 2**index
            self.size += 1
        return item
    
    def __contains__(self, item):
        present = True
        for index in self._hashes(self._calc_digest(item)):
            present = present and self._is_set(index)
        return present



