import re

def parse_srt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    pattern = re.compile(
        r"(\d+)\s*\n" +
        r"(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})\s*\n" +
        r"((?:.*(?:\n|$))+?)\n*(?=\d+\s*\n|$)",
        re.MULTILINE
    )
    
    subtitles = []
    for match in pattern.finditer(content):
        index, start, end, text = match.groups()
        subtitles.append({
            "index": int(index),
            "start": start.strip(),
            "end": end.strip(),
            "text": text.strip().replace('\n', ' ')
        })
    return subtitles

def merge_subtitles_by_period(subtitles):
    """
    인접한 자막들을 결합하는데, 현재 자막의 텍스트가 '.'로 끝나면 결합을 멈춥니다.
    """
    if not subtitles:
        return []
    
    merged = []
    current = subtitles[0].copy()
    
    for next_item in subtitles[1:]:
        # 현재 결합된 자막의 텍스트가 마침표로 끝나는지 확인
        if current["text"].rstrip().endswith('.'):
            merged.append(current)
            current = next_item.copy()
        else:
            # 마침표로 끝나지 않으면 현재 텍스트와 합치고 종료 시간 업데이트
            current["text"] += " " + next_item["text"]
            current["end"] = next_item["end"]
    
    merged.append(current)
    return merged

def write_srt(subtitles, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        for i, sub in enumerate(subtitles, start=1):
            f.write(f"{i}\n")
            f.write(f"{sub['start']} --> {sub['end']}\n")
            f.write(f"{sub['text']}\n\n")

if __name__ == "__main__":
    input_file = "input.srt"   # 원본 SRT 파일 경로
    output_file = "merged.srt" # 결과 SRT 파일 경로
    
    # SRT 파일 파싱
    subs = parse_srt(input_file)
    # 마침표를 기준으로 인접 자막 병합
    merged_subs = merge_subtitles_by_period(subs)
    # 병합된 자막 파일 저장
    write_srt(merged_subs, output_file)
    
    print(f"병합된 자막 파일이 '{output_file}'에 저장되었습니다.")
