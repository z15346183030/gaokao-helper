import json
import os
import anthropic


CAMPUS_INFO_PROMPT = """你是校园生活信息顾问。请根据你所掌握的信息，详细介绍「{university}」的校园生活情况。

请从以下5个方面分别介绍，每个方面用简短的要点形式：

【宿舍条件】
- 几人间、有无空调、有无独立卫浴、有无阳台
- 大致住宿费用
- 新旧校区宿舍差异（如有）

【食堂餐饮】
- 食堂数量和特色
- 价格水平
- 口碑如何

【校园环境】
- 校园面积和绿化
- 图书馆、体育设施
- 建筑风格和整体氛围

【交通出行】
- 最近的地铁站/公交站及步行距离
- 到市中心/火车站/机场的大致时间
- 校区位置（市区/郊区）

【周边配套】
- 周边商业（商场、超市）
- 医疗资源
- 娱乐休闲

如果你不确定某些信息，请如实说明。请用中文回答，语言简洁明了。"""


SYSTEM_PROMPT = """你是「高考择校助手」的 AI 顾问。你帮助高考毕业生了解大学的真实校园生活，而不只是分数匹配。

你拥有以下数据上下文：
{data_context}

你的核心价值是帮助学生了解：
- 在某所大学读书是什么体验
- 校园生活条件如何
- 交通是否便利
- 适合什么样的学生

回答要简洁、专业、有温度。使用中文。"""


class ClaudeClient:
    def __init__(self, api_key):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-sonnet-4-20250514"
        self.data_context = ""
        self.cache_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "ai_cache"
        )
        os.makedirs(self.cache_dir, exist_ok=True)

    def set_data_context(self, data_loader):
        lines = ["【大学信息摘要】"]
        unis = data_loader.universities
        lines.append(f"共 {len(unis)} 所大学")
        for _, row in unis.iterrows():
            lines.append(
                f"- {row['name']} | {row['province']}{row['city']} | {row['type']} | {row.get('tags', '')}"
            )

        lines.append("")
        lines.append("【2025年录取分数摘要】")
        scores = data_loader.admission_scores
        for _, row in scores.iterrows():
            lines.append(
                f"- {row['university']} | {row['province']} | {row['subject_type']} | "
                f"最低分: {row['min_score']} | 最低位次: {row['min_rank']}"
            )

        self.data_context = "\n".join(lines)

    def _get_cache_path(self, university_name):
        safe_name = university_name.replace("/", "_").replace("\\", "_")
        return os.path.join(self.cache_dir, f"{safe_name}.json")

    def get_cached_campus_info(self, university_name):
        path = self._get_cache_path(university_name)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("content", "")
        return None

    def save_campus_info_cache(self, university_name, content):
        path = self._get_cache_path(university_name)
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"university": university_name, "content": content}, f, ensure_ascii=False, indent=2)

    def get_campus_info(self, university_name):
        cached = self.get_cached_campus_info(university_name)
        if cached:
            return cached

        prompt = CAMPUS_INFO_PROMPT.format(university=university_name)
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}],
            )
            content = response.content[0].text
            self.save_campus_info_cache(university_name, content)
            return content
        except Exception as e:
            return f"获取信息失败: {str(e)}"
