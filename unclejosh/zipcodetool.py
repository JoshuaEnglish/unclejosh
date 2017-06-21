# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 10:38:59 2016

@author: jenglish
"""

from collections import Counter
import re

class ZIPCodeTool:
    """Tool for cleaning up US ZIP codes to a five-digit
    code and returning a value from a provided dictionary.
    Must get a dictionary of ZIP Codes from an
    outside source.

    ZIPCodeTool is internally memoized and collects stats
    on how various calls to find_zip_code are handled.

    ZIPCodeTool also tracks requests that ultimatly fail, and
    also requests that do not appear in the source dictionary
    """
    memo = {}
    stats = Counter()
    failures = set()
    u_failures = set()
    missing_zips = set()

    state_zip = re.compile(r'[a-zA-Z]{2}\s(\d{5})')

    def __init__(self, dictionary=None):
        self.zipdict = dictionary if dictionary else {}

    def load_zip_codes(self, dictionary):
        """load_zip_codes(dict)
        The dict keys should be float representations of ZIP codes, the values
        can be anything that needs to be returned.
        """
        self.zipdict = dictionary

    def find_zip_code(self, thing):
        """Returns the value from the given zip code dictionary, or None,
        for a given key. Key could be a number or a string.
        """

        memo = self.memo
        zipdict = self.zipdict
        stats = self.stats

        self.stats['C'] += 1

        if thing in memo:
            stats['M'] += 1
            return self.memo[thing]

        if thing in zipdict:
            stats['Z'] += 1
            return self.zipdict[thing]

        if isinstance(thing, str):
            if thing.endswith('U'):
                try:
                    key = float(thing[:5])
                except ValueError:
                    stats['U failure'] += 1
                    self.u_failures.add(thing)
                    return None
                if key in zipdict:
                    memo[thing] = zipdict[key]
                    stats['U'] += 1
                    return memo.setdefault(thing, zipdict[key])
                else:
                    self.missing_zips.add(key)
                    return None
            if '-' in thing:
                try:
                    key = float(thing[:thing.find('-')])
                except ValueError:
                    stats['hyphen key failure'] += 1
                    print("Hyphen key error:", thing)
                    return None
                if key in zipdict:
                    #memo[thing] = zipdict[key]
                    stats['H'] += 1
                    return memo.setdefault(thing, zipdict[key])
                else:
                    self.missing_zips.add(key)
                    return None
            match = self.state_zip.match(thing)
            if match and match.groups():
                key = float(match.groups()[0])
                if key in zipdict:
                    stats['R'] += 1
                    return memo.setdefault(thing, zipdict[key])
                else:
                    self.missing_zips.add(key)
                    return None

        if isinstance(thing, float):
            key = thing // 10000
            nkey = thing // 1000
            if key in zipdict:
                stats['D'] += 1
                return memo.setdefault(thing, zipdict[key])
            elif nkey in zipdict:
                stats['D'] += 1
                return memo.setdefault(thing, zipdict[nkey])
            else:
                self.missing_zips.add(key)
                return None

        stats['N'] += 1
        self.failures.add(thing)
