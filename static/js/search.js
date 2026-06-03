// ===== 找大学页面 =====
const Search = {
    init() {
        this.loadFilters();
        document.getElementById('btnSearch').addEventListener('click', () => this.doSearch());
        document.getElementById('searchName').addEventListener('input', () => this.doSearch());
        document.getElementById('searchProvince').addEventListener('change', () => this.doSearch());
        document.getElementById('searchType').addEventListener('change', () => this.doSearch());
        this.doSearch();
    },

    async loadFilters() {
        try {
            const [provinces, types] = await Promise.all([
                App.fetchJSON('/api/provinces'),
                App.fetchJSON('/api/universities').then(data => {
                    const t = new Set(data.map(u => u.type));
                    return [...t].sort();
                })
            ]);

            const provSelect = document.getElementById('searchProvince');
            provinces.forEach(p => {
                const opt = document.createElement('option');
                opt.value = p;
                opt.textContent = p;
                provSelect.appendChild(opt);
            });

            const typeSelect = document.getElementById('searchType');
            types.forEach(t => {
                const opt = document.createElement('option');
                opt.value = t;
                opt.textContent = t;
                typeSelect.appendChild(opt);
            });
        } catch (e) {
            console.error('加载筛选项失败:', e);
        }
    },

    async doSearch() {
        const name = document.getElementById('searchName').value.trim();
        const province = document.getElementById('searchProvince').value;
        const type = document.getElementById('searchType').value;

        const params = new URLSearchParams();
        if (name) params.set('name', name);
        if (province) params.set('province', province);
        if (type) params.set('type', type);

        try {
            const results = await App.fetchJSON(`/api/universities?${params.toString()}`);
            this.renderResults(results);
        } catch (e) {
            console.error('搜索失败:', e);
        }
    },

    renderResults(results) {
        document.getElementById('resultCount').textContent = `共找到 ${results.length} 所大学`;

        const list = document.getElementById('universityList');
        if (results.length === 0) {
            list.innerHTML = '<p style="color:#CCC;text-align:center;padding:40px">没有找到匹配的大学</p>';
            return;
        }

        list.innerHTML = results.map(uni => App.renderUniCard(uni)).join('');

        list.querySelectorAll('.uni-card').forEach(card => {
            card.addEventListener('click', () => {
                Detail.open(card.dataset.name);
            });
        });
    }
};

document.addEventListener('DOMContentLoaded', () => Search.init());
