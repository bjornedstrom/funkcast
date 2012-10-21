# funkcast
October 21, 2012

`funkcast` is a small program that generates a MIDI file or Lilypond
score from a weather forecast.

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
and `{weather data}` is described below. Adding a minus sign inverts
the value. Adding an asterisk marks the value as absolute as described
below.

## Weather data

`{weather data}` is one of the following:

* `wind-speed` - This is a fun one. It is an obvious "strength" or "tempo" variable (intuitively music during a storm will sound differently than a sunny day with no winds).
* `wind-direction` - Consider using the wind-direction for music volume or pitch.
* `temperature` - Consider using absolute values for temperature (see below).
* `pressure` - Atmospheric pressure.
* `rain` - Precipitation.
* `cloud-cover` - Low resolution cloud cover (clear, fair, partial, cloudy).

## Absolute vs. Relative value

By marking `{weather data}` with an asterisk in the end makes the
value absolute. This is a very important feature!

By default, a weather data point (such as wind speed) will be
normalized to the other data points in the report. However, this is
something you may not want.

Consider using temperature for pitch. In this case you probably want
the absolute temperature, otherwise you will get the same pitch from a
warm location (the desert) as a cold location (northern Sweden).

Of course, using absolute values has some drawbacks as well, since
`funkcast` has to do something reasonable both for extreme conditions
(a full blown storm for example) as well as mild conditions (no
winds).

## Lilypond

By default the program will generate a MIDI file directly. There is
currently some highly limited support for creating a lilypond score
(an "ly" file).

    $ funkcast --lilypond ... # by default: output.ly
    $ lilypond output.ly
    $ evince output.pdf

![Lilypond output](https://raw.github.com/bjornedstrom/funkcast/master/doc/lilypond.png)

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
