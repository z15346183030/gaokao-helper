// ===== 大学详情弹窗 =====
const Detail = {
    currentUni: null,

    init() {
        const modal = document.getElementById('detailModal');
        const btnClose = document.getElementById('btnClose');

        btnClose.addEventListener('click', () => this.close());
        modal.addEventListener('click', (e) => {
            if (e.target === modal) this.close();
        });
    },

    async open(name) {
        const modal = document.getElementById('detailModal');
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';

        document.getElementById('campusText').style.display = 'none';
        document.getElementById('campusLoading').style.display = 'flex';
        document.getElementById('basicInfo') && (document.getElementById('basicInfo').innerHTML = '');
        document.getElementById('scoreTable').innerHTML = '';

        try {
            const detail = await App.fetchJSON(`/api/universities/${encodeURIComponent(name)}`);
            this.currentUni = detail;
            document.getElementById('modalName').textContent = detail.info.name;

            const tags = (detail.info.tags || '').split('|').filter(Boolean);
            const infoText = [detail.info.province, detail.info.city, detail.info.type].filter(Boolean).join(' · ');
            document.getElementById('modalInfo').textContent = infoText;

            this.renderScoreTable(detail.current_scores || []);
            this.loadCampusInfo(detail.info.name);
        } catch (e) {
            document.getElementById('modalName').textContent = '加载失败';
            document.getElementById('modalInfo').textContent = e.message;
        }
    },

    close() {
        document.getElementById('detailModal').classList.remove('active');
        document.body.style.overflow = '';
    },

    renderScoreTable(scores) {
        const container = document.getElementById('scoreTable');
        if (!scores.length) {
            container.innerHTML = '<p style="color:#CCC;padding:12px">暂无录取数据</p>';
            return;
        }

        let html = '<table class="score-table"><thead><tr>';
        html += '<th>省份</th><th>科类</th><th>最低分</th><th>最低位次</th>';
        html += '</tr></thead><tbody>';

        scores.forEach(s => {
            html += `<tr>
                <td>${s.province || ''}</td>
                <td>${s.subject_type || ''}</td>
                <td>${s.min_score || ''}</td>
                <td>${s.min_rank || ''}</td>
            </tr>`;
        });

        html += '</tbody></table>';
        container.innerHTML = html;
    },

    async loadCampusInfo(name) {
        try {
            const data = await App.fetchJSON(`/api/campus-info/${encodeURIComponent(name)}`);
            document.getElementById('campusLoading').style.display = 'none';
            const textEl = document.getElementById('campusText');
            textEl.style.display = 'block';
            textEl.textContent = data.content;
        } catch (e) {
            document.getElementById('campusLoading').innerHTML = `
                <span style="color:#FF6B6B">获取失败: ${e.message}</span>
            `;
        }
    }
};

document.addEventListener('DOMContentLoaded', () => Detail.init());
