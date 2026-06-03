// ===== 大学详情弹窗 =====
const Detail = {
    currentUni: null,

    init() {
        const modal = document.getElementById('detailModal');
        const btnClose = document.getElementById('btnClose');
        const btnFav = document.getElementById('btnFav');

        btnClose.addEventListener('click', () => this.close());
        modal.addEventListener('click', (e) => {
            if (e.target === modal) this.close();
        });

        btnFav.addEventListener('click', () => this.toggleFav());
    },

    async open(name) {
        const modal = document.getElementById('detailModal');
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';

        // 重置内容
        document.getElementById('campusText').style.display = 'none';
        document.getElementById('campusLoading').style.display = 'flex';
        document.getElementById('basicInfo').innerHTML = '';
        document.getElementById('scoreTable').innerHTML = '';

        try {
            const detail = await App.fetchJSON(`/api/universities/${encodeURIComponent(name)}`);
            this.currentUni = detail;
            this.renderBasicInfo(detail.info);
            this.renderScoreTable(detail.current_scores || []);
            this.updateFavButton(detail.info.name);
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

    renderBasicInfo(info) {
        document.getElementById('modalName').textContent = info.name;

        const tags = (info.tags || '').split('|').filter(Boolean);
        const infoText = [info.province, info.city, info.type].filter(Boolean).join(' · ');
        document.getElementById('modalInfo').textContent = infoText;

        const grid = document.getElementById('basicInfo');
        const rows = [
            ['省份', info.province],
            ['城市', info.city || info.province],
            ['类型', info.type],
            ['标签', tags.join('  ') || '无'],
            ['官网', info.website ? `<a href="${info.website}" target="_blank">${info.website}</a>` : '暂无'],
        ];

        grid.innerHTML = rows.map(([label, value]) => `
            <div class="info-label">${label}</div>
            <div class="info-value">${value}</div>
        `).join('');
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

            if (data.cached) {
                const cachedLabel = document.createElement('div');
                cachedLabel.style.cssText = 'font-size:11px;color:#999;margin-top:8px;text-align:right;';
                cachedLabel.textContent = '(缓存数据)';
                textEl.parentNode.appendChild(cachedLabel);
            }
        } catch (e) {
            document.getElementById('campusLoading').innerHTML = `
                <span style="color:#FF6B6B">获取失败: ${e.message}</span>
            `;
        }
    },

    async updateFavButton(name) {
        try {
            const favs = await App.fetchJSON('/api/favorites');
            const btn = document.getElementById('btnFav');
            if (favs.includes(name)) {
                btn.textContent = '已收藏';
                btn.classList.add('faved');
            } else {
                btn.textContent = '收藏';
                btn.classList.remove('faved');
            }
        } catch (e) {
            // 忽略
        }
    },

    async toggleFav() {
        if (!this.currentUni) return;
        const name = this.currentUni.info.name;
        const btn = document.getElementById('btnFav');

        try {
            if (btn.classList.contains('faved')) {
                await App.fetchJSON(`/api/favorites/${encodeURIComponent(name)}`, { method: 'DELETE' });
                btn.textContent = '收藏';
                btn.classList.remove('faved');
            } else {
                await App.fetchJSON(`/api/favorites/${encodeURIComponent(name)}`, { method: 'POST' });
                btn.textContent = '已收藏';
                btn.classList.add('faved');
            }
        } catch (e) {
            console.error('收藏操作失败:', e);
        }
    }
};

document.addEventListener('DOMContentLoaded', () => Detail.init());
