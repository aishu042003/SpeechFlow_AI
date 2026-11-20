from datetime import datetime

def create_report(data):
    lines = [
        "SPEECHFLOW AI - ANALYSIS REPORT",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"File: {data.get('filename', '')}",
        f"Language: {data.get('language', 'unknown')}",
        "",
        "SUMMARY",
        data.get("summary", ""),
        "",
        "CONVERSATION INSIGHTS",
        str(data.get("conversation", {})),
        "",
        "TEXT TONE ESTIMATE",
        str(data.get("emotion", {})),
        "",
        "TRANSCRIPT",
        data.get("transcript", ""),
    ]

    if data.get("translation"):
        lines.extend(["", "TRANSLATION", data["translation"]])
    if data.get("speakers"):
        lines.extend(["", "SPEAKER SEGMENTS", str(data["speakers"])])

    return "\n".join(lines)