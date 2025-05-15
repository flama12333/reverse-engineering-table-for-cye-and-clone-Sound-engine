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
octave_shifts = [1, 1, 1, 1, 1, 0]
base_grid = 100  # 100ms per grid unit

# === Volume Configuration ===  # Default
channel_volumes = [127, 127, 127, 127, 127, 127, 127]  # Channels 0-7

# Example hex input: each value from 0x00 to 0x7F
hex_volume_input = [0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x01]

# Instrument configuration
channel_instruments = [000, 000, 000, 000, 000, 000]  # Default instruments for channels 0-6 (0 = Acoustic Grand Piano)
hex_instrument_input = [0x3, 0x07, 0x27, 0x00, 0x00, 0x00]  # Example instrument input (1-based)


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
     "40 83 3C 81 39 81 40 83 3C 81 39 81 3E 81 3E 81 3C 81 3E 81 3E 83 3E 83 40 83 3C 81 39 81 40 83 3C 81 39 81 3E 81 3E 81 40 81 40 81 3E 83 61 83 40 83 3C 81 39 81 40 83 3C 81 39 81 3E 81 3E 81 3C 81 3E 81 3E 83 3E 83 40 83 3C 81 39 81 40 83 3C 81 39 81 3E 81 3E 81 40 81 40 81 3E 83 61 83 39 81 3C 81 40 81 41 81 40 81 3C 83 39 81 37 8B 61 83 39 81 3C 81 40 81 41 81 40 81 3C 83 39 81 37 8B 61 83 39 81 3C 81 40 81 41 81 40 81 3C 83 39 81 37 8B 61 83 39 81 3C 81 40 81 41 81 40 81 3C 83 39 81 37 8B 61 83 40 83 3C 81 39 81 40 83 3C 81 39 81 3E 83 3C 81 3E 85 3E 83 40 83 3C 81 39 81 40 83 3C 81 39 81 3E 81 3E 81 40 81 40 81 3E 87 40 83 3C 81 39 81 40 83 3C 81 39 81 3E 83 3C 81 3E 85 3E 83 40 83 3C 81 39 81 40 83 3C 81 39 81 3E 81 3E 81 40 81 40 81 3E 87 34 81 30 83 2D 87 2D 81 32 81 2F 83 2B 89 29 81 2D 83 30 83 32 85 2F 81 2B 83 29 89 34 81 30 83 2D 89 32 81 2F 83 2B 89 29 81 2D 83 30 83 32 83 61 81 34 81 35 83 32 89 34 81 30 83 2D 89 61 81 32 81 2F 81 2B 89 29 81 2D 83 30 83 32 85 2F 81 2B 83 29 89 61 81 34 81 30 81 2D 89 61 81 32 81 2F 81 2B 89 29 81 2D 83 30 83 32 85 34 81 35 83 32 89 61 8F 61 97 61 97 ",
    # Channel 1
    "61 97 61 97 61 97 61 97 61 98 61 98 37 2F 32 81 37 81 32 81 2F 81 2B 81 2F 81 61 98 61 98 37 2F 32 81 37 81 32 81 2F 81 2B 81 2F 81 61 8F 61 91 39 81 61 81 3C 81 61 81 40 81 61 81 3C 81 61 81 3E 81 61 81 37 81 3C 81 3B 81 39 81 37 81 61 81 39 81 61 81 3C 81 61 81 40 81 61 81 3C 81 61 81 3E 81 61 81 37 81 3C 81 3B 81 39 81 37 81 61 81 39 81 61 81 3C 81 61 81 40 81 61 81 3C 81 61 81 3E 81 61 81 37 81 3C 81 3B 81 39 81 37 81 61 81 39 81 61 81 3C 81 61 81 40 81 61 81 3C 81 61 81 3E 81 61 81 37 81 3C 81 3B 81 39 81 37 81 61 97 61 97 61 97 61 97 61 97 61 97 61 97 61 97 61 97 61 97 61 97 61 97 61 8F 61 8F 61",
    # Channel 2
    "1D 85 1D 81 1D 85 1D 81 1F 85 1F 81 1F 81 1A 81 1D 81 1F 81 1D 85 1D 81 1D 85 1D 81 1F 85 1F 81 23 81 26 81 29 81 2B 81 1D 85 1D 81 1D 85 1D 81 1F 85 1F 81 1F 81 1A 81 1D 81 1F 81 1D 85 1D 81 1D 85 1D 81 1F 85 1F 81 23 81 26 81 29 81 2B 81 1D 85 1D 81 1D 85 1D 81 1F 85 1F 81 23 81 26 81 29 81 2B 81 1D 85 1D 81 1D 85 1D 81 1F 85 1F 81 23 81 26 81 29 81 2B 81 1D 85 1D 81 1D 85 1D 81 1F 85 1F 81 23 81 26 81 29 81 2B 81 1D 85 1D 81 1D 85 1D 81 1F 85 1F 81 23 81 26 81 29 81 2B 81 1D 85 1D 81 1D 85 1D 81 1F 85 1F 81 24 81 26 81 29 81 2B 81 1D 85 1D 81 1D 85 1D 81 1F 85 1F 81 23 81 26 81 29 81 2B 81 1D 85 1D 81 1D 85 1D 81 1F 85 1F 81 24 81 26 81 29 81 2B 81 1D 85 1D 81 1D 85 1D 81 1F 85 1F 81 23 81 26 81 29 81 2B 81 1D 85 1D 81 1D 85 1D 81 1F 85 1F 81 23 81 26 81 29 81 2B 81 1D 85 1D 81 1D 85 1D 81 1F 85 1F 81 23 81 26 81 29 81 2B 81 1D 85 1D 81 1D 85 1D 81 1F 85 1F 81 23 81 26 81 29 81 2B 81 1D 85 1D 81 1D 85 1D 81 1F 85 1F 81 23 81 26 81 29 81 2B 81 1D 85 1D 81 1D 85 1D 81 1F 85 1F 81 23 81 26 81 29 81 2B 81 1D 85 1D 81 1D 85 1D 81 1F 85 1F 81 23 81 26 81 29 81 2B 81 1D 85 1D 81 1D 85 1D 81 1F 85 1F 81 23 81 26 81 29 81 2B 81 1D 85 1D 81 1D 85 1D 81 1F 85 1F 81 23 81 26 81 29 81 2B 81 21 83 61 81 21 81 61 81 21 81 61 81 1F 81 21 83 1F 83 21 83 61 83 21 83 61 81 21 81 61 81 21 81 61 81 1F 81 21 83 1D 83 1F 87 61",
    # Channel 3
    "30 83 61 81 30 81 30 83 61 81 30 81 32 81 32 81 32 81 32 81 61 83 32 83 30 83 30 81 30 81 30 83 30 81 30 81 32 81 32 81 32 81 32 81 32 83 61 83 30 83 61 81 30 81 30 83 61 81 30 81 32 81 32 81 32 81 32 81 61 83 32 83 30 83 30 81 30 81 30 83 30 81 30 81 32 81 32 81 32 81 32 81 32 83 61 87 30 81 30 81 61 83 30 81 30 81 61 83 32 81 32 81 61 83 32 81 32 81 61 83 30 81 30 81 61 83 30 81 30 81 61 83 32 81 32 81 32 83 61 87 30 81 30 81 61 83 30 81 30 81 61 83 32 81 32 81 61 83 32 81 32 81 61 83 30 81 30 81 61 83 30 81 30 81 61 83 32 81 32 81 32 83 61 83 30 83 61 81 30 81 30 83 61 81 30 81 61 81 32 81 32 81 32 81 61 83 32 83 30 83 61 81 30 81 30 83 61 81 30 81 61 81 32 81 32 81 32 81 61 83 32 83 30 83 61 81 30 81 30 83 61 81 30 81 61 81 32 81 32 81 32 81 61 83 32 83 30 83 61 81 30 81 30 83 61 81 30 81 61 81 32 81 32 81 32 81 61 83 32 83 30 81 30 81 61 81 30 81 61 83 30 81 30 81 32 81 32 81 61 81 32 81 61 83 32 81 32 81 30 81 30 81 61 81 30 81 61 83 30 81 30 81 32 81 32 81 61 81 32 81 61 83 32 81 32 81 30 81 30 81 61 81 30 81 61 83 30 81 30 81 32 81 32 81 61 81 32 81 61 83 32 81 32 81 30 81 30 81 61 81 30 81 61 83 30 81 30 81 32 81 32 81 61 81 32 81 61 83 32 81 32 81 30 81 30 83 30 85 61 83 32 81 32 83 32 85 61 83 30 81 30 83 30 85 61 83 32 81 32 83 32 85 61 83 30 81 30 83 30 85 61 83 32 81 32 83 32 85 61 83 30 81 30 83 30 85 61 83 32 81 32 83 32 85 61 83 34 83 61 81 34 81 61 81 34 81 61 81 32 81 34 83 32 83 34 83 61 83 34 83 61 81 34 81 61 81 34 81 61 81 32 81 34 83 30 83 32 87 61",
    # Channel 4 (empty)
    "",
    # Channel 5 (empty)
    "",
    # Channel 6 (Drums)
   "12 81 02 81 12 81 0F 81 12 81 02 81 12 81 0F 81 12 81 02 81 12 81 0F 81 12 81 02 81 12 81 0F 81 12 81 02 81 12 81 0F 81 12 81 02 81 12 81 0F 81 12 81 02 81 12 81 0F 81 12 81 02 81 12 81 0F 81 12 81 02 81 12 81 0F 81 12 81 02 81 12 81 0F 81 12 81 02 81 12 81 0F 81 12 81 02 81 12 81 0F 81 12 81 02 81 12 81 0F 81 12 81 02 81 12 81 0F 81 12 81 02 81 12 81 0F 81 12 81 02 81 12 81 0F 81 12 81 02 81 1F 81 02 81 12 81 02 81 1F 81 02 81 12 81 02 81 1F 81 02 81 12 81 02 81 1F 81 02 81 12 81 02 81 1F 81 02 81 12 81 02 81 1F 81 02 81 1F 83 1F 81 1F 81 1F 87 12 81 02 81 1F 81 02 81 12 81 02 81 1F 81 02 81 12 81 02 81 1F 81 02 81 12 81 02 81 1F 81 02 81 12 81 02 81 1F 81 02 81 12 81 02 81 1F 81 02 81 1F 83 1F 81 1F 81 1F 87 1A 81 02 81 1A 81 02 81 1A 81 1A 81 1A 81 02 81 1A 81 02 81 1A 81 02 81 1A 81 1A 81 1A 81 02 81 1A 81 02 81 1A 81 02 81 1A 81 1A 81 1A 81 02 81 1A 81 02 81 1A 81 02 81 08 08 08 08 08 08 08 08 1A 81 02 81 1A 81 02 81 1A 81 1A 81 1A 81 02 81 1A 81 02 81 1A 81 02 81 1A 81 1A 81 1A 81 02 81 1A 81 02 81 1A 81 02 81 1A 81 1A 81 1A 81 02 81 1A 81 02 81 1A 81 02 81 08 08 08 08 08 08 08 08 12 81 02 81 1F 81 02 81 12 81 02 81 1F 81 02 81 12 81 02 81 1F 81 02 81 12 81 02 81 1F 81 02 81 12 81 02 81 1F 81 02 81 12 81 02 81 1F 81 02 81 12 81 02 81 1F 81 02 81 12 81 02 81 1F 81 02 81 12 81 02 81 1F 81 02 81 12 81 02 81 1F 81 02 81 12 81 02 81 1F 81 02 81 12 81 02 81 1F 81 02 81 12 81 02 81 1F 81 02 81 12 81 02 81 1F 81 02 81 12 81 02 81 1F 81 02 81 12 81 02 81 1F 81 02 81 1A 81 02 02 1A 81 02 02 1A 81 02 02 1A 81 02 02 1A 81 02 02 1A 81 02 02 1A 81 02 02 1A 81 02 02 1A 81 02 02 1A 81 02 02 1A 81 02 02 1A 81 02 02 1A 81 02 02 1A 81 02 02 1A 81 02 02 1A 81 02 02 1A 81 02 02 1A 81 02 02 1A 81 02 02 1A 81 02 02 1A 81 02 02 1A 81 02 02 1A 81 02 02 1A 81 02 02 1A 81 02 02 1A 81 02 02 1A 81 02 02 1A 81 02 02 1A 81 02 02 1A 81 02 02 1A 81 02 02 1A 81 02 02 1A 81 02 02 1A 81 02 02 1A 81 02 02 1A 81 02 02 1A 81 02 02 1A 81 02 02 1A 81 02 02 0A 0A 0A 0A 1A 81 02 02 1A 81 02 02 1A 81 02 02 1A 81 02 02 1A 81 02 02 1A 81 02 02 1A 81 02 02 0A 0A 0A 0A 61",

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
