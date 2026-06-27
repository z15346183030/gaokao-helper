import sqlite3
import os


DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "db", "data.db")

ALLOWED_DORMITORY_FIELDS = {"university", "campus", "room_type", "has_ac", "has_bathroom", "has_balcony", "has_hotwater", "cost_per_year", "bed_count", "area", "facilities", "rating", "note"}
ALLOWED_TRANSPORT_FIELDS = {"university", "campus", "nearest_metro", "metro_distance", "nearest_bus", "bus_distance", "to_center", "to_station", "to_airport", "location_type", "nearby_malls", "nearby_hospital", "note"}


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dormitory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            university TEXT NOT NULL,
            campus TEXT DEFAULT '',
            room_type TEXT DEFAULT '',
            has_ac INTEGER DEFAULT 0,
            has_bathroom INTEGER DEFAULT 0,
            has_balcony INTEGER DEFAULT 0,
            has_hotwater INTEGER DEFAULT 0,
            cost_per_year TEXT DEFAULT '',
            bed_count INTEGER DEFAULT 0,
            area TEXT DEFAULT '',
            facilities TEXT DEFAULT '',
            rating TEXT DEFAULT '',
            note TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transport (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            university TEXT NOT NULL,
            campus TEXT DEFAULT '',
            nearest_metro TEXT DEFAULT '',
            metro_distance TEXT DEFAULT '',
            nearest_bus TEXT DEFAULT '',
            bus_distance TEXT DEFAULT '',
            to_center TEXT DEFAULT '',
            to_station TEXT DEFAULT '',
            to_airport TEXT DEFAULT '',
            location_type TEXT DEFAULT '',
            nearby_malls TEXT DEFAULT '',
            nearby_hospital TEXT DEFAULT '',
            note TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# ===== 宿舍 CRUD =====

def get_dormitory(university_name):
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM dormitory WHERE university = ? ORDER BY id",
        (university_name,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_dormitory(data):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO dormitory (university, campus, room_type, has_ac, has_bathroom,
            has_balcony, has_hotwater, cost_per_year, bed_count, area, facilities, rating, note)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("university", ""),
        data.get("campus", ""),
        data.get("room_type", ""),
        data.get("has_ac", 0),
        data.get("has_bathroom", 0),
        data.get("has_balcony", 0),
        data.get("has_hotwater", 0),
        data.get("cost_per_year", ""),
        data.get("bed_count", 0),
        data.get("area", ""),
        data.get("facilities", ""),
        data.get("rating", ""),
        data.get("note", ""),
    ))
    conn.commit()
    dorm_id = cursor.lastrowid
    conn.close()
    return dorm_id


def update_dormitory(dorm_id, data):
    filtered = {k: v for k, v in data.items() if k in ALLOWED_DORMITORY_FIELDS}
    conn = get_conn()
    fields = []
    values = []
    for key in ["campus", "room_type", "has_ac", "has_bathroom", "has_balcony",
                 "has_hotwater", "cost_per_year", "bed_count", "area", "facilities",
                 "rating", "note"]:
        if key in filtered:
            fields.append(f"{key} = ?")
            values.append(filtered[key])
    if fields:
        fields.append("updated_at = CURRENT_TIMESTAMP")
        values.append(dorm_id)
        conn.execute(f"UPDATE dormitory SET {', '.join(fields)} WHERE id = ?", values)
        conn.commit()
    conn.close()


def delete_dormitory(dorm_id):
    conn = get_conn()
    conn.execute("DELETE FROM dormitory WHERE id = ?", (dorm_id,))
    conn.commit()
    conn.close()


# ===== 交通 CRUD =====

def get_transport(university_name):
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM transport WHERE university = ? ORDER BY id",
        (university_name,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_transport(data):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO transport (university, campus, nearest_metro, metro_distance,
            nearest_bus, bus_distance, to_center, to_station, to_airport,
            location_type, nearby_malls, nearby_hospital, note)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("university", ""),
        data.get("campus", ""),
        data.get("nearest_metro", ""),
        data.get("metro_distance", ""),
        data.get("nearest_bus", ""),
        data.get("bus_distance", ""),
        data.get("to_center", ""),
        data.get("to_station", ""),
        data.get("to_airport", ""),
        data.get("location_type", ""),
        data.get("nearby_malls", ""),
        data.get("nearby_hospital", ""),
        data.get("note", ""),
    ))
    conn.commit()
    trans_id = cursor.lastrowid
    conn.close()
    return trans_id


def update_transport(trans_id, data):
    filtered = {k: v for k, v in data.items() if k in ALLOWED_TRANSPORT_FIELDS}
    conn = get_conn()
    fields = []
    values = []
    for key in ["campus", "nearest_metro", "metro_distance", "nearest_bus",
                 "bus_distance", "to_center", "to_station", "to_airport",
                 "location_type", "nearby_malls", "nearby_hospital", "note"]:
        if key in filtered:
            fields.append(f"{key} = ?")
            values.append(filtered[key])
    if fields:
        fields.append("updated_at = CURRENT_TIMESTAMP")
        values.append(trans_id)
        conn.execute(f"UPDATE transport SET {', '.join(fields)} WHERE id = ?", values)
        conn.commit()
    conn.close()


def delete_transport(trans_id):
    conn = get_conn()
    conn.execute("DELETE FROM transport WHERE id = ?", (trans_id,))
    conn.commit()
    conn.close()


# ===== 统计 =====

def get_stats():
    conn = get_conn()
    dorm_count = conn.execute("SELECT COUNT(*) FROM dormitory").fetchone()[0]
    trans_count = conn.execute("SELECT COUNT(*) FROM transport").fetchone()[0]
    dorm_unis = conn.execute("SELECT COUNT(DISTINCT university) FROM dormitory").fetchone()[0]
    trans_unis = conn.execute("SELECT COUNT(DISTINCT university) FROM transport").fetchone()[0]
    conn.close()
    return {
        "dormitory_count": dorm_count,
        "transport_count": trans_count,
        "dormitory_universities": dorm_unis,
        "transport_universities": trans_unis,
    }
