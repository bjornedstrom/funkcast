# funkcast
October 21, 2012

`funkcast` is a small program that generates a MIDI file from a
weather forecast.

Note: this is very early software at the moment, YMMV.

# Usage

Dependencies: Python, BeautifulSoup.

At the most basic usage, just run the program with a location name,
such as below, which is used to grab a weather forecast from
http://www.yr.no/ and generate the file `output.mid` using some
default parameters.

    $ funkcast "Switzerland/Bern/Lauterbrunnen"
    $ timidity output.mid # or however you play midi files

The location names are of the form `<country>/<division>/<location>` as
can be seen in URL when browsing YR.no.

Play around with it by specifing rules, such as the following:

    $ funkcast pitch=-wind-speed \
        duration=temperature \
        time=pressure \
        volume=wind-direction* \
        "Switzerland/Bern/Lauterbrunnen"

Rules are of the form:

    {note spec} '=' ['-'] {weather data} ['*']

Where `{note spec}` is one of "pitch", "duration", "time", "volume"
and `{weather data}` is one of "wind-speed", "wind-direction",
"temperature", "pressure". Adding a minus sign inverts the
value. Adding an asterisk marks the value as absolute.

# License and So On

This software uses parts of the MIDIUtil library by Mark Conway Wirt,
see LICENSE.MIDIUtil for details.

Otherwise, this software is written by Björn Edström. See LICENSE for
details.

## Weather Data

The software uses weather data from YR.no: Weather forecast from
yr.no, delivered by the Norwegian Meteorological Institute and the
NRK. Please read more about our conditions and guidelines at
http://om.yr.no/verdata/ English explanation at
http://om.yr.no/verdata/free-weather-data/
