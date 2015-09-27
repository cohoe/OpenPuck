TODO
====

## Bugs
* CBSInteractive - BU/Providence had a postponed game that BU reports (PRO doesnt).
* CBSInteractive doesnt seem to be reporting past conference games. Different attribute?

## Organization

## Data Integrity
* Going to need a validator at some point for things like seasonphase dates
* Sanity check for number of total games, number of conference games, etc.

## Features
* If provider provides tournament info, get that
* Test connection circuit breaker

### Fields
* Teams need a timezone offset field

## UI
### Matching Games
* For matching games, pick A, B, Manual to trust per field
* Add suggestion logic based on application data and rules
