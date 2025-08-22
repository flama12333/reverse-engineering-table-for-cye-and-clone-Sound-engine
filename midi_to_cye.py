import mido
from mido import MidiFile

def midi_to_hex(midi_file_path, output_text_file, ticks_per_beat=480, base_delay=100, note_min=0x00, note_max=0x60):
    """
    Convert MIDI to hex strings with GRID duration handling:
    - Short notes: "3B 3B 3B" (no delay)
    - Notes with duration: "3B 82 3B 82" (81-FF delays)
    - Handles delays >255ms: "FF 82" for 258ms
    - Removes all note-off events
    - MIDI note 12 (C1) maps to hex 00
    - Notes below C1 (B0) or above hex 60 are replaced with 61 and warnings generated
    """
    mid = MidiFile(midi_file_path, ticks_per_beat=ticks_per_beat)
    hex_tracks = []
    warnings = []
    
    # MIDI note 12 (C1) maps to hex 00
    MIDI_C1 = 12
    
    for track_idx, track in enumerate(mid.tracks):
        hex_track = []
        accumulated_time = 0
        track_warnings = []
        
        for msg in track:
            accumulated_time += msg.time
            
            if msg.type == 'note_on' and msg.velocity > 0:
                # Handle accumulated delay (can be >255ms)
                while accumulated_time >= base_delay:
                    delay_units = min(accumulated_time // base_delay, 127)
                    hex_track.append(f"{0x80 + delay_units:02X}")
                    accumulated_time -= delay_units * base_delay
                
                # Convert MIDI note to hex (C1 = 00)
                mapped_note = msg.note - MIDI_C1
                
                # Check if note is within valid hex range (00-60)
                if mapped_note < note_min:
                    # Note below C1 (B0 or lower)
                    hex_track.append("61")
                    track_warnings.append(f"Note {msg.note} (B0 or lower) below min C1 ({MIDI_C1}), replaced with 61")
                elif mapped_note > note_max:
                    # Note above maximum hex 60
                    hex_track.append("61")
                    track_warnings.append(f"Note {msg.note} (would be hex {mapped_note:02X}) exceeds max {note_max:02X}, replaced with 61")
                else:
                    # Valid note in range 00-60
                    hex_track.append(f"{mapped_note:02X}")
                
                accumulated_time = 0
        
        # Handle final delay (can be >255ms)
        while accumulated_time >= base_delay:
            delay_units = min(accumulated_time // base_delay, 127)
            hex_track.append(f"{0x80 + delay_units:02X}")
            accumulated_time -= delay_units * base_delay
        
        hex_tracks.append(' '.join(hex_track))
        
        # Add track warnings to global warnings
        if track_warnings:
            warnings.append(f"Track {track_idx}:")
            warnings.extend(track_warnings)
            warnings.append("")  # Empty line for separation
    
    # Save hex output
    with open(output_text_file, 'w') as f:
        for i, track in enumerate(hex_tracks):
            f.write(f"// Track {i}\n{track}\n\n")
        
        # Append warnings to the file
        if warnings:
            f.write("// WARNINGS:\n")
            for warning in warnings:
                f.write(f"// {warning}\n")
    
    # Print warnings to console
    if warnings:
        print("⚠️  Warnings detected:")
        for warning in warnings:
            if warning:  # Skip empty lines
                print(f"   {warning}")
    
    print(f"✅ MIDI converted with note range checking, saved as '{output_text_file}'")

# Example usage with note range checking (C1 = 00, max = 60):
midi_to_hex('input.mid', 'output_hex_with_range_check.txt', note_min=0x00, note_max=0x60)
