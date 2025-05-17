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
bpm = 150
base_velocity = 127
tempo = bpm2tempo(bpm)
octave_shifts = [1, 1, 1, 1, 1, 1]
base_grid = 127 # 100ms per grid unit

# === Volume Configuration ===  # Default
channel_volumes = [0, 0, 0, 0, 0, 0, 0]  # Channels 0-7

# Example hex input: each value from 0x00 to 0x7F
hex_volume_input = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

# Instrument configuration
channel_instruments = [000, 000, 000, 000, 000, 000]  # Default instruments for channels 0-6 (0 = Acoustic Grand Piano)
hex_instrument_input = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00]  # Example instrument input (1-based)


def hex_to_volume(hex_list):
    """
    Converts 7 hex values (0x00–0x7F) to MIDI volume values (127–0).
    0x00 -> 127 (max volume), 0x7F -> 0 (min volume)
    """
    return [127 - int(val) for val in hex_list]

def convert_instrument_value(hex_list1):
    """
    Converts instrument value to proper MIDI program number (0-127).
    Handles both hex (0x00-0x7F) and decimal (0-127) inputs.
    For values 0x80-0xFF, wraps around to 0x00-0x7F.
    """
    return [int (val & 0x7F) for val in hex_list1] # Mask to 7 bits to ensure 0-127 range

# Apply hex volume if provided
if hex_volume_input and len(hex_volume_input) == 7:
    channel_volumes = hex_to_volume(hex_volume_input)

# Apply instrument settings if provided
if hex_instrument_input and len(hex_instrument_input) == 6:
    # Convert instrument values and ensure they're in valid range
    channel_instruments = convert_instrument_value(hex_instrument_input)
# Debug print
print("Channel volumes:", channel_volumes)
print("Channel instruments:", channel_instruments)

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
    "2D 81 61 81 2D 81 30 81 39 81 37 81 34 32 30 81 34 81 37 8D 61 81 39 81 39 81 3C 81 39 81 37 81 34 32 30 81 34 81 32 81 2D 8B 61 81 34 81 34 81 37 81 34 81 32 81 32 81 30 81 34 81 37 89 32 81 34 81 32 83 30 81 34 81 32 81 30 81 2D 81 30 81 30 8F 2D 81 61 81 2D 81 30 81 39 81 37 81 34 32 30 81 34 81 37 8D 61 81 39 81 39 81 3C 81 39 81 37 81 34 32 30 81 34 81 32 81 2D 8B 61 81 34 81 34 81 37 81 34 81 32 81 32 81 30 81 34 81 37 89 32 81 34 81 32 83 30 81 34 81 32 81 30 81 2D 81 30 81 30 8F 61 81 30 81 30 81 30 81 32 34 37 81 37 81 34 81 39 81 3C 8D 61 81 39 81 39 81 37 81 39 81 37 81 37 81 34 81 37 81 32 34 8C 61 83 34 81 37 81 39 81 37 81 37 81 37 81 37 81 32 34 82 32 89 61 83 36 81 35 81 35 81 35 81 37 81 39 81 39 3B 37 8D 61 83 39 81 3C 81 39 81 37 81 34 81 32 81 34 81 37 8D 61 81 39 81 39 81 3C 81 39 81 37 81 34 32 30 81 34 32 2D 8D 61 81 34 81 34 81 37 81 34 81 32 81 32 81 30 81 34 81 37 89 32 81 34 81 32 83 30 81 34 81 32 81 30 81 2D 81 30 81 30 8F 63 ",
   # Channel 1
    "2D 81 61 81 2D 81 30 81 39 81 37 81 34 32 30 81 34 81 37 8D 61 81 39 81 39 81 3C 81 39 81 37 81 34 32 30 81 34 81 32 81 2D 8B 61 81 34 81 34 81 37 81 34 81 32 81 32 81 30 81 34 81 37 89 32 81 34 81 32 83 30 81 34 81 32 81 30 81 2D 81 30 81 30 8F 2D 81 61 81 2D 81 30 81 39 81 37 81 34 32 30 81 34 81 37 8D 61 81 39 81 39 81 3C 81 39 81 37 81 34 32 30 81 34 81 32 81 2D 8B 61 81 34 81 34 81 37 81 34 81 32 81 32 81 30 81 34 81 37 89 32 81 34 81 32 83 30 81 34 81 32 81 30 81 2D 81 30 81 30 8F 61 81 30 81 30 81 30 81 32 34 37 81 37 81 34 81 39 81 3C 8D 61 81 39 81 39 81 37 81 39 81 37 81 37 81 34 81 37 81 32 34 8C 61 83 34 81 37 81 39 81 37 81 37 81 37 81 37 81 32 34 82 32 89 61 83 36 81 35 81 35 81 35 81 37 81 39 81 39 3B 37 8D 61 83 39 81 3C 81 39 81 37 81 34 81 32 81 34 81 37 8D 61 81 39 81 39 81 3C 81 39 81 37 81 34 32 30 81 34 32 2D 8D 61 81 34 81 34 81 37 81 34 81 32 81 32 81 30 81 34 81 37 89 32 81 34 81 32 83 30 81 34 81 32 81 30 81 2D 81 30 81 30 8F 63 ",
   # Channel 2
    "61 8F 34 81 37 81 3C 81 3E 85 3C 83 61 8F 34 81 39 81 3C 81 3E 85 3C 83 61 8F 2B 81 2F 81 32 81 39 85 37 83 35 81 34 81 32 81 34 81 32 87 30 8F 61 8F 34 81 37 81 3C 81 3E 85 3C 83 61 8F 34 81 39 81 3C 81 3E 85 3C 83 61 8F 2B 81 2F 81 32 81 39 85 37 83 35 81 34 81 32 81 34 81 32 87 61 8F 61 8F 61 83 35 81 37 85 35 83 35 83 61 8B 61 83 3C 81 3E 85 3C 83 3C 83 61 8B 61 83 32 81 37 85 36 83 35 83 61 87 61 8F 61 8F 34 81 37 81 3C 81 3E 85 3C 83 61 8F 34 81 39 81 3C 81 3E 85 3C 83 61 8F 2B 81 2F 81 32 81 39 85 37 83 35 81 34 81 32 81 34 81 32 87 34 81 37 81 3C 81 3E 85 3C 83 61 8F",
   
   # Channel 3
    "61 8F 34 81 37 81 3C 81 3E 85 3C 83 61 8F 34 81 39 81 3C 81 3E 85 3C 83 61 8F 2B 81 2F 81 32 81 39 85 37 83 35 81 34 81 32 81 34 81 32 87 30 8F 61 8F 34 81 37 81 3C 81 3E 85 3C 83 61 8F 34 81 39 81 3C 81 3E 85 3C 83 61 8F 2B 81 2F 81 32 81 39 85 37 83 35 81 34 81 32 81 34 81 32 87 61 8F 61 8F 61 83 35 81 37 85 35 83 35 83 61 8B 61 83 3C 81 3E 85 3C 83 3C 83 61 8B 61 83 32 81 37 85 36 83 35 83 61 87 61 8F 61 8F 34 81 37 81 3C 81 3E 85 3C 83 61 8F 34 81 39 81 3C 81 3E 85 3C 83 61 8F 2B 81 2F 81 32 81 39 85 37 83 35 81 34 81 32 81 34 81 32 87 34 81 37 81 3C 81 3E 85 3C 83 61 8F",
    
   # Channel 4 (empty)
    "2D 81 2D 81 2D 81 61 89 24 81 24 81 30 81 2B 81 24 81 24 81 30 81 2B 81 24 81 24 81 30 81 2B 81 24 81 24 81 30 81 2B 81 21 81 21 81 21 81 1C 81 21 81 21 81 21 81 1C 81 21 81 21 81 21 81 1C 81 21 81 21 81 61 81 1C 81 28 81 28 81 34 81 2F 81 28 81 28 81 34 81 2F 81 26 81 26 81 32 2D 26 81 26 81 21 81 21 81 23 81 24 81 24 81 30 81 2B 81 24 81 24 81 30 81 2B 81 2D 81 2D 81 2D 81 61 89 24 81 24 81 30 81 2B 81 24 81 24 81 30 81 2B 81 24 81 24 81 30 81 2B 81 24 81 24 81 30 81 2B 81 21 81 21 81 21 81 1C 81 21 81 21 81 21 81 1C 81 21 81 21 81 21 81 1C 81 21 81 21 81 61 81 1C 81 28 81 28 81 34 81 2F 81 28 81 28 81 34 81 2F 81 26 81 26 81 32 2D 26 81 26 81 21 81 21 81 23 81 24 81 24 81 30 81 2B 81 24 81 24 81 30 81 2B 81 24 81 24 81 30 81 2B 81 24 81 24 81 30 81 2B 81 29 81 29 81 35 81 24 81 29 81 29 81 35 81 30 81 29 81 29 81 35 81 24 81 29 81 29 81 2B 2D 30 81 24 81 24 81 30 81 2B 81 24 81 24 81 30 81 2B 81 24 81 24 81 30 81 30 81 24 81 24 81 26 28 2B 2D 26 81 26 81 32 81 2D 81 26 81 26 81 32 81 2D 81 26 81 26 81 32 81 2D 81 26 81 26 81 2D 81 26 81 2B 87 29 87 28 85 29 89 24 81 24 81 30 81 2B 81 24 81 24 81 30 81 2B 81 24 81 24 81 30 81 2B 81 24 81 24 81 26 28 2B 81 21 81 21 81 2D 81 28 81 21 81 21 81 2D 81 28 81 21 81 21 81 2D 81 28 81 21 81 21 81 2D 81 28 81 28 81 28 81 34 81 2F 81 28 81 28 81 34 81 2F 81 26 81 26 81 26 81 2D 81 26 81 21 81 26 28 2B 2D 24 81 24 81 30 81 2B 81 24 81 24 81 30 81 2B 81 61 8F",

   # Channel 5 (empty)
    "2D 81 2D 81 2D 81 61 89 24 81 24 81 30 81 2B 81 24 81 24 81 30 81 2B 81 24 81 24 81 30 81 2B 81 24 81 24 81 30 81 2B 81 21 81 21 81 21 81 1C 81 21 81 21 81 21 81 1C 81 21 81 21 81 21 81 1C 81 21 81 21 81 61 81 1C 81 28 81 28 81 34 81 2F 81 28 81 28 81 34 81 2F 81 26 81 26 81 32 2D 26 81 26 81 21 81 21 81 23 81 24 81 24 81 30 81 2B 81 24 81 24 81 30 81 2B 81 2D 81 2D 81 2D 81 61 89 24 81 24 81 30 81 2B 81 24 81 24 81 30 81 2B 81 24 81 24 81 30 81 2B 81 24 81 24 81 30 81 2B 81 21 81 21 81 21 81 1C 81 21 81 21 81 21 81 1C 81 21 81 21 81 21 81 1C 81 21 81 21 81 61 81 1C 81 28 81 28 81 34 81 2F 81 28 81 28 81 34 81 2F 81 26 81 26 81 32 2D 26 81 26 81 21 81 21 81 23 81 24 81 24 81 30 81 2B 81 24 81 24 81 30 81 2B 81 24 81 24 81 30 81 2B 81 24 81 24 81 30 81 2B 81 29 81 29 81 35 81 24 81 29 81 29 81 35 81 30 81 29 81 29 81 35 81 24 81 29 81 29 81 2B 2D 30 81 24 81 24 81 30 81 2B 81 24 81 24 81 30 81 2B 81 24 81 24 81 30 81 30 81 24 81 24 81 26 28 2B 2D 26 81 26 81 32 81 2D 81 26 81 26 81 32 81 2D 81 26 81 26 81 32 81 2D 81 26 81 26 81 2D 81 26 81 2B 87 29 87 28 85 29 89 24 81 24 81 30 81 2B 81 24 81 24 81 30 81 2B 81 24 81 24 81 30 81 2B 81 24 81 24 81 26 28 2B 81 21 81 21 81 2D 81 28 81 21 81 21 81 2D 81 28 81 21 81 21 81 2D 81 28 81 21 81 21 81 2D 81 28 81 28 81 28 81 34 81 2F 81 28 81 28 81 34 81 2F 81 26 81 26 81 26 81 2D 81 26 81 21 81 26 28 2B 2D 24 81 24 81 30 81 2B 81 24 81 24 81 30 81 2B 81 61 8F",

   # Channel 6 (Drums)
    "15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 15 81 05 81 19 81 05 81 20 8F ",

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
                print(f"Channel {ch}: 70 command - Parameter={volume:02X} (Volume inverted to {inverted_volume})")

                if ch < len(channel_volumes):
                    channel_volumes[ch] = inverted_volume
                midi_channel = 6 if ch == 6 else ch
                track.append(Message('control_change', control=7, value=inverted_volume, channel=midi_channel, time=time_accum))
                
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
                midi_channel = 6 if ch == 6 else ch
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
