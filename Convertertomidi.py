# Knows issues.  
# when read hex 61 does not set note off and will cause to longer notes when importing on onlinesequencer. use midieditor to save.
# it is possible that there may be bugs
# event set to instrument automatic in drums without control affecting game hero midi player system of roblox. 
# Limit the range of the notes musical and drums 00 to 5f
# Drums map not verified. may imperfectly
# will cause to play hex 62 should not play notes.
# if read hex 00 20 40 will cause to play notes which should ignore.
# Partially implemented
# 70 hex automatic instrument not implemented and Volume also the instrument will be ignore, does the midi support change instrument from channel?.
# 73 hex automatic set volume only
# Not implemented
# 64 and 65 feature Not supported since required load hex read .hex
# 66 hex change octave of max of  4 channel in gluck2 max of 6 channel track
import mido
from mido import MidiFile, MidiTrack, Message, MetaMessage, bpm2tempo

# === Configuration ===
ignore_end_signal = True
bpm = 120
base_velocity = 80
tempo = bpm2tempo(bpm)
octave_shifts = [1, 1, 1, 1, 1, 1]
base_grid = 100  # 100ms per grid unit

# === Volume Configuration ===
channel_volumes = [127, 127, 127, 127, 127, 127, 127]  # Channels 0-7

# === Drum Mapping for Channel 6 ===
def get_drum_notes(byte):
    if byte in {0x00, 0x20, 0x40}:
        return 100
    base_byte = byte & 0x1F
    drum_map = {
        0x01: 42, 0x02: 59, 0x03: [59, 42],
        0x04: 41, 0x05: [41, 42], 0x06: [41, 59], 0x07: [41, 59, 42],
        0x08: 38, 0x09: [38, 42], 0x0A: [38, 59], 0x0B: [38, 59, 42],
        0x0C: [38, 41], 0x0D: [38, 41, 42], 0x0E: [38, 41, 59], 0x0F: [38, 41, 59, 42],
        0x10: 35, 0x11: [35, 42], 0x12: [35, 59], 0x13: [35, 59, 42],
        0x14: [35, 41], 0x15: [35, 41, 42], 0x16: [35, 41, 59], 0x17: [35, 41, 59, 42],
        0x18: [35, 38], 0x19: [35, 38, 42], 0x1A: [35, 38, 59], 0x1B: [35, 38, 59, 42],
        0x1C: [35, 38, 41], 0x1D: [35, 38, 41, 42], 0x1E: [35, 38, 41, 59], 0x1F: [35, 38, 41, 59, 42],
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
                print(f"Channel {ch}: 70 command - Parameter={volume:02X} (Volume inverted to {inverted_volume})")

                if ch < len(channel_volumes):
                    channel_volumes[ch] = inverted_volume
                midi_channel = 6 #  if ch == 9 else ch - disabled
                track.append(Message('control_change', control=7, value=inverted_volume, channel=midi_channel, time=time_accum))
                
                time_accum = 0

                i += 3
            else:
                print(f"Channel {ch}: Incomplete 70 command at position {i}")
                i += 1
            continue
         # Volume only change (73) - 1 parameter
        elif byte == 0x73:
            if i + 1 < len(data):
                param = data[i + 1]  # Volume byte
                inverted_volume = 127 - param
                if ch < len(channel_volumes):
                    channel_volumes[ch] = inverted_volume
                midi_channel = 6 #  if ch == 6 else ch - disabled
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
                time_accum = 100
            else:
                midi_note = byte + (octave_shift * 12)
                note_velocity = min(127, int(base_velocity * (channel_volumes[ch] / 127.0)))
                if current_note:
                    track.append(Message('note_off', note=current_note, velocity=0, time=time_accum, channel=ch))
                    time_accum = 0
                track.append(Message('note_on', note=midi_note, velocity=note_velocity, time=time_accum, channel=ch))
                track.append(Message('note_off', note=midi_note, velocity=0, time=duration, channel=ch))
                current_note = midi_note
                time_accum = 100
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
