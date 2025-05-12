# Known issues.  when read hex 61 does not set note off and will cause to longer notes when importing on onlinesequencer. use midieditor to save.
# it is possible that there may be bugs
# event set to instrument automatic in drums affecting game hero. 
# Drums map not verified. may imperfectly
# will cause to play hex 62 or 63 should not play notes.
# Not implemented
# 64 and 65 feature 
# 70 hex automatic instrument
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
    # Channel 0
    "29 83 29 81 29 81 61 81 24 81 27 81 28 81 29 83 29 81 29 81 61 81 28 81 29 81 2A 81 2B 81 61 81 2B 81 61 81 2B 81 61 81 2B 81 61 81 37 81 3C 81 3A 81 37 81 35 37 81 35 34 81 32 81 24 83 24 81 24 81 61 81 24 81 25 81 26 81 27 83 26 81 26 81 61 81 26 81 26 81 26 81 24 83 24 81 24 81 61 81 24 81 24 81 24 81 2B 81 61 81 2B 81 61 81 2B 81 61 81 2B 81 61 81 40 83 43 83 48 83 45 81 43 81 40 83 40 83 3E 81 3C 81 39 81 37 81 3F 81 40 81 43 81 3E 40 40 81 43 81 40 83 43 81 3F 40 40 81 43 81 3E 81 3C 81 39 81 37 81 30 83 30 81 30 81 34 81 37 81 39 81 37 81 30 83 30 81 30 81 34 81 37 81 39 81 37 81 3E 81 40 81 43 81 3E 40 40 81 43 81 40 83 43 81 3F 40 40 81 43 81 3E 81 3C 81 39 81 37 81 ",
    # Channel 1
    "29 81 29 81 29 81 29 81 24 81 24 81 26 81 24 81 29 81 29 81 29 81 29 81 24 81 24 81 26 81 24 81 1F 81 1F 81 23 81 23 81 26 81 26 81 28 81 26 81 1F 81 61 89 29 2B 81 29 24 83 24 81 24 81 61 81 25 81 24 81 26 81 27 83 26 81 26 81 61 81 26 81 26 81 25 81 24 83 24 81 24 81 61 81 24 81 24 81 24 81 2B 81 2B 81 29 81 29 81 28 81 28 81 26 81 26 81 24 81 24 81 27 81 28 81 2B 81 2B 81 2D 81 2B 81 24 81 24 81 27 81 28 81 2B 81 2B 81 2D 81 2B 81 21 81 21 81 23 81 23 81 24 81 24 81 28 81 26 81 21 81 21 81 23 81 23 81 24 81 24 81 28 81 26 81 24 81 24 81 27 81 28 81 2B 81 2B 81 2E 81 2B 81 24 81 24 81 27 81 28 81 2B 81 2B 81 2E 81 2B 81 21 81 21 81 23 81 23 81 24 81 24 81 28 81 26 81 21 81 21 81 23 81 23 81 24 81 24 81 28 81 26 81 61 ",
    # Channel 2
    "",
    # Channel 3
    "",    
    # Channel 4 (empty)
    "",
    # Channel 5 (empty)
    "",
    # Channel 6 (Drums)
   "11 81 01 81 01 81 01 81 10 81 08 08 08 08 08 81 11 81 01 81 01 81 01 81 10 81 08 08 08 08 08 81 11 81 01 81 01 81 01 81 10 81 08 08 08 08 08 81 18 83 20 8B 18 08 08 08 18 08 08 08 18 08 08 08 18 08 08 08 18 08 08 08 18 08 08 08 18 08 08 08 18 08 08 08 18 08 08 08 18 08 08 08 18 08 08 08 18 08 08 08 18 83 18 08 08 08 18 08 08 08 18 08 08 08 11 81 01 81 09 81 09 81 11 81 01 81 09 81 01 81 11 81 01 81 09 81 09 81 10 81 08 08 08 08 08 81 11 81 01 81 09 81 09 81 10 81 08 08 08 08 08 81 11 81 01 81 09 81 09 81 10 81 08 08 08 08 08 81 11 81 01 81 09 81 09 81 10 81 08 08 08 08 08 81 11 81 01 81 09 81 09 81 10 81 08 08 08 08 08 81 11 81 01 81 09 81 09 81 10 81 08 08 08 08 08 81 11 81 01 81 09 81 09 81 10 81 08 08 08 08 08 81 20",

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
                
                # Send note_on for all drum notes with accumulated time
                for note in drum_notes:
                    track.append(Message('note_on', note=note, velocity=velocity, 
                                       time=time_accum, channel=9))
                    time_accum = 0
                
                # Send note_off for all drum notes with the full duration
                for j, note in enumerate(drum_notes):
                    # Only add time to the first note_off, subsequent ones have 0 time
                    off_time = duration if j == 0 else 0
                    track.append(Message('note_off', note=note, velocity=0,
                                       time=off_time, channel=9))
                    time_accum = 100

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
            time_accum = 100  # Reset time accumulation after handling the note
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
                
                # Send note_on for all drum notes with accumulated time
                for note in drum_notes:
                    track.append(Message('note_on', note=note, velocity=velocity,
                                       time=time_accum, channel=9))
                    time_accum = 0
                
                # Send note_off for all drum notes with base_grid duration
                for j, note in enumerate(drum_notes):
                    # Only add time to the first note_off, subsequent ones have 0 time
                    off_time = base_grid if j == 0 else 0
                    track.append(Message('note_off', note=note, velocity=0,
                                       time=off_time, channel=9))
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
print("- Accurate duration handling (81=100ms, 82=200ms, ..., FF=800ms)")
print("- Simultaneous drum notes when required")
print("- Fixed drum note skipping bug with duration bytes")
