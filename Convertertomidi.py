
# known issues: 
# change program is not  working in gamehero midi - make sure to enable MoreStrictProgChange = true
# event set to instrument automatic in drums without control affecting game hero midi player system of roblox. 
# it is possible that there may be bugs

# Misc
# when read hex 61 does not set note off and will cause to longer notes when importing on onlinesequencer. use midieditor to save.
# Limit the range of the notes musical and drums 00 to 5f
# Drums map not verified. may imperfectly
# will cause to play hex 62 should not play notes.
# if read hex 00 20 40 will cause to play notes which should ignore.

# Partially implemented
# 70 hex automatic instrument  and Volume 
# 73 hex automatic set volume only
# Not implemented
# 64 and 65 feature Not supported since required load hex read .hex
# 66 hex change octave of max of  4 channel of wlzb, in gluck2 max of 6 channel track
# Need switch True Or False to ignore
# 63 - loop
# 62 - no loop instant stop 


import mido
from mido import MidiFile, MidiTrack, Message, MetaMessage, bpm2tempo

# === Custom MIDI Instrument Mapping ===
MIDI_INSTRUMENT_MAP = {
    # Standard GM 1-128 (with hex 00-7F and 80-FF both mapping to 0-127)
    0x00: 0,    # Acoustic Grand Piano
    0x01: 1,    # Bright Acoustic Piano
    0x02: 2,    # Electric Grand Piano
    0x03: 3,    # Honky-tonk Piano
    0x04: 4,    # Electric Piano 1
    0x05: 5,    # Electric Piano 2
    0x06: 6,    # Harpsichord
    0x07: 7,    # Clavinet
    0x08: 8,    # Celesta
    0x09: 9,    # Glockenspiel
    0x0A: 10,   # Music Box
    0x0B: 11,   # Vibraphone
    0x0C: 12,   # Marimba
    0x0D: 13,   # Xylophone
    0x0E: 14,   # Tubular Bells
    0x0F: 15,   # Dulcimer
    0x10: 16,   # Drawbar Organ
    0x11: 17,   # Percussive Organ
    0x12: 18,   # Rock Organ
    0x13: 19,   # Church Organ
    0x14: 20,   # Reed Organ
    0x15: 21,   # Accordion
    0x16: 22,   # Harmonica
    0x17: 23,   # Tango Accordion
    0x18: 24,   # Acoustic Guitar (nylon)
    0x19: 25,   # Acoustic Guitar (steel)
    0x1A: 26,   # Electric Guitar (jazz)
    0x1B: 27,   # Electric Guitar (clean)
    0x1C: 28,   # Electric Guitar (muted)
    0x1D: 29,   # Overdriven Guitar
    0x1E: 30,   # Distortion Guitar
    0x1F: 31,   # Guitar Harmonics
    0x20: 32,   # Acoustic Bass
    0x21: 33,   # Electric Bass (finger)
    0x22: 34,   # Electric Bass (pick)
    0x23: 35,   # Fretless Bass
    0x24: 36,   # Slap Bass 1
    0x25: 37,   # Slap Bass 2
    0x26: 38,   # Synth Bass 1
    0x27: 39,   # Synth Bass 2
    0x28: 40,   # Violin
    0x29: 41,   # Viola
    0x2A: 42,   # Cello
    0x2B: 43,   # Contrabass
    0x2C: 44,   # Tremolo Strings
    0x2D: 45,   # Pizzicato Strings
    0x2E: 46,   # Orchestral Harp
    0x2F: 47,   # Timpani
    0x30: 48,   # String Ensemble 1
    0x31: 49,   # String Ensemble 2
    0x32: 50,   # Synth Strings 1
    0x33: 51,   # Synth Strings 2
    0x34: 52,   # Choir Aahs
    0x35: 53,   # Voice Oohs
    0x36: 54,   # Synth Voice
    0x37: 55,   # Orchestra Hit
    0x38: 56,   # Trumpet
    0x39: 57,   # Trombone
    0x3A: 58,   # Tuba
    0x3B: 59,   # Muted Trumpet
    0x3C: 60,   # French Horn
    0x3D: 61,   # Brass Section
    0x3E: 62,   # Synth Brass 1
    0x3F: 63,   # Synth Brass 2
    0x40: 64,   # Soprano Sax
    0x41: 65,   # Alto Sax
    0x42: 66,   # Tenor Sax
    0x43: 67,   # Baritone Sax
    0x44: 68,   # Oboe
    0x45: 69,   # English Horn
    0x46: 70,   # Bassoon
    0x47: 71,   # Clarinet
    0x48: 72,   # Piccolo
    0x49: 73,   # Flute
    0x4A: 74,   # Recorder
    0x4B: 75,   # Pan Flute
    0x4C: 76,   # Blown Bottle
    0x4D: 77,   # Shakuhachi
    0x4E: 78,   # Whistle
    0x4F: 79,   # Ocarina
    0x50: 80,   # Lead 1 (square)
    0x51: 81,   # Lead 2 (sawtooth)
    0x52: 82,   # Lead 3 (calliope)
    0x53: 83,   # Lead 4 (chiff)
    0x54: 84,   # Lead 5 (charang)
    0x55: 85,   # Lead 6 (voice)
    0x56: 86,   # Lead 7 (fifths)
    0x57: 87,   # Lead 8 (bass + lead)
    0x58: 88,   # Pad 1 (new age)
    0x59: 89,   # Pad 2 (warm)
    0x5A: 90,   # Pad 3 (polysynth)
    0x5B: 91,   # Pad 4 (choir)
    0x5C: 92,   # Pad 5 (bowed)
    0x5D: 93,   # Pad 6 (metallic)
    0x5E: 94,   # Pad 7 (halo)
    0x5F: 95,   # Pad 8 (sweep)
    0x60: 96,   # FX 1 (rain)
    0x61: 97,   # FX 2 (soundtrack)
    0x62: 98,   # FX 3 (crystal)
    0x63: 99,   # FX 4 (atmosphere)
    0x64: 100,  # FX 5 (brightness)
    0x65: 101,  # FX 6 (goblins)
    0x66: 102,  # FX 7 (echoes)
    0x67: 103,  # FX 8 (sci-fi)
    0x68: 104,  # Sitar
    0x69: 105,  # Banjo
    0x6A: 106,  # Shamisen
    0x6B: 107,  # Koto
    0x6C: 108,  # Kalimba
    0x6D: 109,  # Bagpipe
    0x6E: 110,  # Fiddle
    0x6F: 111,  # Shanai
    0x70: 112,  # Tinkle Bell
    0x71: 113,  # Agogo
    0x72: 114,  # Steel Drums
    0x73: 115,  # Woodblock
    0x74: 116,  # Taiko Drum
    0x75: 117,  # Melodic Tom
    0x76: 118,  # Synth Drum
    0x77: 119,  # Reverse Cymbal
    0x78: 120,  # Guitar Fret Noise
    0x79: 121,  # Breath Noise
    0x7A: 122,  # Seashore
    0x7B: 123,  # Bird Tweet
    0x7C: 124,  # Telephone Ring
    0x7D: 125,  # Helicopter
    0x7E: 126,  # Applause
    0x7F: 127,  # Gunshot
    
    # Extended mapping for 0x80-0xFF (same as 0x00-0x7F)
    **{i: i - 0x80 for i in range(0x80, 0x100)}
}

def get_instrument_from_hex(hex_value):
    """Convert hex instrument value to MIDI program number (0-127)"""
    return MIDI_INSTRUMENT_MAP.get(hex_value & 0xFF, 0)  # Default to piano if invalid

def handle_instrument_change(track, channel, hex_value, time_accum=0):
    """Handle instrument change command (70)"""
    midi_program = get_instrument_from_hex(hex_value)
    if channel == 6:  # Drums channel doesn't use program change
        return time_accum
        
    track.append(Message(
        'program_change', 
        program=midi_program, 
        channel=channel, 
        time=time_accum
    ))
    return 0  # Reset accumulated time

# === Configuration ===
ignore_end_signal = True
bpm = 137
base_velocity = 127
tempo = bpm2tempo(bpm)
octave_shifts = [1, 1, 1, 1, 1, 1]
base_grid = 127 # 100ms per grid unit

# === Volume Configuration ===  # Default
channel_volumes = [15, 15, 15, 0, 0, 0, 0]  # Channels 0-7

# Example hex input: each value from 0x00 to 0x7F
hex_volume_input = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

# Instrument configuration
channel_instruments = [0, 0, 0, 0, 0, 0]  # Default instruments for channels 0-5 (0 = Acoustic Grand Piano)
hex_instrument_input = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00]  # Example instrument input (1-based)

def hex_to_volume(hex_list):
    """
    Converts 7 hex values (0x00–0x7F) to MIDI volume values (127–0).
    0x00 -> 127 (max volume), 0x7F -> 0 (min volume)
    """
    return [127 - int(val) for val in hex_list]

def convert_instrument_value(hex_list):
    """
    Converts instrument value to proper MIDI program number (0-127).
    Uses the custom MIDI_INSTRUMENT_MAP for conversion.
    """
    return [get_instrument_from_hex(val) for val in hex_list]

# Apply hex volume if provided
if hex_volume_input and len(hex_volume_input) == 7:
    channel_volumes = hex_to_volume(hex_volume_input)

# Apply instrument settings if provided
if hex_instrument_input and len(hex_instrument_input) == 6:
    channel_instruments = convert_instrument_value(hex_instrument_input)

# === Drum Mapping for Channel 6 ===
def get_drum_notes(byte):
    base_byte = byte & 0x1f
    drum_map = {
            0x00:  127,                       # None But I set 127 causing to play at G9	 since how to fix to ignore?
            0x01:  42,                       # HH - Closed Hi-Hat
            0x02:  59,                       # CYM - Crash Cymbal
            0x03: [59, 42],                  # CYM + HH
            0x04:  41,                       # TM - High Tom
            0x05: [41, 42],                  # TM + HH
            0x06: [41, 59],                  # TM + CYM
            0x07: [41, 59, 42],              # TM + CYM + HH
            0x08:  38,                       # SD - Snare Drum
            0x09: [38, 42],                  # SD + HH
            0x0A: [38, 59],                  # SD + CYM
            0x0B: [38, 59, 42],              # SD + CYM + HH
            0x0C: [38, 41],                  # SD + TM
            0x0D: [38, 41, 42],              # SD + TM + HH
            0x0E: [38, 41, 59],              # SD + TM + CYM
            0x0F: [38, 41, 59, 42],          # SD + TM + CYM + HH
            0x10:  35,                       # BD - Bass Drum
            0x11: [35, 42],                  # BD + HH
            0x12: [35, 59],                  # BD + CYM
            0x13: [35, 59, 42],              # BD + CYM + HH
            0x14: [35, 41],                  # BD + TM
            0x15: [35, 41, 42],              # BD + TM + HH
            0x16: [35, 41, 59],              # BD + TM + CYM
            0x17: [35, 41, 59, 42],          # BD + TM + CYM + HH
            0x18: [35, 38],                  # BD + SD
            0x19: [35, 38, 42],              # BD + SD + HH
            0x1A: [35, 38, 59],             # BD + SD + CYM
            0x1B: [35, 38, 59, 42],          # BD + SD + CYM + HH
            0x1C: [35, 38, 41],              # BD + SD + TM
            0x1D: [35, 38, 41, 42],          # BD + SD + TM + HH
            0x1E: [35, 38, 41, 59],          # BD + SD + TM + CYM
            0x1F: [35, 38, 41, 59, 42],      # BD + SD + TM + CYM + HH
    }
    
    return drum_map.get(base_byte, [])

# === MIDI Setup ===
mid = MidiFile()
hex_strings = [

   # Channel 0
    "70 15 02 61 83 37 81 36 81 39 81 37 81 34 81 30 81 2B 85 37 81 34 85 32 81 30 81 2F 81 2D 81 2F 81 30 85 2D 81 2B 8F 61 83 2B 81 2D 81 30 81 2F 81 2D 81 2B 81 35 85 32 81 2F 85 2D 81 2B 81 2D 81 2F 81 32 81 2D 85 2F 81 30 8F 70 27 01 61 83 37 81 36 81 39 81 37 81 34 81 30 81 2B 85 37 81 34 85 32 81 30 81 2F 81 2D 81 2F 81 30 85 2D 81 2B 8F 61 83 2B 81 2D 81 30 81 2F 81 2D 81 2B 81 35 85 32 81 2F 85 2D 81 2B 81 2D 81 2F 81 32 81 39 85 37 81 34 8F 61 83 37 81 36 81 39 81 37 81 34 81 30 81 2B 85 37 81 34 85 32 81 30 81 2F 81 2D 81 2F 81 30 85 2D 81 2B 8F 61 83 2B 81 2D 81 30 81 2F 81 2D 81 2B 81 35 85 32 81 2F 85 2D 81 2B 81 2D 81 2F 81 32 81 2D 85 2F 81 30 8F 61 83 30 83 35 83 37 83 39 87 35 87 61 81 39 81 3B 81 3C 81 3B 85 39 81 39 87 37 8D 37 81 34 81 35 81 37 81 39 81 34 87 32 87 61 81 34 81 32 81 2D 81 30 81 2F 83 30 81 32 8F 61 83 37 81 36 81 39 81 37 81 34 81 30 81 2B 85 37 81 34 85 32 81 30 81 2F 81 2D 81 2F 81 30 85 2D 81 2B 8F 61 83 2B 81 2D 81 30 81 2F 81 2D 81 2B 81 35 85 32 81 2F 85 2D 81 2B 81 2D 81 2F 81 32 81 2D 85 2F 81 30 8F 70 14 02 61 83 37 81 36 81 39 81 37 81 34 81 30 81 2B 85 37 81 34 85 32 81 30 81 2F 81 2D 81 2F 81 30 85 2D 81 2B 8F 61 83 2B 81 2D 81 30 81 2F 81 2D 81 2B 81 35 85 32 81 2F 85 2D 81 2B 81 2D 81 2F 81 32 81 2D 85 2F 81 30 8F 61 9F 63",   
   # Channel 1

    "70 15 02 61 83 37 81 36 81 39 81 37 81 34 81 30 81 2B 85 37 81 34 85 32 81 30 81 2F 81 2D 81 2F 81 30 85 2D 81 2B 8F 61 83 2B 81 2D 81 30 81 2F 81 2D 81 2B 81 35 85 32 81 2F 85 2D 81 2B 81 2D 81 2F 81 32 81 2D 85 2F 81 30 8F 70 27 01 61 83 37 81 36 81 39 81 37 81 34 81 30 81 2B 85 37 81 34 85 32 81 30 81 2F 81 2D 81 2F 81 30 85 2D 81 2B 8F 61 83 2B 81 2D 81 30 81 2F 81 2D 81 2B 81 35 85 32 81 2F 85 2D 81 2B 81 2D 81 2F 81 32 81 39 85 37 81 34 8F 61 83 37 81 36 81 39 81 37 81 34 81 30 81 2B 85 37 81 34 85 32 81 30 81 2F 81 2D 81 2F 81 30 85 2D 81 2B 8F 61 83 2B 81 2D 81 30 81 2F 81 2D 81 2B 81 35 85 32 81 2F 85 2D 81 2B 81 2D 81 2F 81 32 81 2D 85 2F 81 30 8F 61 83 30 83 35 83 37 83 39 87 35 87 61 81 39 81 3B 81 3C 81 3B 85 39 81 39 87 37 8D 37 81 34 81 35 81 37 81 39 81 34 87 32 87 61 81 34 81 32 81 2D 81 30 81 2F 83 30 81 32 8F 61 83 37 81 36 81 39 81 37 81 34 81 30 81 2B 85 37 81 34 85 32 81 30 81 2F 81 2D 81 2F 81 30 85 2D 81 2B 8F 61 83 2B 81 2D 81 30 81 2F 81 2D 81 2B 81 35 85 32 81 2F 85 2D 81 2B 81 2D 81 2F 81 32 81 2D 85 2F 81 30 8F 70 14 02 61 83 37 81 36 81 39 81 37 81 34 81 30 81 2B 85 37 81 34 85 32 81 30 81 2F 81 2D 81 2F 81 30 85 2D 81 2B 8F 61 83 2B 81 2D 81 30 81 2F 81 2D 81 2B 81 35 85 32 81 2F 85 2D 81 2B 81 2D 81 2F 81 32 81 2D 85 2F 81 30 8F 61 9F 63",   
   # Channel 2 (empty)
    "",

   
   # Channel 3 (empty)
    "",

    
   # Channel 4
    "24 87 28 83 2B 83 24 87 28 83 2B 83 29 87 26 83 26 83 1F 87 23 83 26 83 24 87 28 83 2B 83 29 87 2F 83 2F 83 1F 87 23 83 26 83 24 87 28 83 2B 83 24 87 28 83 2B 83 29 87 2F 83 2F 83 29 87 26 83 26 83 1F 87 23 83 26 83 24 87 28 83 2B 83 29 87 2F 83 2F 83 1F 87 23 83 26 83 24 87 28 83 2B 83 24 87 28 83 2B 83 29 87 2F 83 2F 83 29 87 26 83 26 83 1F 87 23 83 26 83 24 87 28 83 2B 83 29 87 2F 83 2F 83 1F 87 23 83 26 83 24 87 28 83 2B 83 24 87 28 83 2B 83 29 87 2F 83 2F 83 1F 87 23 83 26 83 1F 87 23 83 26 83 24 87 28 83 2B 83 21 87 26 83 26 83 26 87 29 83 2D 83 1F 87 23 83 26 83 24 87 28 83 2B 83 29 87 2F 83 2F 83 29 87 26 83 26 83 1F 87 23 83 26 83 24 87 28 83 2B 83 29 87 2F 83 2F 83 1F 87 23 83 26 83 24 87 28 83 2B 83 24 87 28 83 2B 83 24 87 28 83 2B 83 29 87 26 83 26 83 1F 87 23 83 26 83 24 87 28 83 2B 83 29 87 2F 83 2F 83 1F 87 23 83 26 83 24 87 28 83 2B 83 61 9F 61 8F",   



   # Channel 5
    "24 87 28 83 2B 83 24 87 28 83 2B 83 29 87 26 83 26 83 1F 87 23 83 26 83 24 87 28 83 2B 83 29 87 2F 83 2F 83 1F 87 23 83 26 83 24 87 28 83 2B 83 24 87 28 83 2B 83 29 87 2F 83 2F 83 29 87 26 83 26 83 1F 87 23 83 26 83 24 87 28 83 2B 83 29 87 2F 83 2F 83 1F 87 23 83 26 83 24 87 28 83 2B 83 24 87 28 83 2B 83 29 87 2F 83 2F 83 29 87 26 83 26 83 1F 87 23 83 26 83 24 87 28 83 2B 83 29 87 2F 83 2F 83 1F 87 23 83 26 83 24 87 28 83 2B 83 24 87 28 83 2B 83 29 87 2F 83 2F 83 1F 87 23 83 26 83 1F 87 23 83 26 83 24 87 28 83 2B 83 21 87 26 83 26 83 26 87 29 83 2D 83 1F 87 23 83 26 83 24 87 28 83 2B 83 29 87 2F 83 2F 83 29 87 26 83 26 83 1F 87 23 83 26 83 24 87 28 83 2B 83 29 87 2F 83 2F 83 1F 87 23 83 26 83 24 87 28 83 2B 83 24 87 28 83 2B 83 24 87 28 83 2B 83 29 87 26 83 26 83 1F 87 23 83 26 83 24 87 28 83 2B 83 29 87 2F 83 2F 83 1F 87 23 83 26 83 24 87 28 83 2B 83 61 9F 61 8F",   

   # Channel 6 (Drums)
    "15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 15 81 01 81 09 81 11 81 20 8F",   


]  # 7 channels

def get_grid_multiplier(byte):
    if byte < 0x81: return 1
    if byte == 0xFF: return 8
    return byte - 0x80

for ch, hex_str in enumerate(hex_strings):
    if not hex_str.strip():
        continue

    track = MidiTrack()
    mid.tracks.append(track)
    track.append(MetaMessage('set_tempo', tempo=tempo, time=0))

    # Set instrument for this channel (only for channels 0-5)
    if ch < 6 and ch < len(channel_instruments):
        track.append(Message('program_change', program=channel_instruments[ch], channel=ch, time=0))

    if ch < len(channel_volumes):
        track.append(Message('control_change', control=7, value=channel_volumes[ch], channel=ch, time=0))

    octave_shift = octave_shifts[ch] if ch < len(octave_shifts) else 0
    data = [int(x, 16) for x in hex_str.split() if x]
    i = 0
    time_accum = 0
    current_note = None

    while i < len(data):
        byte = data[i]

        if byte == 0x63:
            if not ignore_end_signal:
                break
            i += 1
            continue

        elif byte == 0x70:
            if i + 2 < len(data):
                instrument = data[i + 1]
                volume = data[i + 2]
                inverted_volume = 127 - volume
                
                # Handle instrument change
                time_accum = handle_instrument_change(track, ch, instrument, time_accum)
                
                # Handle volume change
                if ch < len(channel_volumes):
                    channel_volumes[ch] = inverted_volume
                midi_channel = 9 if ch == 6 else ch
                track.append(Message(
                    'control_change', 
                    control=7, 
                    value=inverted_volume, 
                    channel=midi_channel, 
                    time=time_accum
                ))
                
                print(f"Channel {ch}: 70 command - Instrument={instrument:02X}->{get_instrument_from_hex(instrument)}, Volume={volume:02X}->{inverted_volume}")
                time_accum = 0
                i += 3
            else:
                print(f"Channel {ch}: Incomplete 70 command at position {i}")
                i += 1
            continue

        elif byte == 0x73:
            if i + 1 < len(data):
                param = data[i + 1]  # Volume byte
                inverted_volume = 127 - param
                if ch < len(channel_volumes):
                    channel_volumes[ch] = inverted_volume
                midi_channel = 9 if ch == 6 else ch
                track.append(Message('control_change', control=7, value=inverted_volume, channel=midi_channel, time=time_accum))

                print(f"Channel {ch}: 73 command - Parameter={param:02X} (Volume inverted to {inverted_volume})")
                i += 2  # Advance past 73 + param
                time_accum = 0
                continue
            else:
                print(f"Channel {ch}: Incomplete 73 command at position {i}")
                i += 1
                continue

        if byte in range(0x80, 0xFF):
            duration = get_grid_multiplier(byte) * base_grid
            time_accum += duration
            i += 1
            continue

        elif byte == 0x61:
            time_accum += base_grid
            if i + 1 < len(data) and data[i + 1] >= 0x81:
                duration = get_grid_multiplier(data[i + 1]) * base_grid
                time_accum += duration
                i += 2
            else:
                i += 1
            continue

        elif byte in range(0x00, 0x5f) and i + 1 < len(data) and data[i + 1] >= 0x81:
            duration = get_grid_multiplier(data[i + 1]) * base_grid

            if ch == 6:
                drum_notes = get_drum_notes(byte)
                if drum_notes is None:
                    time_accum += duration
                    i += 2
                    continue
                if not isinstance(drum_notes, list):
                    drum_notes = [drum_notes]

                drum_velocity = min(127, int(base_velocity * (channel_volumes[6] / 127.0)))
                for note in drum_notes:
                    track.append(Message('note_on', note=note, velocity=drum_velocity, time=time_accum, channel=9))
                    time_accum = 0
                for j, note in enumerate(drum_notes):
                    track.append(Message('note_off', note=note, velocity=0,
                                         time=duration if j == 0 else 0, channel=9))
                time_accum = base_grid
            else:
                midi_note = byte + (octave_shift * 12)
                note_velocity = min(127, int(base_velocity * (channel_volumes[ch] / 127.0)))
                if current_note:
                    track.append(Message('note_off', note=current_note, velocity=0, time=time_accum, channel=ch))
                    time_accum = 0
                track.append(Message('note_on', note=midi_note, velocity=note_velocity, time=time_accum, channel=ch))
                track.append(Message('note_off', note=midi_note, velocity=0, time=duration, channel=ch))
                current_note = midi_note
                time_accum = base_grid
            i += 2
            continue

        elif byte in range(0x00, 0x5f):
            if ch == 6:
                drum_notes = get_drum_notes(byte)
                if drum_notes is None:
                    time_accum += base_grid
                    i += 1
                    continue
                if not isinstance(drum_notes, list):
                    drum_notes = [drum_notes]
                drum_velocity = min(127, int(base_velocity * (channel_volumes[6] / 127.0)))
                for note in drum_notes:
                    track.append(Message('note_on', note=note, velocity=drum_velocity, time=time_accum, channel=9))
                    time_accum = 0
                for j, note in enumerate(drum_notes):
                    track.append(Message('note_off', note=note, velocity=0, time=base_grid if j == 0 else 0, channel=9))
            else:
                midi_note = byte + (octave_shift * 12)
                note_velocity = min(127, int(base_velocity * (channel_volumes[ch] / 127.0)))
                if current_note:
                    track.append(Message('note_off', note=current_note, velocity=0, time=time_accum, channel=ch))
                    time_accum = 0
                track.append(Message('note_on', note=midi_note, velocity=note_velocity, time=time_accum, channel=ch))
                track.append(Message('note_off', note=midi_note, velocity=0, time=base_grid, channel=ch))
                current_note = midi_note
            time_accum = 0
            i += 1
            continue

        elif byte == 0x00 and i + 1 < len(data) and data[i + 1] >= 0x81:
            time_accum += get_grid_multiplier(data[i + 1]) * base_grid
            i += 2
            continue

        i += 1

    if current_note:
        track.append(Message('note_off', note=current_note, velocity=0, time=time_accum, channel=ch))

# === Save MIDI ===
mid.save('final_music_output.mid')
print("Successfully saved 'final_music_output.mid'")
