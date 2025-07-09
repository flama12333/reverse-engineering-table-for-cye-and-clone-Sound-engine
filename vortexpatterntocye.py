   # Experimental code to convert pattern save using Vortex tracker to custom to make playable in ym2413 or ym3812
   # Missing Feature:
   # Samples 1-9 A-B
   # Envelope Type 1-F
   # Ornament 0-F
   # Volume 0-F
   # Envelope Generator Period 0-FFFF and Envelope Type 1-E
   # Noise Generator Base Period 0-1f
   # Unsuported feature.
   # noise. might be required to convert to simulate drums noise
import re

def note_to_hex(note_str):
    if note_str == '---':
        return 0x81  # Standard rest value
    elif note_str == '--R':
        return 0x61  # Special rest value
    elif note_str.startswith('--'):
        return 0x81  # Default for other -- patterns
    
    # Parse note string (e.g., "C#6", "Bb3", "D-2")
    match = re.match(r'([A-Ga-g])([#b]?)-?([0-9])', note_str)
    if not match:
        return 0x81  # Invalid format → 81
    
    note = match.group(1).upper()
    accidental = match.group(2)
    octave = int(match.group(3))
    
    # Convert flats to sharps
    if accidental == 'b':
        if note == 'C': note = 'B'; octave -= 1
        elif note == 'D': note = 'C'; accidental = '#'
        elif note == 'E': note = 'D'; accidental = '#'
        elif note == 'F': note = 'E'
        elif note == 'G': note = 'F'; accidental = '#'
        elif note == 'A': note = 'G'; accidental = '#'
        elif note == 'B': note = 'A'; accidental = '#'
    
    # Calculate MIDI note number (C-1 = 0, B-8 = 119)
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    note_name = note + (accidental if accidental else '')
    
    if note_name not in notes:
        return 0x81  # Invalid note → 81
    
    midi_note = (octave + 1) * 12 + notes.index(note_name) - 12
    
    # Convert to hex 01-5F (C-1=01 to B-8=5F)
    if midi_note < 0:
        return 0x01  # Clamp to minimum
    elif midi_note > 119:
        return 0x5F  # Clamp to maximum
    return midi_note + 1

def process_pattern_file(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    ch1 = []
    ch2 = []
    ch3 = []
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('[Pattern]') or line == 'HexNoise':
            continue
            
        # Extract from columns 9, 23, 37 (1-based)
        ch1_note = line[8:12].strip()
        ch2_note = line[22:26].strip()
        ch3_note = line[36:40].strip()
        
        # Convert each note
        ch1.append(f"{note_to_hex(ch1_note):02x}")
        ch2.append(f"{note_to_hex(ch2_note):02x}")
        ch3.append(f"{note_to_hex(ch3_note):02x}")
    
    # Write to single output file with headers
    with open(output_file, 'w') as f:
        f.write("CH 1\n")
        f.write("\n".join(ch1) + "\n\n")
        
        f.write("CH 2\n")
        f.write("\n".join(ch2) + "\n\n")
        
        f.write("CH 3\n")
        f.write("\n".join(ch3) + "\n")

if __name__ == '__main__':
    input_filename = 'input.txt'
    output_filename = 'output_notes.txt'
    process_pattern_file(input_filename, output_filename)
    print(f"Conversion complete. Output saved to {output_filename}")
