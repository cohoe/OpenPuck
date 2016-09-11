#!/usr/bin/env python

import json
import re
from datetime import datetime, time, date


class HawkeyApiObject(object):
    def __init__(self):
        pass

    def json(self, pretty=True):
        """
        Print out a JSON representation of this object.
        """
        name = self.__class__.__name__
        o_dict = {}
        for k in self.__dict__:
            # This is some StackOverflow magic...
            # nk = re.sub(r'(?!^)_([a-zA-Z])', lambda m: m.group(1).upper(), k)
            nk = k
            if isinstance(self.__dict__[k], datetime):
                o_dict[nk] = self.__dict__[k].isoformat()
            elif isinstance(self.__dict__[k], date):
                o_dict[nk] = self.__dict__[k].isoformat()
            elif isinstance(self.__dict__[k], time):
                o_dict[nk] = self.__dict__[k].isoformat()
            else:
                o_dict[nk] = self.__dict__[k]

        if pretty is True:
            return json.dumps({name: o_dict}, sort_keys=True, indent=4,
                              separators=(',', ': '))

        return json.dumps([name, o_dict])

