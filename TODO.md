TODO
====

## Bugs
* normalize_opponent is getting a little too normal (streamline)
* get_datetime_from_string is likely full of bugs...

## Organization
* Remove schedule year detection since we have objects now

## Data Integrity
* Fix all 12:00AM game references to either be None or something

## Features

### Fields
* Add is_tournament flag to all providers
* Add game status (scheduled, inprogress, final)
