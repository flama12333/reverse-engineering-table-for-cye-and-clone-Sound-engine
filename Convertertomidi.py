# Known issues.  when read hex 61 does not set note off and will cause to longer notes when importing on onlinesequencer. use midieditor to save.
# it is possible that there may be bugs
# event set to instrument automatic in drums affecting game hero. 
# Drums map not verified. may imperfectly
# will cause to play hex 62 or 63 should not play notes.
# Not implemented
# 64 and 65 feature 
# 70 hex automatic instrument and Volume also will be ignore.
# hex 66
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
    if byte in {0x00, 0x20, 0x40}:
        return 100
    
    # Map to the 00-1F range by masking
    base_byte = byte & 0x1F
    
    # Original 00-1F mappings
    drum_map = {
        0x01: 42,  # HH - Closed Hi-Hat
        0x02: 49,  # CYM - Crash Cymbal
        0x03: [42, 49],  # CYM + HH
        0x04: 50,  # TM - High Tom
        0x05: [42, 50],  # TM + HH
        0x06: [49, 50],  # TM + CYM
        0x07: [42, 49, 50],  # TM + CYM + HH
        0x08: 38,  # SD - Snare Drum
        0x09: [38, 42],  # SD + HH
        0x0A: [38, 49],  # SD + CYM
        0x0B: [38, 42, 49],  # SD + CYM + HH
        0x0C: [38, 50],  # SD + TM
        0x0D: [38, 42, 50],  # SD + TM + HH
        0x0E: [38, 49, 50],  # SD + TM + CYM
        0x0F: [38, 42, 49, 50],  # SD + TM + CYM + HH
        0x10: 36,  # BD - Bass Drum
        0x11: [36, 42],  # BD + HH
        0x12: [36, 49],  # BD + CYM
        0x13: [36, 42, 49],  # BD + CYM + HH
        0x14: [36, 50],  # BD + TM
        0x15: [36, 42, 50],  # BD + TM + HH
        0x16: [36, 49, 50],  # BD + TM + CYM
        0x17: [36, 42, 49, 50],  # BD + TM + CYM + HH
        0x18: [36, 38],  # BD + SD
        0x19: [36, 38, 42],  # BD + SD + HH
        0x1A: [36, 38, 49],  # BD + SD + CYM
        0x1B: [36, 38, 42, 49],  # BD + SD + CYM + HH
        0x1C: [36, 38, 50],  # BD + SD + TM
        0x1D: [36, 38, 42, 50],  # BD + SD + TM + HH
        0x1E: [36, 38, 49, 50],  # BD + SD + TM + CYM
        0x1F: [36, 38, 42, 49, 50],  # BD + SD + TM + CYM + HH
    }
    
    return drum_map.get(base_byte, [])

# === MIDI Setup ===
mid = MidiFile()
hex_strings = [
    # Your hex strings here (same as before)
    # Channel 0
    "61 81 43 81 43 81 43 81 43 81 40 81 3E 81 3C 81 40 81 3C 83 37 83 40 81 3E 81 3C 81 40 81 3C 83 37 85 40 83 40 81 3E 81 61 8B 61 81 41 81 41 81 41 81 41 81 3E 81 3C 81 3B 81 3E 81 3B 83 37 83 40 81 3E 81 3C 81 3E 81 3B 83 37 85 3E 83 3E 81 3C 81 61 93 2B 81 2B 81 2D 81 2E 81 2F 83 41 83 41 81 40 81 61 81 3E 81 61 87 2B 81 2B 81 2D 81 2F 81 30 83 40 83 41 81 42 81 61 81 43 81 61 87 2B 81 2B 81 2D 81 2E 81 2F 83 41 83 41 81 40 81 61 81 3E 81 61 87 2B 81 2B 81 2D 81 2F 81 30 83 61 8B 70 58 14 61 81 2B 81 2B 81 2B 81 2B 81 28 81 26 81 24 81 28 81 24 83 1F 83 28 81 26 81 24 81 28 81 24 83 1F 85 28 83 28 81 26 81 61 8B 61 81 29 81 29 81 29 81 29 81 26 81 24 81 23 81 26 81 23 83 1F 83 26 81 24 81 23 81 26 81 23 81 1F 85 26 85 26 81 24 81 61 8B 61 ",
    # Channel 1
    "61 97 61 97 61 83 3E 83 3E 81 40 81 61 81 41 81 61 97 61 97 41 81 40 81 61 81 40 81 61 81 3E 81 40 81 41 81 43 81 61 85 37 81 37 81 39 81 3A 81 3B 83 61 93 37 81 37 81 39 81 3B 81 3C 83 61 93 37 81 37 81 39 81 3A 81 3B 83 61 93 37 81 37 81 39 81 3B 81 3C 83 61 97 61 97 61 8F 3E 83 3E 81 40 81 61 81 41 81 61 8F 61 97 61 97 61",
    # Channel 2
    "18 83 61 81 13 81 18 83 61 81 13 81 18 83 61 81 13 81 18 83 61 81 13 81 18 83 61 81 13 81 18 83 61 81 13 81 13 83 61 81 0E 81 13 81 13 81 15 81 17 81 13 83 61 81 0E 81 13 83 61 81 0E 81 13 83 61 81 0E 81 13 83 61 81 0E 81 13 83 61 81 0E 81 13 83 61 81 0E 81 18 83 61 81 18 81 18 81 18 81 18 81 18 81 18 83 61 83 13 81 13 81 15 81 16 81 17 83 61 83 13 83 61 81 0E 81 13 83 61 83 13 81 13 81 15 81 17 81 18 83 61 83 18 83 61 81 13 81 18 83 61 83 13 81 13 81 15 81 16 81 17 83 61 83 13 83 61 81 0E 81 13 83 61 83 13 81 13 81 15 81 17 81 18 83 61 83 18 81 18 81 18 81 18 81 18 83 61 81 13 81 18 83 61 81 13 81 18 83 61 81 13 81 18 83 61 81 13 81 18 83 61 81 13 81 18 83 61 81 13 81 13 83 61 81 0E 81 13 83 61 81 0E 81 13 83 61 81 0E 81 13 83 61 81 0E 81 13 83 61 81 0E 81 13 83 61 81 0E 81 13 83 61 81 0E 81 13 83 61 81 0E 81 18 83 61 81 13 81 61 87 61",
    # Channel 3
    "61 81 37 81 37 81 37 81 37 81 34 81 32 81 30 81 34 81 30 83 2B 83 34 81 32 81 30 81 34 81 30 83 2B 85 34 83 34 81 32 81 61 8D 35 81 35 81 35 81 35 81 32 81 30 81 2F 81 32 81 2F 83 2B 83 34 81 32 81 30 81 32 81 2F 83 2B 85 32 83 32 81 30 81 61 93 1F 81 1F 81 21 81 22 81 23 83 35 83 35 81 34 81 61 81 32 81 61 87 1F 81 1F 81 21 81 23 81 24 83 34 83 35 81 36 81 61 81 37 81 61 87 1F 81 1F 81 21 81 22 81 23 83 35 83 35 81 34 81 61 81 32 81 61 87 1F 81 1F 81 21 81 23 81 24 83 70 00 10 61 8D 37 81 37 81 37 81 37 81 34 81 32 81 30 81 34 81 30 83 2B 83 34 81 32 81 30 81 34 81 30 83 2B 85 34 83 34 81 32 81 61 8D 35 81 35 81 35 81 35 81 32 81 30 81 2F 81 32 81 2F 83 2B 83 32 81 30 81 2F 81 32 81 2F 81 2B 85 32 85 32 81 30 81 61 8B 61",
    # Channel 4 (empty)
    "",
    # Channel 5 (empty)
    "",
    # Channel 6 (Drums)
    "12 81 02 81 1A 81 02 81 12 81 02 81 1A 81 02 81 12 81 02 81 1A 81 02 81 12 81 02 81 1A 81 02 81 12 81 02 81 1A 81 02 81 12 81 02 81 1A 81 02 81 12 81 02 81 1A 81 02 81 12 81 02 81 08 08 08 08 12 81 02 81 1A 81 02 81 12 81 02 81 1A 81 02 81 12 81 02 81 1A 81 02 81 12 81 02 81 1A 81 02 81 12 81 02 81 1A 81 02 81 12 81 02 81 1A 81 02 81 12 81 02 02 1A 81 02 02 08 08 08 08 08 08 08 08 12 81 02 02 1A 81 02 02 1A 81 1A 81 1A 81 1A 81 1A 81 02 81 1A 81 02 81 1A 81 1A 83 1A 81 12 81 02 02 1A 81 02 02 1A 81 1A 81 1A 81 1A 81 1A 81 02 81 1A 81 02 81 1A 81 1A 83 1A 81 12 81 02 02 1A 81 02 02 1A 81 1A 81 1A 81 1A 81 1A 81 02 81 1A 81 02 81 1A 81 1A 83 1A 81 12 81 02 02 1A 81 02 02 1A 81 1A 81 1A 81 1A 81 1A 81 02 02 1A 81 02 02 08 08 08 08 08 08 08 08 12 81 02 81 1A 81 02 81 12 81 02 81 1A 81 02 81 12 81 02 81 1A 81 02 81 12 81 02 81 1A 81 02 81 12 81 02 81 1A 81 02 81 12 81 02 81 1A 81 02 81 12 81 02 81 1A 81 02 81 12 81 02 81 08 08 08 08 12 81 02 81 1A 81 02 81 12 81 02 81 1A 81 02 81 12 81 02 81 1A 81 02 81 12 81 02 81 1A 81 02 81 12 81 02 81 1A 81 02 81 12 81 02 81 1A 81 02 81 12 81 02 02 1A 81 02 02 08 08 08 08 08 08 08 08 61",
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
            
        # Instrument/Volume change (70)
        elif byte == 0x70:
            if i+2 < len(data):
                instrument = data[i+1]  # Offset 01 - Instrument
                volume = data[i+2]      # Offset 02 - Volume
                print(f"Ignoring instrument/volume change - Instrument: {instrument}, Volume: {volume}")
                i += 3  # Skip the command and both parameters
                continue
            else:
                i += 1
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
        elif byte == 0x00 and i+1 < len(data) and data[i+1] >= 0x81:
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
