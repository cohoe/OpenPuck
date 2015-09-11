#!/usr/bin/env python

from hawkeyapi.models import TeamModel

if TeamModel.exists():
    TeamModel.delete_table()

TeamModel.create_table()
print "Created Teams table"
