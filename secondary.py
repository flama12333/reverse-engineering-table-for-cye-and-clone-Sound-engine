import mido
from mido import MidiFile, MidiTrack, Message, MetaMessage, bpm2tempo

# === Configuration ===
ignore_end_signal = True
bpm = 120
velocity = 80
tempo = bpm2tempo(bpm)

# Optional octave shift (-2 = two octaves down, +1 = one octave up, etc.)
octave_shift = 0  # Set to desired value

# === MIDI Setup ===
mid = MidiFile()
hex_strings = [
    # Channel 0 - Fill with your actual hex music data
    "66 00 00 00 00 00 0C 70 27 02 34 81 34 81 33 81 34 81 35 81 36 81 37 81 38 81",
    "", "", "", "", "",  # Channels 1–6
]

# === Note Mapper: From hex to MIDI note ===
def map_hex_byte_to_midi_note(byte, octave_shift=0):
    if 0x00 <= byte <= 0x66:  # Extended to include up to 0x66 (decimal 102)
        return byte + (octave_shift * 12)
    return None

# === MIDI Note Range (0x00 to 0x66 = decimal 0 to 102) ===
valid_notes = list(range(0x00, 0x67))  # Inclusive of 0x66

# === Process Each Channel ===
for ch, hex_str in enumerate(hex_strings):
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(MetaMessage('set_tempo', tempo=tempo, time=0))

    data = [int(x, 16) for x in hex_str.split()]
    i = 0
    time_accum = 0

    while i < len(data):
        byte = data[i]

        # End signal
        if byte in [0x62, 0x63]:
            if ignore_end_signal:
                i += 1
                continue
            else:
                break

        # Decode start (64 or 65)
        elif byte in [0x64, 0x65]:
            i += 4
            continue

        # Octave change (0x66)
        elif byte == 0x66:
            i += 7
            continue

        # Instrument/volume change (0x70)
        elif byte == 0x70:
            i += 3
            continue

        # Time marker
        elif byte == 0x61:
            time_accum += 100
            i += 1

        # Delay bytes (>= 0x80)
        elif 0x80 <= byte <= 0xFF:
            time_accum += (byte - 0x80) * 100
            i += 1

        # Valid note byte
        elif byte in valid_notes:
            midi_note = map_hex_byte_to_midi_note(byte, octave_shift)
            if midi_note is not None and 0 <= midi_note <= 127:
                track.append(Message('note_on', note=midi_note, velocity=velocity, time=time_accum, channel=ch))
                track.append(Message('note_off', note=midi_note, velocity=velocity, time=100, channel=ch))
            else:
                print(f"⚠️ Skipped invalid MIDI note: {midi_note}")
            time_accum = 0
            i += 1

        # Unknown byte
        else:
            print(f"❓ Unknown byte: {hex(byte)} at index {i}, skipping...")
            i += 1

# === Save MIDI ===
mid.save('hex_to_midi_octave_configurable.mid')
print("✅ Saved as 'hex_to_midi_octave_configurable.mid'")
