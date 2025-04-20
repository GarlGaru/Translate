from transformers import AutoTokenizer
from sentence_transformers import SentenceTransformer, util

# ① 하나의 Sentence‑Transformers 모델만 사용
sbert      = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
tokenizer  = sbert.tokenizer         # 동일 어휘로 토크나이징

def find_token_subsequence(
    haystack_ids,
    needle_ids,
    start,
    *,
    threshold=0.7,
    min_ratio=0.8,
    max_ratio=2.0,
    step_tokens=4,
):
    """
    동일 시작점에서 길이를 점진적으로 늘리며 코사인 유사도를 확인.
    길이 범위 = [len(needle_ids)*min_ratio, len(needle_ids)*max_ratio]
    """
    need_len   = len(needle_ids)
    min_len    = max(1, int(need_len * min_ratio))
    max_len    = int(need_len * max_ratio)

    needle_emb = sbert.encode(
        tokenizer.decode(needle_ids, skip_special_tokens=True),
        convert_to_tensor=True,
    )

    for i in range(start, len(haystack_ids) - min_len + 1):
        for win_len in range(min_len, max_len + 1, step_tokens):
            if i + win_len > len(haystack_ids):
                break
            win_text = tokenizer.decode(haystack_ids[i : i + win_len], skip_special_tokens=True)
            print(win_text)
            win_emb = sbert.encode(
                win_text,
                convert_to_tensor=True,
            )
            if util.cos_sim(needle_emb, win_emb).item() >= threshold:
                return i, win_len
    return -1, 0


def consume_with_tokenizer(original_sentences, translated, **kwargs):
    # --- 토큰 ID와 문자 오프셋 동시 확보 -------------------
    enc = tokenizer(
        translated,
        add_special_tokens=False,
        return_offsets_mapping=True,
    )
    trans_ids      = enc["input_ids"]
    offsets        = enc["offset_mapping"]   # [(char_start, char_end), ...]
    cursor_token   = 0
    slices         = []

    for src in original_sentences:
        print(src)
        src_ids = tokenizer(src, add_special_tokens=False)["input_ids"]

        pos, win_len = find_token_subsequence(
            trans_ids, src_ids, cursor_token, **kwargs
        )
        if pos == -1:
            raise ValueError(f"'{src[:30]}...'을(를) 찾지 못했습니다.")

        # ② 토큰 → 문자 위치 변환으로 '원본 그대로' 추출
        char_start = offsets[pos][0]
        char_end   = offsets[pos + win_len - 1][1]
        exact_sub  = translated[char_start : char_end]

        print(exact_sub)
        slices.append(exact_sub)
        cursor_token = pos + win_len

    return slices
