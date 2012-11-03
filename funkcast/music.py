# -*- coding: utf-8 -*-
#
# Copyright (c) 2012 Björn Edström <be@bjrn.se>
# See license for details.

import funkcast.MidiFile as MidiFile
import funkcast.nature as nature


def convert(report, idx, data_point, note_descr, absolute=True, invert=False):
    # to normalize we need the complete report
    weather = report[idx]
    value = float(weather[data_point])
    raw = [entry[data_point] for entry in report]

    norm = nature.normalize(data_point, raw, value, absolute)

    if invert:
        norm = 1.0 - norm

    # TODO: Below is MIDI specific and not suited for Lilypond.
    if note_descr == 'pitch':
        return int(40 + 12 * norm)
    if note_descr == 'volume':
        return int(50 + 50 * norm) # XXX: log
    if note_descr == 'time':
        return 0.5 + norm / 2
    if note_descr == 'duration':
        return 0.5 + norm / 2
    return norm


def generate(weather_data, rules, output_format, output, options):

    # generate music
    def _convert(i, note):
        point, absolute, invert = rules[note]
        return convert(weather_data, i, point, note,
                       absolute=absolute, invert=invert)

    # by default, just createa a midi directly
    if output_format == 'midi':
        midi = MidiFile.MIDIFile(1)
        midi.addTrackName(0, 0, 'Weather Track')
        midi.addTempo(0, 0, options.tempo)
        # midi.addProgramChange(0, 10, 0, 35)

        time = 0

        for idx in range(len(weather_data)):
            pitch = _convert(idx, 'pitch')
            duration = _convert(idx, 'duration')
            volume = _convert(idx, 'volume')

            midi.addNote(0, 0, pitch, time, duration, volume)

            time += _convert(idx, 'time')

        midi.writeFile(output)
    # if --lilypond is given, create a score instead
    else:
        out = output
        print >> out, r"""
\version "2.12.3"
\score {
  \new Staff <<
    \new Voice \relative c' {
      \set midiInstrument = #"flute"
      \voiceOne
      \key c \major
      \time 2/2
"""
        time = 0
        # XXX
        some_scale = 'a4 ais b c cis4 d dis e f4 fis g gis'.split()
        for idx in range(len(weather_data)):
            pitch = _convert(idx, 'pitch')
            note = some_scale[(pitch - 40) % len(some_scale)]
            print >> out, note,
        print >> out, r"""
    }
  >>
  \layout { }
  \midi {
    \context {
      \Staff
      \remove "Staff_performer"
    }
    \context {
      \Voice
      \consists "Staff_performer"
    }
    \context {
      \Score
      tempoWholesPerMinute = #(ly:make-moment 72 2)
    }
  }
}
"""
