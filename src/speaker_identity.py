def assign_speaker_labels(diarization_rows):
    """Map backend speaker IDs to stable display labels."""
    mapping = {}
    labeled_rows = []

    for row in diarization_rows:
        speaker_id = row.get("speaker", "UNKNOWN")
        if speaker_id not in mapping:
            mapping[speaker_id] = f"Speaker {len(mapping) + 1}"
        labeled_rows.append({**row, "speaker_label": mapping[speaker_id]})

    return labeled_rows