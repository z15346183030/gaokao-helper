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

        // 重置
        document.getElementById('campusText').style.display = 'none';
        document.getElementById('campusLoading').style.display = 'flex';
        document.getElementById('campusLoading').innerHTML = '<div class="spinner"></div><span>正在加载校园信息...</span>';
        document.getElementById('scoreTable').innerHTML = '';

        try {
            const detail = await App.fetchJSON(`/api/universities/${encodeURIComponent(name)}`);
            this.currentUni = detail;

            document.getElementById('modalName').textContent = detail.info.name;
            const infoText = [detail.info.province, detail.info.city, detail.info.type].filter(Boolean).join(' · ');
            document.getElementById('modalInfo').textContent = infoText;

            this.renderScoreTable(detail.current_scores || []);

            // 同时加载数据库宿舍/交通 和 AI 分析
            this.loadDbInfo(name);
            this.loadCampusInfo(name);

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

    async loadDbInfo(name) {
        try {
            const [dorms, trans] = await Promise.all([
                App.fetchJSON(`/api/dormitory/${encodeURIComponent(name)}`),
                App.fetchJSON(`/api/transport/${encodeURIComponent(name)}`)
            ]);

            if (dorms.length || trans.length) {
                let html = '';

                if (dorms.length) {
                    html += '<div style="margin-bottom:16px">';
                    html += '<h4 style="font-size:14px;font-weight:bold;color:#1A73E8;margin-bottom:10px">🏠 宿舍条件</h4>';
                    dorms.forEach(d => {
                        html += `<div style="background:#F8F9FA;border-radius:10px;padding:14px;margin-bottom:8px;font-size:13px">`;
                        if (d.campus) html += `<div style="font-weight:bold;margin-bottom:6px">${d.campus}</div>`;
                        html += `<div style="display:grid;grid-template-columns:1fr 1fr;gap:4px 16px">`;
                        if (d.room_type) html += `<div>🛏️ ${d.room_type}</div>`;
                        if (d.bed_count) html += `<div>👥 ${d.bed_count}人间</div>`;
                        if (d.has_ac) html += `<div>${d.has_ac ? '✅' : '❌'} 空调</div>`;
                        if (d.has_bathroom) html += `<div>${d.has_bathroom ? '✅' : '❌'} 独立卫浴</div>`;
                        if (d.has_balcony) html += `<div>${d.has_balcony ? '✅' : '❌'} 阳台</div>`;
                        if (d.has_hotwater) html += `<div>${d.has_hotwater ? '✅' : '❌'} 热水</div>`;
                        if (d.cost_per_year) html += `<div>💰 ${d.cost_per_year}/年</div>`;
                        if (d.area) html += `<div>📐 ${d.area}</div>`;
                        html += `</div>`;
                        if (d.facilities) html += `<div style="margin-top:6px;color:#666">配套设施：${d.facilities}</div>`;
                        if (d.note) html += `<div style="margin-top:4px;color:#999;font-size:12px">${d.note}</div>`;
                        html += `</div>`;
                    });
                    html += '</div>';
                }

                if (trans.length) {
                    html += '<div>';
                    html += '<h4 style="font-size:14px;font-weight:bold;color:#2ED573;margin-bottom:10px">🚇 交通出行</h4>';
                    trans.forEach(t => {
                        html += `<div style="background:#F8F9FA;border-radius:10px;padding:14px;margin-bottom:8px;font-size:13px">`;
                        if (t.campus) html += `<div style="font-weight:bold;margin-bottom:6px">${t.campus}</div>`;
                        html += `<div style="display:grid;grid-template-columns:1fr 1fr;gap:4px 16px">`;
                        if (t.location_type) html += `<div>📍 ${t.location_type}</div>`;
                        if (t.nearest_metro) html += `<div>🚇 ${t.nearest_metro} ${t.metro_distance || ''}</div>`;
                        if (t.nearest_bus) html += `<div>🚌 ${t.nearest_bus} ${t.bus_distance || ''}</div>`;
                        if (t.to_center) html += `<div>🏙️ 到市中心 ${t.to_center}</div>`;
                        if (t.to_station) html += `<div>🚄 到火车站 ${t.to_station}</div>`;
                        if (t.to_airport) html += `<div>✈️ 到机场 ${t.to_airport}</div>`;
                        html += `</div>`;
                        if (t.nearby_malls) html += `<div style="margin-top:6px;color:#666">周边商业：${t.nearby_malls}</div>`;
                        if (t.nearby_hospital) html += `<div style="margin-top:4px;color:#666">医疗：${t.nearby_hospital}</div>`;
                        if (t.note) html += `<div style="margin-top:4px;color:#999;font-size:12px">${t.note}</div>`;
                        html += `</div>`;
                    });
                    html += '</div>';
                }

                // 在 AI 内容前插入数据库信息
                const campusText = document.getElementById('campusText');
                campusText.innerHTML = html;
                campusText.style.display = 'block';
                document.getElementById('campusLoading').style.display = 'none';
            }
        } catch (e) {
            console.error('加载数据库信息失败:', e);
        }
    },

    async loadCampusInfo(name) {
        // 如果数据库已有数据，AI 内容追加在后面
        try {
            const data = await App.fetchJSON(`/api/campus-info/${encodeURIComponent(name)}`);
            const campusText = document.getElementById('campusText');
            const existingHtml = campusText.innerHTML;

            if (existingHtml && existingHtml.trim()) {
                // 数据库有数据，AI 内容追加
                campusText.innerHTML = existingHtml +
                    '<hr style="margin:16px 0;border:none;border-top:1px solid #E8E8E8">' +
                    '<h4 style="font-size:14px;font-weight:bold;color:#F57F17;margin-bottom:10px">🤖 AI 综合分析</h4>' +
                    '<div style="white-space:pre-wrap;line-height:1.8;color:#333">' + data.content + '</div>';
            } else {
                // 数据库没数据，直接显示 AI 内容
                document.getElementById('campusLoading').style.display = 'none';
                campusText.style.display = 'block';
                campusText.textContent = data.content;
            }
        } catch (e) {
            const campusLoading = document.getElementById('campusLoading');
            if (campusLoading.style.display !== 'none') {
                campusLoading.innerHTML = `<span style="color:#FF6B6B">AI 分析失败: ${e.message}</span>`;
            }
        }
    }
};

document.addEventListener('DOMContentLoaded', () => Detail.init());
