import os
import pandas as pd


class DataLoader:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.universities = None
        self.admission_scores = None
        self.admission_history = None
        self.score_rankings = None
        self.provinces = None
        self._load_all()

    def _load_all(self):
        self.universities = pd.read_csv(
            os.path.join(self.data_dir, "universities.csv"), encoding="utf-8"
        )
        self.admission_scores = pd.read_csv(
            os.path.join(self.data_dir, "admission_scores.csv"), encoding="utf-8"
        )
        self.admission_history = pd.read_csv(
            os.path.join(self.data_dir, "admission_history.csv"), encoding="utf-8"
        )
        self.score_rankings = pd.read_csv(
            os.path.join(self.data_dir, "score_rankings.csv"), encoding="utf-8"
        )
        self.provinces = pd.read_csv(
            os.path.join(self.data_dir, "provinces.csv"), encoding="utf-8"
        )

    def get_province_list(self):
        return self.provinces["name"].tolist()

    def get_subject_types(self, province):
        scores = self.admission_scores[self.admission_scores["province"] == province]
        return sorted(scores["subject_type"].unique().tolist())

    def search_universities(self, name="", province="", university_type="", tag=""):
        df = self.universities.copy()
        if name:
            df = df[df["name"].str.contains(name, na=False)]
        if province:
            df = df[df["province"] == province]
        if university_type:
            df = df[df["type"] == university_type]
        if tag:
            df = df[df["tags"].str.contains(tag, na=False)]
        return df.to_dict("records")

    def get_university_detail(self, name):
        uni = self.universities[self.universities["name"] == name]
        if uni.empty:
            return None
        uni_info = uni.iloc[0].to_dict()

        current_scores = self.admission_scores[
            self.admission_scores["university"] == name
        ].to_dict("records")

        history = self.admission_history[
            self.admission_history["university"] == name
        ].to_dict("records")

        return {
            "info": uni_info,
            "current_scores": current_scores,
            "history": history,
        }

    def get_recommendations(self, province, subject_type, score):
        scores_2025 = self.admission_scores[
            (self.admission_scores["province"] == province)
            & (self.admission_scores["subject_type"] == subject_type)
        ]

        history = self.admission_history[
            (self.admission_history["province"] == province)
            & (self.admission_history["subject_type"] == subject_type)
        ]

        if scores_2025.empty and history.empty:
            return {"chong": [], "wen": [], "bao": []}

        uni_scores = {}
        for _, row in scores_2025.iterrows():
            name = row["university"]
            if name not in uni_scores:
                uni_scores[name] = {}
            uni_scores[name]["2025"] = row["min_score"]

        for _, row in history.iterrows():
            name = row["university"]
            year = str(row["year"])
            if name not in uni_scores:
                uni_scores[name] = {}
            if year not in uni_scores[name]:
                uni_scores[name][year] = row["min_score"]

        chong, wen, bao = [], [], []
        for name, years_data in uni_scores.items():
            weights = {"2025": 0.5, "2024": 0.3, "2023": 0.2}
            weighted_sum = 0
            weight_total = 0
            for year, w in weights.items():
                if year in years_data:
                    weighted_sum += years_data[year] * w
                    weight_total += w

            if weight_total == 0:
                continue

            avg_score = weighted_sum / weight_total
            diff = score - avg_score

            uni_info = self.universities[self.universities["name"] == name]
            if uni_info.empty:
                continue
            uni_data = uni_info.iloc[0].to_dict()
            uni_data["avg_score"] = round(avg_score, 1)
            uni_data["score_diff"] = round(diff, 1)
            uni_data["year_scores"] = years_data

            if diff < -20:
                continue
            elif diff < 0:
                uni_data["probability"] = "冲刺"
                chong.append(uni_data)
            elif diff < 10:
                uni_data["probability"] = "稳妥"
                wen.append(uni_data)
            else:
                uni_data["probability"] = "保底"
                bao.append(uni_data)

        chong.sort(key=lambda x: x["avg_score"], reverse=True)
        wen.sort(key=lambda x: x["avg_score"], reverse=True)
        bao.sort(key=lambda x: x["avg_score"], reverse=True)

        return {"chong": chong, "wen": wen, "bao": bao}

    def get_score_ranking(self, province, subject_type, year, score):
        rankings = self.score_rankings[
            (self.score_rankings["province"] == province)
            & (self.score_rankings["subject_type"] == subject_type)
            & (self.score_rankings["year"] == year)
        ]

        if rankings.empty:
            return None

        exact = rankings[rankings["score"] == score]
        if not exact.empty:
            row = exact.iloc[0]
            return {
                "score": int(row["score"]),
                "count": int(row["count"]),
                "cumulative_count": int(row["cumulative_count"]),
                "cumulative_ratio": float(row["cumulative_ratio"]),
            }

        lower = rankings[rankings["score"] < score].sort_values("score", ascending=False)
        if not lower.empty:
            row = lower.iloc[0]
            return {
                "score": int(row["score"]),
                "count": int(row["count"]),
                "cumulative_count": int(row["cumulative_count"]),
                "cumulative_ratio": float(row["cumulative_ratio"]),
            }

        return None

    def get_full_ranking_table(self, province, subject_type, year):
        rankings = self.score_rankings[
            (self.score_rankings["province"] == province)
            & (self.score_rankings["subject_type"] == subject_type)
            & (self.score_rankings["year"] == year)
        ]
        return rankings.sort_values("score", ascending=False).to_dict("records")

    def get_all_tags(self):
        tags = set()
        for t in self.universities["tags"].dropna():
            for tag in t.split("|"):
                tags.add(tag)
        return sorted(tags)

    def get_all_types(self):
        return sorted(self.universities["type"].unique().tolist())

    def get_years_for_ranking(self, province, subject_type):
        rankings = self.score_rankings[
            (self.score_rankings["province"] == province)
            & (self.score_rankings["subject_type"] == subject_type)
        ]
        return sorted(rankings["year"].unique().tolist(), reverse=True)
