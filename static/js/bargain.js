// ===== 试试捡个漏页面 =====
const Bargain = {
    init() {
        this.loadProvinces();
        document.getElementById('btnBargain').addEventListener('click', () => this.doBargain());
    },

    async loadProvinces() {
        try {
            const provinces = await App.fetchJSON('/api/provinces');
            const select = document.getElementById('bargainProvince');
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
        const province = document.getElementById('bargainProvince').value;
        if (!province) return;
        try {
            const subjects = await App.fetchJSON(`/api/subjects?province=${encodeURIComponent(province)}`);
            const select = document.getElementById('bargainSubject');
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

    async doBargain() {
        const province = document.getElementById('bargainProvince').value;
        const subject = document.getElementById('bargainSubject').value;
        const score = parseInt(document.getElementById('bargainScore').value);

        if (!province || !subject) return;

        const container = document.getElementById('bargainResults');
        container.innerHTML = '<div class="loading-spinner"><div class="spinner"></div><span>正在分析历年数据，寻找捡漏机会...</span></div>';

        try {
            const results = await App.fetchJSON('/api/bargain', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ province, subject, score })
            });
            this.renderResults(results, province, subject, score);
        } catch (e) {
            container.innerHTML = `<p style="color:#FF6B6B;text-align:center;padding:20px">分析失败: ${e.message}</p>`;
        }
    },

    renderResults(results, province, subject, score) {
        const container = document.getElementById('bargainResults');

        if (!results.length) {
            container.innerHTML = `
                <div class="section-card" style="text-align:center;padding:40px">
                    <p style="font-size:48px;margin-bottom:12px">😅</p>
                    <p style="font-size:16px;color:#555">暂时没有找到合适的捡漏机会</p>
                    <p style="font-size:13px;color:#999;margin-top:8px">可以试试调整分数或换一个省份</p>
                </div>
            `;
            return;
        }

        let html = `
            <div class="section-card" style="background:#FFF8E1;border:1px solid #FFD54F;margin-bottom:20px">
                <p style="font-size:15px;color:#F57F17;font-weight:bold">
                    💡 捡漏原理：以下学校历年录取分数波动较大，有些年份出现过低于你分数的录取线，有机会"捡漏"录取！
                </p>
            </div>
        `;

        html += `<h2 class="section-title">找到 ${results.length} 个捡漏机会</h2>`;

        results.forEach((uni, index) => {
            const history = uni.history || [];
            const minYear = history.reduce((min, h) => h.min_score < min.min_score ? h : min, history[0]);
            const maxYear = history.reduce((max, h) => h.min_score > max.min_score ? h : max, history[0]);
            const diff = score - minYear.min_score;

            let historyHTML = history.map(h => {
                const isLow = h.min_score === minYear.min_score;
                const color = isLow ? '#FF6B6B' : '#555';
                const bg = isLow ? '#FFF0F0' : 'transparent';
                return `<span style="display:inline-block;padding:4px 10px;margin:2px;border-radius:6px;background:${bg};color:${color};font-size:12px;font-weight:${isLow ? 'bold' : 'normal'}">${h.year}年: ${h.min_score}分</span>`;
            }).join('');

            html += `
                <div class="uni-card bargain-card" data-name="${uni.name}">
                    <div class="uni-card-left">
                        <div class="uni-name">
                            <span style="color:#FF6B6B;font-size:12px;margin-right:6px">🔥</span>
                            ${uni.name}
                        </div>
                        <div class="uni-info">${uni.province} · ${uni.type} · ${uni.tags || ''}</div>
                        <div style="margin-top:8px">
                            <span style="font-size:12px;color:#888">历年最低分：</span>
                            ${historyHTML}
                        </div>
                        <div style="margin-top:6px;font-size:13px">
                            <span style="color:#51CF66;font-weight:bold">最低 ${minYear.min_score}分（${minYear.year}年）</span>
                            <span style="color:#999;margin:0 8px">|</span>
                            <span style="color:#FF6B6B">最高 ${maxYear.min_score}分（${maxYear.year}年）</span>
                            <span style="color:#999;margin:0 8px">|</span>
                            <span style="color:#F57F17;font-weight:bold">波动 ${maxYear.min_score - minYear.min_score} 分</span>
                        </div>
                        <div style="margin-top:6px;padding:6px 10px;background:#EAFAF1;border-radius:6px;display:inline-block">
                            <span style="font-size:13px;color:#27AE60;font-weight:bold">
                                你的分数 ${score} 高于最低录取线 ${diff} 分，有机会！
                            </span>
                        </div>
                    </div>
                    <div class="uni-card-right">
                        <span class="badge" style="background:#FF6B6B">捡漏</span>
                        <span class="uni-arrow">→</span>
                    </div>
                </div>
            `;
        });

        container.innerHTML = html;

        container.querySelectorAll('.bargain-card').forEach(card => {
            card.addEventListener('click', () => {
                Detail.open(card.dataset.name);
            });
        });
    }
};

document.addEventListener('DOMContentLoaded', () => Bargain.init());
