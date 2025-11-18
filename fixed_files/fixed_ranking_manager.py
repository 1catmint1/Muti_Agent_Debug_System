# data/ranking_manager.py
import os, json, time
from typing import List, Dict, Any, Optional
from config import RANKING_DIR

LEADERBOARD_PATH = os.path.join(RANKING_DIR, "leaderboard.json")

def _ensure_dir(path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)

def _now_str() -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def _normalize_shape(s: str) -> str:
    if not s:
        return "jigsaw"
    m = {
        "正方形":"rectangle","方形":"rectangle","square":"rectangle","rectangle":"rectangle",
        "三角形":"triangle","triangle":"triangle",
        "不规则":"jigsaw","凹凸形":"jigsaw","jigsaw":"jigsaw","irregular":"jigsaw"
    }
    return m.get(s, "jigsaw")

def _to_int_seconds(v) -> Optional[int]:
    if v is None:
        return None
    try:
        # 支持 "12", "12.3", 12, 12.0
        return int(round(float(v)))
    except (ValueError, TypeError):
        return None

def _normalize_record(rec: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    统一记录字段：
    - image: str
    - difficulty: int（3/4/5）
    - shape: 'jigsaw' | 'triangle' | 'rectangle'
    - elapsed: int（秒）
    - finished_at: 'YYYY-MM-DD HH:MM:SS'
    """
    image = rec.get("image") or rec.get("image_id") or rec.get("img") or "default"
    shape = _normalize_shape(rec.get("shape") or rec.get("type") or "jigsaw")

    # 难度可能以 rows/cols/level/字符串形式保存
    diff = rec.get("difficulty", None)
    if diff is None:
        diff = rec.get("level", None)
    if diff is None:
        diff = rec.get("rows", None)
    try:
        difficulty = int(diff) if diff is not None else 3
    except (ValueError, TypeError):
        difficulty = 3

    # elapsed 的各种历史命名
    elapsed = (
        _to_int_seconds(rec.get("elapsed")) or
        _to_int_seconds(rec.get("elapsed_sec")) or
        _to_int_seconds(rec.get("seconds")) or
        _to_int_seconds(rec.get("time")) or
        _to_int_seconds(rec.get("use_time")) or
        0
    )

    # finished_at 的历史命名
    finished_at = (
        rec.get("finished_at") or
        rec.get("date") or
        rec.get("timestamp") or
        _now_str()
    )

    if elapsed is None:
        elapsed = 0

    return {
        "image": str(image),
        "difficulty": int(difficulty),
        "shape": shape,
        "elapsed": int(elapsed),
        "finished_at": str(finished_at),
    }

class RankingManager:
    def __init__(self, path: str = LEADERBOARD_PATH):
        self.path = path
        _ensure_dir(self.path)
        self._data: List[Dict[str, Any]] = []
        self._load()

    def _load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    raw = json.load(f)
                # 支持 list 或 dict 包裹
                records = raw.get("records", raw) if isinstance(raw, dict) else raw
                if not isinstance(records, list):
                    records = []
            except (json.JSONDecodeError, OSError):
                records = []
        else:
            records = []

        normalized = []
        for r in records:
            nr = _normalize_record(r)
            if nr:
                normalized.append(nr)

        self._data = normalized
        self._save()  # 一次性写回规范化后的结构

    def _save(self):
        payload = {"records": self._data}
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

    # 统一写入（游戏完成时调用）
    def add_record(self, image: str, difficulty: int, shape: str, elapsed_sec: int, finished_at: Optional[str] = None):
        rec = _normalize_record({
            "image": image,
            "difficulty": difficulty,
            "shape": shape,
            "elapsed": elapsed_sec,
            "finished_at": finished_at or _now_str(),
        })
        self._data.append(rec)
        self._save()

    # 统一查询（排行榜使用）
    def query(self, image: Optional[str] = None, difficulty: Optional[int] = None, shape: Optional[str] = None, limit: int = 20) -> List[Dict[str, Any]]:
        image = image or None
        shape = _normalize_shape(shape) if shape else None

        rows = []
        for r in self._data:
            if image and r["image"] != image:
                continue
            if difficulty and int(r["difficulty"]) != int(difficulty):
                continue
            if shape and r["shape"] != shape:
                continue
            rows.append(r)

        rows.sort(key=lambda x: x.get("elapsed", 1_000_000))
        return rows[: max(1, int(limit))]

    # 给 UI 的选项集
    def get_all_values(self):
        images = sorted({r["image"] for r in self._data} | {"default"})
        diffs  = sorted({int(r["difficulty"]) for r in self._data} | {3,4,5})
        shapes = sorted({r["shape"] for r in self._data} | {"jigsaw","triangle","rectangle"})
        return {"images": images, "difficulties": diffs, "shapes": shapes}

    # 兼容旧 UI 调用名
    def get_records(self, image=None, difficulty=None, shape=None, limit=20):
        return self.query(image=image, difficulty=difficulty, shape=shape, limit=limit)