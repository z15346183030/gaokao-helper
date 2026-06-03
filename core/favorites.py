import json
import os


class FavoritesManager:
    def __init__(self, filepath):
        self.filepath = filepath
        self.favorites = []
        self._load()

    def _load(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, "r", encoding="utf-8") as f:
                self.favorites = json.load(f)

    def _save(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.favorites, f, ensure_ascii=False, indent=2)

    def add(self, university_name):
        if university_name not in self.favorites:
            self.favorites.append(university_name)
            self._save()
            return True
        return False

    def remove(self, university_name):
        if university_name in self.favorites:
            self.favorites.remove(university_name)
            self._save()
            return True
        return False

    def is_favorite(self, university_name):
        return university_name in self.favorites

    def get_all(self):
        return list(self.favorites)

    def toggle(self, university_name):
        if self.is_favorite(university_name):
            self.remove(university_name)
            return False
        else:
            self.add(university_name)
            return True

    def export_text(self):
        if not self.favorites:
            return "暂无收藏的大学。"
        lines = ["=" * 40, "我的收藏大学列表", "=" * 40, ""]
        for i, name in enumerate(self.favorites, 1):
            lines.append(f"{i}. {name}")
        lines.append("")
        lines.append(f"共收藏 {len(self.favorites)} 所大学")
        return "\n".join(lines)
