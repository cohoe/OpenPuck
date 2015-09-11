#!/usr/bin/env python
from pynamodb.models import Model
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
from pynamodb.attributes import UnicodeAttribute, BooleanAttribute, UTCDateTimeAttribute, JSONAttribute

class HawkeyModel(Model):
    """
    Base class for models
    """
