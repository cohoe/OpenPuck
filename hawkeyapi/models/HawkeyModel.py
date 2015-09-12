#!/usr/bin/env python
from pynamodb.models import Model
from pynamodb.indexes import GlobalSecondaryIndex, LocalSecondaryIndex, AllProjection
from pynamodb.attributes import UnicodeAttribute, BooleanAttribute, UTCDateTimeAttribute, JSONAttribute, UnicodeSetAttribute

class HawkeyModel(Model):
    """
    Base class for models
    """
