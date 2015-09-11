#!/usr/bin/env python
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, BooleanAttribute, UTCDateTimeAttribute, JSONAttribute

class HawkeyModel(Model):
    """
    Base class for models
    """
