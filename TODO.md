TODO
====

## Bugs
* Add lxml to all BeautifulSoup calls
* Certain BC women games vs Providence arent getting tracked as home games (SidearmAdaptive)

## Organization
* Move util to providers.util and start modularizing

## Data Integrity
* Going to need a validator at some point for things like seasonphase dates
* Sanity check for number of total games, number of conference games, etc.
* Stop rewriting location and opponent information. Keep it raw until game building.

## Features
* If provider provides tournament info, get that
* Test connection circuit breaker
* Team lookup helper
* Team home arenas and location altnames
* onetimer to copy all altnames from mens to womens teams

### Fields
* Teams need a timezone offset field
* Games need modification date
* sentries need acquisition date

## UI
### Matching Games
* For matching games, pick A, B, Manual to trust per field
* Add suggestion logic based on application data and rules

## Future Data
* Rosters
* Schedule publish date
* Box-score posting to notifications
* Subscribe to updates and live notifications of things
