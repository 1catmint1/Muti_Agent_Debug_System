# utils/normalizer.py
import os

def normalize_shape(s: str) -> str:
    """统一到 'rectangle' / 'triangle' / 'jigsaw'"""
    mapping = {
        "rectangle": "rectangle", "square": "rectangle", "正方形": "rectangle", "方形": "rectangle",
        "triangle": "triangle", "三角形": "triangle",
        "jigsaw": "jigsaw", "irregular": "jigsaw", "凹凸形": "jigsaw", "不规则": "jigsaw",
    }
    key = (s or "").strip().lower()
    if s in ("正方形", "方形"): return "rectangle"
    if s == "三角形": return "triangle"
    if s in ("凹凸形", "不规则"): return "jigsaw"
    return mapping.get(key, "jigsaw")

def infer_image_id(image_path: str) -> str:
    """从路径推断 image_id；custom/<id>/... -> <id>；否则用文件名"""
    if not image_path:
        return "default"
    parts = os.path.normpath(image_path).split(os.sep)
    if "custom" in parts:
        i = parts.index("custom")
        if i + 1 < len(parts):
            return parts[i + 1]
    return os.path.splitext(os.path.basename(image_path))[0]

def normalize_difficulty(d) -> int:
    try:
        return int(d)
    except (ValueError, TypeError):
        return 3