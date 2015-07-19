TODO
====

## Bugs

## Organization
* Implement notes in all providers
* Reimplement SidearmLegacy to use the table-as-a-dict functionality
* Fix the Neulion provider that passes text and not elements

## Features
### Objects
* Make season object to hold dates and things
* Figure out team object that will handle website and season data
* Make games return objects then shit out json from those
* Make media_urls defined somewhere else first (obj???)

### Fields
* add isConference flag
* isPreSeason is totally busted and isnt going to work without a season object
* Add schedule year field and have it somewhat auto calculate
* Add is_tournament flag to all providers
