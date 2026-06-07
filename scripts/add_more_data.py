import json
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
SEED_PATH = os.path.join(DATA_DIR, "seed_data.json")

with open(SEED_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

new_dorms = [
    {"university": "中国人民大学", "campus": "主校区", "room_type": "四人间", "bed_count": 4, "has_ac": 1, "has_bathroom": 1, "has_balcony": 1, "has_hotwater": 1, "cost_per_year": "750-1200元", "area": "约25㎡", "facilities": "独立卫浴、空调、洗衣机、书桌", "note": "品园宿舍区条件较好"},
    {"university": "北京师范大学", "campus": "主校区", "room_type": "四人间", "bed_count": 4, "has_ac": 1, "has_bathroom": 0, "has_balcony": 0, "has_hotwater": 1, "cost_per_year": "750元", "area": "约20㎡", "facilities": "公共卫浴、空调、洗衣机", "note": "宿舍翻新中"},
    {"university": "北京理工大学", "campus": "良乡校区", "room_type": "四人间", "bed_count": 4, "has_ac": 1, "has_bathroom": 1, "has_balcony": 1, "has_hotwater": 1, "cost_per_year": "900元", "area": "约28㎡", "facilities": "独立卫浴、空调、阳台、洗衣机", "note": "良乡校区宿舍较新"},
    {"university": "北京科技大学", "campus": "主校区", "room_type": "四人间/六人间", "bed_count": 4, "has_ac": 1, "has_bathroom": 0, "has_balcony": 0, "has_hotwater": 1, "cost_per_year": "750-900元", "area": "约20-25㎡", "facilities": "公共卫浴、空调、洗衣机", "note": "不同宿舍楼差异大"},
    {"university": "中央财经大学", "campus": "沙河校区", "room_type": "四人间", "bed_count": 4, "has_ac": 1, "has_bathroom": 1, "has_balcony": 1, "has_hotwater": 1, "cost_per_year": "900元", "area": "约28㎡", "facilities": "独立卫浴、空调、阳台、洗衣机", "note": "沙河校区条件好"},
    {"university": "华东师范大学", "campus": "闵行校区", "room_type": "四人间", "bed_count": 4, "has_ac": 1, "has_bathroom": 1, "has_balcony": 1, "has_hotwater": 1, "cost_per_year": "1200元", "area": "约28㎡", "facilities": "独立卫浴、空调、阳台、洗衣机", "note": "闵行校区宿舍条件好"},
    {"university": "上海大学", "campus": "宝山校区", "room_type": "四人间", "bed_count": 4, "has_ac": 1, "has_bathroom": 1, "has_balcony": 1, "has_hotwater": 1, "cost_per_year": "1200元", "area": "约28㎡", "facilities": "独立卫浴、空调、阳台、洗衣机", "note": "宝山校区宿舍好"},
    {"university": "苏州大学", "campus": "独墅湖校区", "room_type": "四人间", "bed_count": 4, "has_ac": 1, "has_bathroom": 1, "has_balcony": 1, "has_hotwater": 1, "cost_per_year": "1500元", "area": "约30㎡", "facilities": "独立卫浴、空调、阳台、洗衣机", "note": "独墅湖校区条件很好"},
    {"university": "东南大学", "campus": "九龙湖校区", "room_type": "四人间", "bed_count": 4, "has_ac": 1, "has_bathroom": 1, "has_balcony": 1, "has_hotwater": 1, "cost_per_year": "1200元", "area": "约28㎡", "facilities": "独立卫浴、空调、阳台、洗衣机", "note": "九龙湖校区较新"},
    {"university": "中南大学", "campus": "主校区", "room_type": "四人间", "bed_count": 4, "has_ac": 1, "has_bathroom": 1, "has_balcony": 1, "has_hotwater": 1, "cost_per_year": "1200元", "area": "约28㎡", "facilities": "独立卫浴、空调、阳台、洗衣机", "note": "新校区条件好"},
    {"university": "湖南大学", "campus": "主校区", "room_type": "四人间", "bed_count": 4, "has_ac": 1, "has_bathroom": 1, "has_balcony": 1, "has_hotwater": 1, "cost_per_year": "1200元", "area": "约25㎡", "facilities": "独立卫浴、空调、阳台、洗衣机", "note": "天马宿舍区条件好"},
    {"university": "电子科技大学", "campus": "清水河校区", "room_type": "四人间", "bed_count": 4, "has_ac": 1, "has_bathroom": 1, "has_balcony": 1, "has_hotwater": 1, "cost_per_year": "1200元", "area": "约30㎡", "facilities": "独立卫浴、空调、阳台、洗衣机、电梯", "note": "清水河校区条件很好"},
    {"university": "西南交通大学", "campus": "犀浦校区", "room_type": "四人间", "bed_count": 4, "has_ac": 1, "has_bathroom": 1, "has_balcony": 1, "has_hotwater": 1, "cost_per_year": "1200元", "area": "约28㎡", "facilities": "独立卫浴、空调、阳台、洗衣机", "note": "犀浦校区较新"},
    {"university": "大连理工大学", "campus": "主校区", "room_type": "四人间", "bed_count": 4, "has_ac": 1, "has_bathroom": 1, "has_balcony": 1, "has_hotwater": 1, "cost_per_year": "1200元", "area": "约28㎡", "facilities": "独立卫浴、空调、阳台、洗衣机", "note": "西山宿舍区条件好"},
    {"university": "东北大学", "campus": "南湖校区", "room_type": "四人间", "bed_count": 4, "has_ac": 1, "has_bathroom": 0, "has_balcony": 0, "has_hotwater": 1, "cost_per_year": "1000元", "area": "约22㎡", "facilities": "公共卫浴、空调、暖气、洗衣机", "note": "沈阳冬天有暖气"},
    {"university": "吉林大学", "campus": "前卫南区", "room_type": "四人间/六人间", "bed_count": 4, "has_ac": 0, "has_bathroom": 0, "has_balcony": 0, "has_hotwater": 1, "cost_per_year": "800-1200元", "area": "约20-25㎡", "facilities": "公共卫浴、暖气、洗衣机", "note": "长春有暖气不需要空调"},
    {"university": "西北工业大学", "campus": "长安校区", "room_type": "四人间", "bed_count": 4, "has_ac": 1, "has_bathroom": 1, "has_balcony": 1, "has_hotwater": 1, "cost_per_year": "1200元", "area": "约28㎡", "facilities": "独立卫浴、空调、阳台、洗衣机", "note": "长安校区条件好"},
    {"university": "重庆大学", "campus": "虎溪校区", "room_type": "四人间", "bed_count": 4, "has_ac": 1, "has_bathroom": 1, "has_balcony": 1, "has_hotwater": 1, "cost_per_year": "1200元", "area": "约30㎡", "facilities": "独立卫浴、空调、阳台、洗衣机、电梯", "note": "虎溪校区条件很好"},
    {"university": "郑州大学", "campus": "主校区", "room_type": "四人间/六人间", "bed_count": 4, "has_ac": 1, "has_bathroom": 0, "has_balcony": 0, "has_hotwater": 1, "cost_per_year": "800-1200元", "area": "约20-25㎡", "facilities": "公共卫浴、空调、洗衣机", "note": "不同宿舍区条件不同"},
    {"university": "南昌大学", "campus": "前湖校区", "room_type": "四人间", "bed_count": 4, "has_ac": 1, "has_bathroom": 1, "has_balcony": 1, "has_hotwater": 1, "cost_per_year": "1200元", "area": "约28㎡", "facilities": "独立卫浴、空调、阳台、洗衣机", "note": "前湖校区宿舍条件好"},
    {"university": "云南大学", "campus": "呈贡校区", "room_type": "四人间", "bed_count": 4, "has_ac": 0, "has_bathroom": 1, "has_balcony": 1, "has_hotwater": 1, "cost_per_year": "1200元", "area": "约28㎡", "facilities": "独立卫浴、阳台、洗衣机", "note": "昆明气候好不需要空调"},
    {"university": "贵州大学", "campus": "花溪校区", "room_type": "四人间", "bed_count": 4, "has_ac": 0, "has_bathroom": 1, "has_balcony": 1, "has_hotwater": 1, "cost_per_year": "1200元", "area": "约28㎡", "facilities": "独立卫浴、阳台、洗衣机", "note": "贵阳气候宜人"},
    {"university": "海南大学", "campus": "海甸校区", "room_type": "四人间", "bed_count": 4, "has_ac": 1, "has_bathroom": 1, "has_balcony": 1, "has_hotwater": 1, "cost_per_year": "1200元", "area": "约28㎡", "facilities": "独立卫浴、空调、阳台、洗衣机", "note": "海口热必须有空调"},
    {"university": "广西大学", "campus": "主校区", "room_type": "四人间", "bed_count": 4, "has_ac": 1, "has_bathroom": 1, "has_balcony": 1, "has_hotwater": 1, "cost_per_year": "1200元", "area": "约28㎡", "facilities": "独立卫浴、空调、阳台、洗衣机", "note": "宿舍条件在改善中"},
    {"university": "内蒙古大学", "campus": "主校区", "room_type": "四人间/六人间", "bed_count": 4, "has_ac": 0, "has_bathroom": 0, "has_balcony": 0, "has_hotwater": 1, "cost_per_year": "800元", "area": "约20㎡", "facilities": "公共卫浴、暖气、洗衣机", "note": "呼和浩特冬天有暖气"},
    {"university": "新疆大学", "campus": "红湖校区", "room_type": "四人间/六人间", "bed_count": 4, "has_ac": 0, "has_bathroom": 0, "has_balcony": 0, "has_hotwater": 1, "cost_per_year": "800元", "area": "约20㎡", "facilities": "公共卫浴、暖气、洗衣机", "note": "乌鲁木齐冬天有暖气"},
    {"university": "宁夏大学", "campus": "主校区", "room_type": "四人间", "bed_count": 4, "has_ac": 0, "has_bathroom": 0, "has_balcony": 0, "has_hotwater": 1, "cost_per_year": "800元", "area": "约20㎡", "facilities": "公共卫浴、暖气、洗衣机", "note": "银川冬天有暖气"},
    {"university": "青海大学", "campus": "主校区", "room_type": "四人间/六人间", "bed_count": 4, "has_ac": 0, "has_bathroom": 0, "has_balcony": 0, "has_hotwater": 1, "cost_per_year": "800元", "area": "约20㎡", "facilities": "公共卫浴、暖气、洗衣机", "note": "西宁冬天有暖气"},
    {"university": "西藏大学", "campus": "纳金校区", "room_type": "四人间/六人间", "bed_count": 4, "has_ac": 0, "has_bathroom": 0, "has_balcony": 0, "has_hotwater": 1, "cost_per_year": "800元", "area": "约20㎡", "facilities": "公共卫浴、暖气、洗衣机", "note": "拉萨冬天有暖气"},
]

new_trans = [
    {"university": "中国人民大学", "campus": "主校区", "location_type": "市区", "nearest_metro": "人大站（4号线）", "metro_distance": "步行5分钟", "nearest_bus": "人民大学站", "bus_distance": "步行3分钟", "to_center": "地铁20分钟到天安门", "to_station": "地铁30分钟到北京站", "to_airport": "打车40分钟到首都机场", "nearby_malls": "中关村、当代商城", "nearby_hospital": "海淀医院", "note": "海淀区，交通便利"},
    {"university": "华东师范大学", "campus": "闵行校区", "location_type": "郊区", "nearest_metro": "华东师大站（15号线）", "metro_distance": "步行10分钟", "nearest_bus": "华东师大站", "bus_distance": "步行3分钟", "to_center": "地铁45分钟到人民广场", "to_station": "地铁50分钟到上海站", "to_airport": "打车30分钟到虹桥机场", "nearby_malls": "吴泾宝龙广场", "nearby_hospital": "第五人民医院", "note": "闵行区"},
    {"university": "电子科技大学", "campus": "清水河校区", "location_type": "郊区", "nearest_metro": "电子科大站（6号线）", "metro_distance": "步行5分钟", "nearest_bus": "电子科大站", "bus_distance": "步行3分钟", "to_center": "地铁30分钟到天府广场", "to_station": "地铁40分钟到成都站", "to_airport": "打车30分钟到双流机场", "nearby_malls": "龙湖时代天街", "nearby_hospital": "省人民医院", "note": "高新区"},
    {"university": "中南大学", "campus": "主校区", "location_type": "市区", "nearest_metro": "中南大学站（3号线）", "metro_distance": "步行5分钟", "nearest_bus": "中南大学站", "bus_distance": "步行3分钟", "to_center": "地铁15分钟到五一广场", "to_station": "地铁25分钟到长沙站", "to_airport": "打车40分钟到黄花机场", "nearby_malls": "步步高广场", "nearby_hospital": "湘雅医院", "note": "岳麓区大学城"},
    {"university": "大连理工大学", "campus": "主校区", "location_type": "市区", "nearest_metro": "大连理工站（1号线）", "metro_distance": "步行10分钟", "nearest_bus": "理工大学站", "bus_distance": "步行3分钟", "to_center": "地铁20分钟到青泥洼桥", "to_station": "地铁30分钟到大连站", "to_airport": "打车20分钟到周水子机场", "nearby_malls": "万达广场", "nearby_hospital": "大医附属医院", "note": "凌水河畔"},
    {"university": "吉林大学", "campus": "前卫南区", "location_type": "市区", "nearest_metro": "卫星广场站（1号线）", "metro_distance": "步行10分钟", "nearest_bus": "吉大南校站", "bus_distance": "步行3分钟", "to_center": "地铁15分钟到人民广场", "to_station": "地铁25分钟到长春站", "to_airport": "打车40分钟到龙嘉机场", "nearby_malls": "欧亚商都", "nearby_hospital": "吉大一院", "note": "长春市中心"},
    {"university": "重庆大学", "campus": "虎溪校区", "location_type": "郊区", "nearest_metro": "大学城站（1号线）", "metro_distance": "步行10分钟", "nearest_bus": "重庆大学站", "bus_distance": "步行3分钟", "to_center": "地铁40分钟到解放碑", "to_station": "地铁50分钟到重庆站", "to_airport": "打车40分钟到江北机场", "nearby_malls": "熙街、龙湖U城", "nearby_hospital": "大学城医院", "note": "沙坪坝大学城"},
    {"university": "郑州大学", "campus": "主校区", "location_type": "郊区", "nearest_metro": "郑大科技园站（1号线）", "metro_distance": "步行10分钟", "nearest_bus": "郑州大学站", "bus_distance": "步行3分钟", "to_center": "地铁30分钟到二七广场", "to_station": "地铁40分钟到郑州站", "to_airport": "打车40分钟到新郑机场", "nearby_malls": "万达广场", "nearby_hospital": "郑大一附院", "note": "高新区大学城"},
    {"university": "云南大学", "campus": "呈贡校区", "location_type": "郊区", "nearest_metro": "大学城站（1号线）", "metro_distance": "步行15分钟", "nearest_bus": "云大呈贡校区站", "bus_distance": "步行3分钟", "to_center": "地铁40分钟到东风广场", "to_station": "地铁50分钟到昆明站", "to_airport": "打车40分钟到长水机场", "nearby_malls": "呈贡吾悦广场", "nearby_hospital": "呈贡区医院", "note": "呈贡大学城"},
]

existing_unis = {d["university"] for d in data["dormitory"]}
for d in new_dorms:
    if d["university"] not in existing_unis:
        data["dormitory"].append(d)

existing_trans = {t["university"] for t in data["transport"]}
for t in new_trans:
    if t["university"] not in existing_trans:
        data["transport"].append(t)

with open(SEED_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"宿舍数据: {len(data['dormitory'])} 条")
print(f"交通数据: {len(data['transport'])} 条")
