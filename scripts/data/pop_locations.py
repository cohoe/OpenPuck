#!/usr/bin/env python

from hawkeyapi.database import Locations, LocationAltnames

Locations.put_item(data={
    'id': 'WALTER BROWN ARENA',
    'cn': 'Walter Brown Arena',
    'street': '285 BABCOCK ST',
    'city': 'BOSTON',
    'state': 'MA',
    'postal': '02215',
    'country': 'USA',
}, overwrite=True)

Locations.put_item(data={
    'id': 'ALFOND',
    'cn': 'Alfond Arena',
    'street': 'TUNK RD',
    'city': 'ORONO',
    'state': 'ME',
    'postal': '04473',
    'country': 'USA',
}, overwrite=True)

Locations.put_item(data={
    'id': 'SCHNEIDER',
    'cn': 'Schneider Arena',
    'street': '292 HUXLEY AVE',
    'city': 'PROVIDENCE',
    'state': 'RI',
    'postal': '02908',
    'country': 'USA',
}, overwrite=True)
LocationAltnames.put_item(data={
    'location_id': 'SCHNEIDER',
    'affiliation': 'NCAA-Providence-W',
    'altname': 'PROVIDENCE RI',
},
overwrite=True)

Locations.put_item(data={
    'id': 'CONTE',
    'cn': 'Conte Forum',
}, overwrite=True)
LocationAltnames.put_item(data={
    'location_id': 'CONTE',
    'affiliation': 'NCAA-BC-W',
    'altname': 'CONTE FORUM CHESTNUT HILL MASS',
},
overwrite=True)

Locations.put_item(data={
    'id': 'MATTHEWS',
    'cn': 'Matthews Arena',
}, overwrite=True)

Locations.put_item(data={
    'id': 'FREITAS',
    'cn': 'Freitas Ice Forum',
}, overwrite=True)
LocationAltnames.put_item(data={
    'location_id': 'FREITAS',
    'affiliation': 'NCAA-UConn-W',
    'altname': 'STORRS CONN',
},
overwrite=True)

Locations.put_item(data={
    'id': 'LUMBER',
    'cn': '84 Lumber Arena',
}, overwrite=True)
LocationAltnames.put_item(data={
    'location_id': 'LUMBER',
    'affiliation': 'NCAA-RMU-W',
    'altname': 'MOON TOWNSHIP PA',
},
overwrite=True)

Locations.put_item(data={
    'id': 'TENNITY',
    'cn': 'Tennity Ice Pavillion',
}, overwrite=True)
LocationAltnames.put_item(data={
    'location_id': 'TENNITY',
    'affiliation': 'NCAA-Syracuse-W',
    'altname': 'SYRACUSE NY',
},
overwrite=True)

Locations.put_item(data={
    'id': 'POLISSENI',
    'cn': 'Gene Polisseni Center',
}, overwrite=True)
LocationAltnames.put_item(data={
    'location_id': 'POLISSENI',
    'affiliation': 'NCAA-RIT-W',
    'altname': 'ROCHESTER NY',
},
overwrite=True)

Locations.put_item(data={
    'id': 'HURST',
    'cn': 'Mercyhurst Ice Center',
}, overwrite=True)
LocationAltnames.put_item(data={
    'location_id': 'HURST',
    'affiliation': 'NCAA-Mercyhurst-W',
    'altname': 'ERIE PA',
},
overwrite=True)

Locations.put_item(data={
    'id': 'WHITT',
    'cn': 'Whittemore Center',
}, overwrite=True)
LocationAltnames.put_item(data={
    'location_id': 'WHITT',
    'affiliation': 'NCAA-New Hampshire-W',
    'altname': 'DURHAM NH',
},
overwrite=True)

Locations.put_item(data={
    'id': 'GUTT',
    'cn': 'Gutterson Field House',
}, overwrite=True)
LocationAltnames.put_item(data={
    'location_id': 'GUTT',
    'affiliation': 'NCAA-Vermont-W',
    'altname': 'BURLINGTON VT',
},
overwrite=True)

Locations.put_item(data={
    'id': 'BRIGHT',
    'cn': 'Bright-Landry Hockey Center',
}, overwrite=True)
LocationAltnames.put_item(data={
    'location_id': 'BRIGHT',
    'affiliation': 'NCAA-Harvard-W',
    'altname': 'CAMBRIDGE MASS',
},
overwrite=True)

Locations.put_item(data={
    'id': 'HYANNIS',
    'cn': 'Hyannis Youth and Community Center',
}, overwrite=True)
LocationAltnames.put_item(data={
    'location_id': 'HYANNIS',
    'altname': 'HYANNIS YOUTH AND COMMUNITY CENTER HYANNIS MASS',
},
overwrite=True)
LocationAltnames.put_item(data={
    'location_id': 'HYANNIS',
    'altname': 'HYANNIS MASS',
},
overwrite=True)
