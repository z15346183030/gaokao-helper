// ===== 智能推荐页面 =====
const Recommend = {
    init() {
        this.loadProvinces();
        document.getElementById('btnRecommend').addEventListener('click', () => this.doRecommend());
    },

    async loadProvinces() {
        try {
            const provinces = await App.fetchJSON('/api/provinces');
            const select = document.getElementById('recProvince');
            provinces.forEach(p => {
                const opt = document.createElement('option');
                opt.value = p;
                opt.textContent = p;
                select.appendChild(opt);
            });
            select.addEventListener('change', () => this.loadSubjects());
            this.loadSubjects();
        } catch (e) {
            console.error('加载省份失败:', e);
        }
    },

    async loadSubjects() {
        const province = document.getElementById('recProvince').value;
        if (!province) return;
        try {
            const subjects = await App.fetchJSON(`/api/subjects?province=${encodeURIComponent(province)}`);
            const select = document.getElementById('recSubject');
            select.innerHTML = '';
            subjects.forEach(s => {
                const opt = document.createElement('option');
                opt.value = s;
                opt.textContent = s;
                select.appendChild(opt);
            });
        } catch (e) {
            console.error('加载科类失败:', e);
        }
    },

    async doRecommend() {
        const province = document.getElementById('recProvince').value;
        const subject = document.getElementById('recSubject').value;
        const score = parseInt(document.getElementById('recScore').value);

        if (!province || !subject) return;

        const container = document.getElementById('recResults');
        container.innerHTML = '<div class="loading-spinner"><div class="spinner"></div><span>正在推荐...</span></div>';

        try {
            const results = await App.fetchJSON('/api/recommend', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ province, subject, score })
            });

            this.renderResults(results, province, subject, score);
        } catch (e) {
            container.innerHTML = `<p style="color:#FF6B6B;text-align:center;padding:20px">推荐失败: ${e.message}</p>`;
        }
    },

    renderResults(results, province, subject, score) {
        const container = document.getElementById('recResults');
        let html = '';

        const sections = [
            { title: '冲刺院校', key: 'chong', desc: '分数略高于历年录取线，可尝试' },
            { title: '稳妥院校', key: 'wen', desc: '与历年录取线接近，概率较大' },
            { title: '保底院校', key: 'bao', desc: '分数明显高于录取线，非常安全' },
        ];

        sections.forEach(sec => {
            const unis = results[sec.key] || [];
            html += `<h2 class="section-title">${sec.title}（${unis.length} 所）</h2>`;
            html += `<p class="section-desc">${sec.desc}</p>`;

            if (unis.length === 0) {
                html += '<p style="color:#CCC;padding:12px">暂无推荐</p>';
            } else {
                unis.forEach(uni => {
                    html += App.renderRecCard(uni, sec.key);
                });
            }
        });

        container.innerHTML = html;

        // 绑定卡片点击事件
        container.querySelectorAll('.uni-card').forEach(card => {
            card.addEventListener('click', () => {
                Detail.open(card.dataset.name);
            });
        });
    }
};

document.addEventListener('DOMContentLoaded', () => Recommend.init());
