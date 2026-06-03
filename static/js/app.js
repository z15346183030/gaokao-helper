// ===== 全局应用逻辑 =====
const App = {
    currentPage: 'recommend',

    init() {
        this.initRouter();
        this.initSettings();
        this.checkApiStatus();
    },

    // 路由
    initRouter() {
        const tabs = document.querySelectorAll('.nav-tab');
        tabs.forEach(tab => {
            tab.addEventListener('click', (e) => {
                e.preventDefault();
                const page = tab.dataset.page;
                this.switchPage(page);
                window.location.hash = `/${page}`;
            });
        });

        const hash = window.location.hash.replace('#/', '') || 'recommend';
        this.switchPage(hash);
    },

    switchPage(page) {
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));

        const pageEl = document.getElementById(`page-${page}`);
        const tabEl = document.querySelector(`.nav-tab[data-page="${page}"]`);

        if (pageEl) pageEl.classList.add('active');
        if (tabEl) tabEl.classList.add('active');

        this.currentPage = page;
    },

    // 设置弹窗
    initSettings() {
        const modal = document.getElementById('settingsModal');
        const btnSettings = document.getElementById('btnSettings');
        const btnClose = document.getElementById('btnCloseSettings');
        const btnSave = document.getElementById('btnSaveKey');

        btnSettings.addEventListener('click', () => modal.classList.add('active'));
        btnClose.addEventListener('click', () => modal.classList.remove('active'));
        modal.addEventListener('click', (e) => {
            if (e.target === modal) modal.classList.remove('active');
        });

        btnSave.addEventListener('click', () => this.saveApiKey());
    },

    async checkApiStatus() {
        try {
            const res = await fetch('/api/config/status');
            const data = await res.json();
            const statusEl = document.getElementById('apiKeyStatus');
            if (data.has_key) {
                statusEl.textContent = 'API Key 已配置' + (data.ai_ready ? '，AI 功能就绪' : '');
                statusEl.className = 'api-status success';
            } else {
                statusEl.textContent = '未配置 API Key，AI 校园信息功能不可用';
                statusEl.className = 'api-status error';
            }
        } catch (e) {
            console.error('检查 API 状态失败:', e);
        }
    },

    async saveApiKey() {
        const input = document.getElementById('apiKeyInput');
        const key = input.value.trim();
        if (!key) return;

        try {
            const res = await fetch('/api/config/api-key', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ api_key: key })
            });
            const data = await res.json();
            if (data.success) {
                input.value = '';
                this.checkApiStatus();
                const statusEl = document.getElementById('apiKeyStatus');
                statusEl.textContent = '保存成功！AI 功能已启用';
                statusEl.className = 'api-status success';
            }
        } catch (e) {
            const statusEl = document.getElementById('apiKeyStatus');
            statusEl.textContent = '保存失败: ' + e.message;
            statusEl.className = 'api-status error';
        }
    },

    // API 工具方法
    async fetchJSON(url, options = {}) {
        const res = await fetch(url, options);
        if (!res.ok) {
            const err = await res.json().catch(() => ({ detail: res.statusText }));
            throw new Error(err.detail || '请求失败');
        }
        return res.json();
    },

    // 渲染大学卡片
    renderUniCard(uni, extra = '') {
        const tags = (uni.tags || '').split('|').filter(Boolean);
        const tagHTML = tags.map(t => `<span class="uni-tag">${t}</span>`).join('');
        const info = [uni.province, uni.city !== uni.province ? uni.city : '', uni.type].filter(Boolean).join(' · ');

        return `
            <div class="uni-card" data-name="${uni.name}">
                <div class="uni-card-left">
                    <div class="uni-name">${uni.name}</div>
                    <div class="uni-info">${info}</div>
                    ${extra}
                </div>
                <div class="uni-card-right">
                    <div class="uni-tags">${tagHTML}</div>
                    <span class="uni-arrow">→</span>
                </div>
            </div>
        `;
    },

    // 渲染推荐卡片
    renderRecCard(uni, level) {
        const levelNames = { chong: '冲刺', wen: '稳妥', bao: '保底' };
        const diff = uni.score_diff || 0;
        const diffClass = diff >= 0 ? 'positive' : 'negative';
        const diffText = diff >= 0 ? `高于均分 ${diff.toFixed(0)} 分` : `低于均分 ${Math.abs(diff).toFixed(0)} 分`;

        return `
            <div class="uni-card rec-card ${level}" data-name="${uni.name}">
                <div class="uni-card-left">
                    <div class="uni-name">${uni.name}</div>
                    <div class="uni-info">${uni.province} · ${uni.type}</div>
                    <div class="rec-score ${diffClass}">加权均分 ${uni.avg_score.toFixed(0)} · ${diffText}</div>
                </div>
                <div class="uni-card-right">
                    <span class="badge ${level}">${levelNames[level]}</span>
                    <span class="uni-arrow">→</span>
                </div>
            </div>
        `;
    }
};

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', () => App.init());
