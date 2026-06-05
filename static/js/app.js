// ===== 全局应用逻辑 =====
const App = {
    currentPage: 'look',

    init() {
        this.initRouter();
    },

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

        const hash = window.location.hash.replace('#/', '') || 'look';
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

    async fetchJSON(url, options = {}) {
        const res = await fetch(url, options);
        if (!res.ok) {
            const err = await res.json().catch(() => ({ detail: res.statusText }));
            throw new Error(err.detail || '请求失败');
        }
        return res.json();
    },

    renderUniCard(uni) {
        const tags = (uni.tags || '').split('|').filter(Boolean);
        const tagHTML = tags.map(t => `<span class="uni-tag">${t}</span>`).join('');
        const info = [uni.province, uni.city !== uni.province ? uni.city : '', uni.type].filter(Boolean).join(' · ');

        return `
            <div class="uni-card" data-name="${uni.name}">
                <div class="uni-card-left">
                    <div class="uni-name">${uni.name}</div>
                    <div class="uni-info">${info}</div>
                </div>
                <div class="uni-card-right">
                    <div class="uni-tags">${tagHTML}</div>
                    <span class="uni-arrow">→</span>
                </div>
            </div>
        `;
    }
};

document.addEventListener('DOMContentLoaded', () => App.init());
