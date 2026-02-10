"""
Dataset manager for storing classified comments
"""
import os
import csv
from typing import Dict, List
from .models import Comment, Sentiment


class DatasetManager:
    """Manages the dataset CSV file for storing classified comments"""
    
    def __init__(self, path: str):
        self.path = path
        self._ensure_file()
    
    def _ensure_file(self):
        """Ensure the dataset file exists with proper headers"""
        if not os.path.exists(self.path):
            with open(self.path, "w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(["comment", "target"])
    
    def _read_all(self) -> List[Dict[str, str]]:
        """Read all rows from the dataset"""
        with open(self.path, "r", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    
    def _write_all(self, rows: List[Dict[str, str]]):
        """Write all rows to the dataset"""
        with open(self.path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["comment", "target"])
            writer.writeheader()
            writer.writerows(rows)
    
    def save_comment(self, comment: str, sentiment: Sentiment):
        """Save or update a comment with its sentiment in the dataset"""
        rows = self._read_all()
        for row in rows:
            if row["comment"] == comment:
                row["target"] = str(sentiment.value)
                self._write_all(rows)
                return
        rows.append({"comment": comment, "target": str(sentiment.value)})
        self._write_all(rows)
    
    def remove_comment(self, comment: str):
        """Remove a comment from the dataset"""
        rows = self._read_all()
        rows = [row for row in rows if row["comment"] != comment]
        self._write_all(rows)
    
    def get_counts(self) -> Dict[str, int]:
        """Get count of comments by sentiment"""
        counts = {"positive": 0, "neutral": 0, "negative": 0, "total": 0}
        for row in self._read_all():
            target_value = row.get("target", "")
            if target_value == "1":
                counts["positive"] += 1
            elif target_value == "0":
                counts["neutral"] += 1
            elif target_value == "-1":
                counts["negative"] += 1
            counts["total"] += 1
        return counts