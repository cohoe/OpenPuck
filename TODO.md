TODO
====

## Bugs
* Dates in Streamline are totally wrong (years)
* normalize_opponent is getting a little too normal (streamline)

## Organization
* Remove schedule year detection since we have objects now

## Data Integrity
* Fix all 12:00AM game references to either be None or something

## Features
* Finish all providers to use new team objects and not be season-dependent

### Fields
* Add is_tournament flag to all providers
* Add game status (scheduled, inprogress, final)
