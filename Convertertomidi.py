# Knows issues.  
# when read hex 61 does not set note off and will cause to longer notes when importing on onlinesequencer. use midieditor to save.
# it is possible that there may be bugs
# event set to instrument automatic in drums without control affecting game hero midi player system. 
# Limit the range of the notes musical and drums 00 to 5f
# Drums map not verified. may imperfectly
# will cause to play hex 62 should not play notes.

# Not implemented
# 64 and 65 feature Not supported since required load hex read .hex
# 70 hex automatic instrument and Volume also will be ignore, does the midi support change instrument from channel?.
# 73 hex automatic set volume? also will be ignore
# 66 hex change octave of max of  4 channel in gluck2 max of 6 channel track
import mido
from mido import MidiFile, MidiTrack, Message, MetaMessage, bpm2tempo

# === Configuration ===
ignore_end_signal = True
bpm = 120
velocity = 80
tempo = bpm2tempo(bpm)
octave_shifts = [1, 1, 1, 1, 1, 0, 0]  # Octave shifts per channel
base_grid = 100  # 100ms per grid unit (81 = 100ms)

# === Drum Mapping for Channel 6 ===
def get_drum_notes(byte):
    """Get drum notes for a byte, handling all three identical ranges"""
    # Empty space bytes
    if byte in {0x00, 0x20, 0x40}: #  when reading hex 00 20 40 it will play notes number 100 in C7 which is not supposed to play notes
        return 100 # Fix me
    
    # Map to the 00-1F range by masking
    base_byte = byte & 0x1F
    
    # Original 00-1F mappings # Not verified and imperfectly.
    drum_map = {
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
    "3E 61 82 3E 61 3E 61 3C 61 82 3C 61 3C 61 3E 61 3E 61 3E 61 3C 83 3E 61 3C 61 82 3E 61 82 3E 61 3E 61 3C 61 82 3C 61 3C 61 3E 61 3E 61 3E 61 3C 83 3E 61 3C 61 82 43 61 82 43 61 43 61 41 61 82 41 61 41 61 43 61 43 61 43 61 41 83 43 61 41 61 82 40 61 82 40 61 40 61 3E 61 82 3E 61 3E 61 40 61 40 61 40 61 3E 85 61 83 70 58 10 3E 85 3E 81 3C 83 61 81 37 81 3E 81 3E 81 40 81 3C 85 39 81 39 81 3E 81 3E 81 40 83 3C 83 61 81 39 81 3B 81 3C 81 3B 81 39 89 40 85 3E 85 61 81 39 81 40 81 41 81 40 81 3E 85 61 81 3C 81 3B 81 3C 81 3B 81 3B 83 3C 81 61 81 3B 83 37 89 61 83 70 48 10 3E 85 3E 81 3C 83 61 81 37 81 3E 81 3E 81 40 81 3C 85 39 81 39 81 3E 81 3E 81 40 83 3C 83 61 81 39 81 3B 81 3C 81 3B 81 39 89 40 85 3E 85 61 81 39 81 40 81 41 81 40 81 3E 85 61 81 3C 81 3B 81 3C 81 3B 81 3B 83 3C 81 61 81 3B 83 37 89 61 83 70 59 10 37 87 43 85 37 89 37 81 39 81 3B 81 3C 81 3E 83 3C 83 39 8F 43 81 40 81 3C 81 39 81 35 8F 61 87 45 81 41 81 3E 81 3B 81 37 8F 61 87 35 81 34 81 32 83 70 4A 10 61 83 3E 85 3C 81 3C 83 61 81 3B 81 3C 81 43 83 40 3E 3C 83 61 83 3E 85 3C 81 3B 81 3C 81 61 81 3B 81 3C 81 45 83 40 3E 3C 83 61 81 40 81 40 81 39 81 3C 81 3C 81 3E 83 40 81 40 81 40 81 39 3C 82 3E 83 61 81 40 83 61 81 3C 81 3B 81 3B 81 3B 81 3C 81 3B 81 3B 81 3B 81 3B 39 37 83 37 83 3E 83 3C 81 3B 83 3C 81 37 81 37 81 3E 81 3C 81 3B 81 3C 85 61 81 39 81 3E 83 3C 83 3B 81 3C 81 37 81 37 81 3E 81 3C 81 3B 81 3C 85 61 83 3E 83 3C 83 39 83 61 83 40 85 3E 85 3E 81 3C 81 40 81 3E 81 3E 81 3C 81 3C 81 3B 81 3C 81 3B 81 3C 81 3B 81 3C 81 37 85 61 83 70 18 14 3E 85 3E 81 3C 83 61 81 37 81 3E 81 3E 81 40 81 3C 85 39 81 39 81 3E 81 3E 81 40 83 3C 83 61 81 39 81 3B 81 3C 81 3B 81 39 81 47 81 48 81 47 81 45 81 40 85 3E 85 61 81 39 81 40 81 41 81 40 81 3E 85 61 81 3C 81 3B 81 3C 81 3B 81 3B 83 3C 81 61 81 3B 83 37 83 47 83 43 83 61 81 73 1F 3E 85 3E 81 3C 83 61 81 37 81 3E 81 3E 81 40 81 3C 85 39 81 39 81 3E 81 3E 81 40 83 3C 83 61 81 39 81 3B 81 3C 81 3B 81 39 81 47 81 48 81 47 81 45 81 40 85 3E 85 61 81 39 81 40 81 41 81 40 81 3E 85 61 81 3C 81 3B 81 3C 81 3B 81 3B 83 3C 81 61 81 3B 83 37 83 47 83 43 83 61 81 73 24 3E 85 3E 81 3C 83 61 81 37 81 3E 81 3E 81 40 81 3C 85 39 81 39 81 3E 81 3E 81 40 83 3C 83 61 81 39 81 3B 81 3C 81 3B 81 39 81 47 81 48 81 47 81 45 81 40 85 3E 85 61 81 39 81 40 81 41 81 40 81 3E 85 61 81 3C 81 3B 81 3C 81 3B 81 3B 83 3C 81 61 81 3B 83 37 83 47 83 43 83 61 81 61 62 ",
    # Channel 1
    "37 61 37 61 37 61 37 61 37 61 37 61 37 61 37 61 37 61 37 61 37 61 37 61 37 61 37 61 37 61 37 61 34 61 34 61 34 61 34 61 34 61 34 61 34 61 34 61 34 61 34 61 34 61 34 61 34 61 34 61 34 61 34 61 39 61 39 61 39 61 39 61 39 61 39 61 39 61 39 61 39 61 39 61 39 61 39 61 39 61 39 61 39 61 39 61 32 61 32 61 32 61 32 61 32 61 32 61 32 61 32 61 32 61 32 61 32 61 32 61 32 61 32 61 32 61 32 61 84 37 81 61 85 37 81 61 85 37 81 61 85 37 81 61 85 34 81 61 85 34 81 61 85 34 81 61 85 34 81 61 85 39 81 61 85 39 81 61 85 39 81 61 85 39 81 61 85 32 81 61 85 32 81 61 85 32 81 61 85 32 81 61 81 30 81 37 81 3C 81 37 81 40 81 37 81 3C 81 37 81 30 81 37 81 3C 81 37 81 40 81 37 81 3C 81 37 81 2D 81 34 81 39 81 34 81 3C 81 34 81 39 81 34 81 2D 81 34 81 39 81 34 81 3C 81 34 81 39 81 34 81 32 81 39 81 3E 81 39 81 41 81 39 81 3E 81 39 81 32 81 39 81 3E 81 39 81 41 81 39 81 3E 81 39 81 2B 81 32 81 37 81 32 81 3B 81 32 81 37 81 32 81 2B 81 32 81 37 81 32 81 3B 81 37 81 3B 81 3E 81 61 81 37 61 82 37 61 82 37 61 82 37 61 82 37 61 82 37 61 82 37 61 82 37 61 82 34 61 82 34 61 82 34 61 82 34 61 82 34 61 82 34 61 82 34 61 82 34 61 82 39 61 82 39 61 82 39 61 86 39 61 84 39 61 39 61 39 61 39 61 84 32 81 61 85 32 81 61 85 32 81 61 85 32 81 61 81 61 83 37 81 61 85 37 81 61 85 37 81 61 85 37 81 61 85 34 81 61 85 34 81 61 85 34 81 61 85 34 81 61 85 39 81 61 85 39 81 61 85 39 81 61 85 39 81 61 85 32 81 61 85 32 81 61 85 32 81 61 85 32 81 61 85 37 81 61 85 37 81 61 85 37 81 61 85 37 81 61 85 34 81 61 85 34 81 61 85 34 81 61 85 34 81 61 85 39 81 61 85 39 81 61 85 39 81 61 85 39 81 61 85 32 81 61 85 32 81 61 85 32 81 61 85 32 81 61 81 73 1F 37 61 37 61 37 61 37 61 37 61 37 61 37 61 37 61 37 61 37 61 37 61 37 61 37 61 37 61 37 61 37 61 34 61 34 61 34 61 34 61 34 61 34 61 34 61 34 61 34 61 34 61 34 61 34 61 34 61 34 61 34 61 34 61 39 61 39 61 39 61 39 61 39 61 39 61 39 61 39 61 39 61 39 61 39 61 39 61 39 61 39 61 39 61 39 61 32 61 32 61 32 61 32 61 32 61 32 61 32 61 32 61 32 61 32 61 32 61 32 61 32 61 32 61 32 61 32 61 73 24 37 61 37 61 37 61 37 61 37 61 37 61 37 61 37 61 37 61 37 61 37 61 37 61 37 61 37 61 37 61 37 61 34 61 34 61 34 61 34 61 34 61 34 61 34 61 34 61 34 61 34 61 34 61 34 61 34 61 34 61 34 61 34 61 39 61 39 61 39 61 39 61 39 61 39 61 39 61 39 61 39 61 39 61 39 61 39 61 39 61 39 61 39 61 39 61 32 61 32 61 32 61 32 61 32 61 32 61 32 61 32 61 32 61 32 61 32 61 32 61 32 61 32 61 32 61 32 61 73 29 37 61 37 61 37 61 37 61 37 61 37 61 37 61 37 61 37 61 37 61 37 61 37 61 37 61 37 61 37 61 37 61 34 61 34 61 34 61 34 61 34 61 34 61 34 61 34 61 34 61 34 61 34 61 34 61 34 61 34 61 34 61 34 61 39 61 39 61 39 61 39 61 39 61 39 61 39 61 39 61 39 61 39 61 39 61 39 61 39 61 39 61 39 61 39 61 32 61 32 61 32 61 32 61 32 61 32 61 32 61 32 61 32 61 32 61 32 61 32 61 32 61 32 61 32 61 32 61 61",
    # Channel 2
    "24 8F 24 8F 21 8F 21 8F 1A 8F 1A 8F 1F 8F 1F 8F 24 8F 24 8B 23 83 21 8F 21 87 23 83 24 83 1A 8F 1A 87 1C 83 1D 83 1F 8F 1F 8F 24 8F 24 8B 23 83 21 8F 21 87 23 83 24 83 1A 8F 1A 87 1C 83 1D 83 1F 8F 1F 8F 24 8F 24 8B 23 83 21 8F 21 87 23 83 24 83 1A 8F 1A 87 1C 83 1D 83 1F 8F 1F 8F 24 81 30 81 24 81 30 81 24 81 30 81 24 81 30 81 24 81 30 81 24 81 30 81 24 81 30 81 23 83 21 81 2D 81 21 81 2D 81 21 81 2D 81 21 81 2D 81 21 81 2D 81 21 81 2D 81 23 83 24 83 1A 81 26 81 1A 81 26 81 1A 81 26 81 1A 81 26 81 1A 81 26 81 1A 81 26 81 1C 83 1D 83 1F 81 2B 81 1F 81 2B 81 1F 81 2B 81 1F 81 2B 81 1F 81 2B 81 1F 81 2B 81 1F 81 2B 81 1F 81 2B 81 24 81 30 81 24 81 30 81 24 81 30 81 24 81 30 81 24 81 30 81 24 81 30 81 24 81 30 81 23 83 21 81 2D 81 21 81 2D 81 21 81 2D 81 21 81 2D 81 21 81 2D 81 21 81 2D 81 23 83 24 83 1A 81 26 81 1A 81 26 81 1A 81 26 81 1A 81 26 81 1A 81 26 81 1A 81 26 81 1C 83 1D 83 1F 81 2B 81 1F 81 2B 81 1F 81 2B 81 1F 81 2B 81 1F 81 2B 81 1F 81 2B 81 1F 81 2B 81 1F 81 2B 81 73 1F 24 8F 24 8B 23 83 21 8F 21 8F 1A 8F 1A 87 1C 83 1D 83 1F 8F 1F 8F 73 24 24 8F 24 8B 23 83 21 8F 21 8F 1A 8F 1A 87 1C 83 1D 83 1F 8F 1F 8F 73 29 24 8F 24 8B 23 83 21 8F 21 8F 1A 8F 1A 87 1C 83 1D 83 1F 8F 1F 8F 61 ", 
    # Channel 3
    "",    
    # Channel 4 (empty)
    "",
    # Channel 5 (empty)
    "",
    # Channel 6 (Drums)
    "12 81 02 81 0A 81 12 81 12 81 02 81 0A 81 12 81 12 81 02 81 0A 81 12 81 12 81 02 81 0A 81 08 08 12 81 02 81 0A 81 12 81 12 81 02 81 0A 81 12 81 12 81 02 81 0A 81 12 81 12 81 02 81 0A 81 08 08 12 81 02 81 0A 81 12 81 12 81 02 81 0A 81 12 81 12 81 02 81 0A 81 12 81 12 81 02 81 0A 81 08 08 12 81 02 81 0A 81 12 81 12 81 02 81 0A 81 12 81 12 81 02 81 0A 81 12 81 12 81 02 81 08 08 08 08 12 81 02 81 0A 81 12 81 12 81 02 81 0A 81 12 81 12 81 02 81 0A 81 12 81 12 81 02 81 0A 81 12 81 12 81 02 81 0A 81 12 81 12 81 02 81 0A 81 12 81 12 81 02 81 0A 81 12 81 12 81 02 81 08 08 08 08 12 81 02 81 0A 81 12 81 12 81 02 81 0A 81 12 81 12 81 02 81 0A 81 12 81 12 81 02 81 0A 81 12 81 12 81 02 81 0A 81 12 81 12 81 02 81 0A 81 12 81 12 81 02 81 0A 81 12 81 12 81 02 81 08 08 08 08 12 81 02 81 0A 81 12 81 12 81 02 81 0A 81 12 81 12 81 02 81 0A 81 12 81 12 81 02 81 0A 81 12 81 12 81 02 81 0A 81 12 81 12 81 02 81 0A 81 12 81 12 81 02 81 0A 81 12 81 12 81 02 81 08 08 08 08 12 81 02 81 0A 81 12 81 12 81 02 81 0A 81 12 81 12 81 02 81 0A 81 12 81 12 81 02 81 0A 81 12 81 12 81 02 81 0A 81 12 81 12 81 02 81 0A 81 12 81 12 81 02 81 0A 81 12 81 12 81 02 81 08 08 08 08 1A 81 02 02 1A 81 02 02 1A 81 02 02 1A 81 02 02 1A 81 02 02 08 08 08 08 1A 81 02 02 1A 81 02 02 1A 81 02 81 1A 81 02 81 1A 81 02 81 1A 81 02 81 08 08 08 08 08 08 08 08 1A 81 1A 81 1A 81 1A 81 1A 81 02 02 1A 81 02 02 1A 81 02 02 08 08 08 08 1A 81 02 02 08 08 08 08 1A 81 1A 81 1A 81 1A 81 12 81 02 81 1A 81 02 81 12 81 02 81 1A 81 02 81 12 81 02 81 1A 81 02 81 12 81 02 81 1A 81 02 81 12 81 02 02 1A 81 02 02 12 81 02 02 1A 81 02 02 12 81 02 02 1A 81 02 02 12 81 02 02 1A 81 02 02 12 81 02 02 1A 81 02 02 12 81 02 02 1A 81 02 02 12 81 02 02 1A 81 02 02 12 81 02 02 1A 81 02 02 12 81 02 02 1A 81 02 02 12 81 02 02 1A 81 02 02 12 81 02 02 1A 81 02 02 12 81 02 02 1A 81 02 02 12 81 02 02 1A 81 02 02 12 81 02 02 1A 81 02 02 12 81 02 02 1A 81 02 02 12 81 02 02 1A 81 02 02 12 81 02 02 1A 81 02 02 12 81 02 02 1A 81 02 02 12 81 02 02 1A 81 02 02 12 81 02 02 1A 81 02 02 12 81 02 02 1A 81 02 02 12 81 02 02 1A 81 02 02 12 81 02 02 1A 81 02 02 12 81 02 02 1A 81 02 02 12 81 02 02 1A 81 02 02 12 81 02 02 1A 81 02 02 12 81 02 02 1A 81 02 02 12 81 02 02 1A 81 02 02 12 81 02 02 1A 81 02 02 12 81 02 02 1A 81 02 02 1A 81 02 02 1A 81 02 02 08 08 08 08 08 08 08 08 12 81 02 81 0A 81 12 81 12 81 02 81 0A 81 12 81 12 81 02 81 0A 81 12 81 12 81 02 81 0A 81 12 81 12 81 02 81 0A 81 12 81 12 81 02 81 0A 81 12 81 12 81 02 81 0A 81 12 81 08 08 08 08 08 08 08 08 12 81 02 81 0A 81 12 81 12 81 02 81 0A 81 12 81 12 81 02 81 0A 81 12 81 12 81 02 81 0A 81 12 81 12 81 02 81 0A 81 12 81 12 81 02 81 0A 81 12 81 12 81 12 81 0A 81 12 81 08 08 08 08 08 08 08 08 02 81 02 81 06 81 02 81 02 81 02 81 06 81 02 81 02 81 02 81 06 81 02 81 02 81 02 81 06 81 02 81 02 81 02 81 06 81 02 81 02 81 02 81 06 81 02 81 02 81 02 81 06 81 02 81 04 04 04 04 04 04 04 04 02 81 02 81 06 81 02 81 02 81 02 81 06 81 02 81 02 81 02 81 06 81 02 81 02 81 02 81 06 81 02 81 02 81 02 81 06 81 02 81 02 81 02 81 06 81 02 81 02 81 02 81 06 81 02 81 04 04 04 04 04 04 04 04 01 81 01 81 04 81 01 81 01 81 01 81 04 81 01 81 01 81 01 81 04 81 01 81 01 81 01 81 04 81 01 81 01 81 01 81 04 81 01 81 01 81 01 81 04 81 01 81 01 81 01 81 04 81 01 81 04 04 04 04 04 04 04 04 01 81 01 81 04 81 01 81 01 81 01 81 04 81 01 81 01 81 01 81 04 81 01 81 01 81 01 81 04 81 01 81 01 81 01 81 04 81 01 81 01 81 01 81 04 81 01 81 01 81 01 81 04 81 01 81 04 04 04 04 04 04 04 04 61",
]

def get_grid_multiplier(byte):
    """Calculate grid multiplier from hex value (81-FF)"""
    if byte < 0x81: return 1
    if byte == 0xFF: return 8  # Special long duration
    return byte - 0x80  # 81=1, 82=2, ..., FE=126

# === Processing ===
for ch, hex_str in enumerate(hex_strings):
    if not hex_str.strip():  # Skip empty channels
        continue
        
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(MetaMessage('set_tempo', tempo=tempo, time=0))
    
    octave_shift = octave_shifts[ch] if ch < len(octave_shifts) else 0
    
    data = [int(x, 16) for x in hex_str.split() if x]
    i = 0
    time_accum = 0
    current_note = None

    while i < len(data):
        byte = data[i]
        
        # End signal (63)
        if byte == 0x63:
            if not ignore_end_signal:
                break
            i += 1
            continue
            
        # Instrument/Volume change (70) - 2 parameters
        elif byte == 0x70:
           if i+2 < len(data):
             instrument = data[i+1]  # Offset 1
             volume = data[i+2]      # Offset 2
             print(f"Channel {ch}: 70 command - Instrument={instrument:02X} Volume={volume:02X}")
             i += 2  # Skip command + 2 parameters
           else:
             print(f"Channel {ch}: Incomplete 70 command at position {i}")
             i += 1  # Skip just the command
             continue

# Unknown command (73) - 1 parameter
        elif byte == 0x73:
           if i+1 < len(data):
             param = data[i+2]  # Only offset 1
             print(f"Channel {ch}: 73 command - Parameter={param:02X} (00-FF)")
             i += 1  # Skip command + 1 parameter
           else:
             print(f"Channel {ch}: Incomplete 73 command at position {i}")
             i += 1  # Skip just the command
             continue
       
       
       
            
        # Note off (61) with optional duration
        elif byte == 0x61:
            time_accum += base_grid  # Always add base grid first
            
            # Check for optional duration
            if i+1 < len(data) and data[i+1] >= 0x81:
                duration = get_grid_multiplier(data[i+1]) * base_grid
                time_accum += duration
                i += 2
            else:
                i += 1
            continue
            
        # Note with explicit duration (00-67 followed by 81-FF)
        elif byte in range(0x00, 0x68) and i+1 < len(data) and data[i+1] >= 0x81:
            duration = get_grid_multiplier(data[i+1]) * base_grid
            
            # For drum channel (6)
            if ch == 6:
                drum_notes = get_drum_notes(byte)
                if drum_notes is None:  # Empty space (00, 20, 40)
                    time_accum += duration
                    i += 2
                    continue
                    
                if not isinstance(drum_notes, list):
                    drum_notes = [drum_notes]
                
                # Send note_on for all drum notes
                for note in drum_notes:
                    track.append(Message('note_on', note=note, velocity=velocity, 
                                       time=time_accum, channel=9))
                    time_accum = 0
                
                # Send note_off for all drum notes
                for note in drum_notes:
                    track.append(Message('note_off', note=note, velocity=0,
                                       time=duration, channel=9))
                    duration = 0  # Only apply duration once
            else:
                # For melodic channels
                midi_note = byte + (octave_shift * 12)
                if current_note:
                    track.append(Message('note_off', note=current_note,
                                       velocity=0, time=time_accum, channel=ch))
                    time_accum = 0
                track.append(Message('note_on', note=midi_note, velocity=velocity,
                                   time=time_accum, channel=ch))
                track.append(Message('note_off', note=midi_note, velocity=0,
                                   time=duration, channel=ch))
                current_note = midi_note
            time_accum = base_grid  # Small gap after note
            i += 2
            continue
            
        # Note without explicit duration (default 100ms)
        elif byte in range(0x00, 0x68):
            # For drum channel (6)
            if ch == 6:
                drum_notes = get_drum_notes(byte)
                if drum_notes is None:  # Empty space (00, 20, 40)
                    time_accum += base_grid
                    i += 1
                    continue
                    
                if not isinstance(drum_notes, list):
                    drum_notes = [drum_notes]
                
                # Send note_on for all drum notes
                for note in drum_notes:
                    track.append(Message('note_on', note=note, velocity=velocity,
                                       time=time_accum, channel=9))
                    time_accum = 0
                
                # Send note_off for all drum notes
                for note in drum_notes:
                    track.append(Message('note_off', note=note, velocity=0,
                                       time=base_grid, channel=9))
            else:
                # For melodic channels
                midi_note = byte + (octave_shift * 12)
                if current_note:
                    track.append(Message('note_off', note=current_note,
                                       velocity=0, time=time_accum, channel=ch))
                    time_accum = 0
                track.append(Message('note_on', note=midi_note, velocity=velocity,
                                   time=time_accum, channel=ch))
                track.append(Message('note_off', note=midi_note, velocity=0,
                                   time=base_grid, channel=ch))
                current_note = midi_note
            time_accum = 0
            i += 1
            continue
            
        # Empty note (00) with grid control
        elif byte == 0xFF and i+1 < len(data) and data[i+1] >= 0x81:
            time_accum += get_grid_multiplier(data[i+1]) * base_grid
            i += 2
            continue
            
        # Skip invalid bytes
        i += 1

    # End any lingering note
    if current_note:
        track.append(Message('note_off', note=current_note,
                           velocity=0, time=time_accum, channel=ch))

# === Save MIDI ===
mid.save('final_music_output.mid')
print("Successfully saved 'final_music_output.mid'")
print("Key features:")
print("- Three identical drum mapping ranges: 00-1F, 20-3F, 40-5F")
print("- Hex 00, 20, and 40 treated as empty spaces (no sound)")
print("- Hex 70 (instrument/volume change) detected and ignored")
print("- Accurate duration handling (81=100ms, 82=200ms, ..., FF=800ms)")
print("- Simultaneous drum notes when required")
print("- All timing relationships preserved")
