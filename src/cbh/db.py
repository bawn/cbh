import sqlite3

def initialize_db():
    conn = get_connection()
    create_tables()
    conn.commit()
    conn.close()


def check_db_exists():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='metrics'")
        table_exists = cursor.fetchone() is not None
        conn.close()
        return table_exists
    except sqlite3.Error as e:
        print(f"Error checking database existence: {e}")
        return False

def get_connection():
    return sqlite3.connect("data.db")

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )
    """)

    cursor.execute("""
    CREATE TABLE data_points (
        metric_id INTEGER,
        year INTEGER,
        value REAL,
        FOREIGN KEY(metric_id) REFERENCES metrics(id),
        PRIMARY KEY (metric_id, year)
    )
    """)

def fetch_years(cursor):
    cursor.execute("SELECT DISTINCT year FROM data_points ORDER BY year")
    years = [row[0] for row in cursor.fetchall()]
    return years

def fetch_metrics(cursor):
    cursor.execute("SELECT name FROM metrics")
    metrics = [row[0] for row in cursor.fetchall()]
    return metrics

def fetch_metric_data(cursor, metric_name):
    cursor.execute("""
        SELECT dp.year, dp.value
        FROM data_points dp
        JOIN metrics m ON dp.metric_id = m.id
        WHERE m.name = ?
        ORDER BY dp.year
    """, (metric_name,))
    data = cursor.fetchall()
    return data
def fetch_all_metrics(cursor):
    cursor.execute("SELECT name FROM metrics")
    metrics = [row[0] for row in cursor.fetchall()]
    return metrics

def insert_metric(cursor, name):
    
    try:
        cursor.execute("INSERT OR IGNORE INTO metrics (name) VALUES (?)", (name,))

    except sqlite3.Error as e:
        print(f"Error occurred while inserting metric: {e}")

    cursor.execute("SELECT id FROM metrics WHERE name=?", (name,))

    return cursor.fetchone()[0]

def insert_data(cursor, metric, year, value):

    metric_id = insert_metric(cursor, metric)

    print(f"Inserting data: Metric='{metric}', Year={year}, Value={value}")
    cursor.execute("""
        INSERT INTO data_points (metric_id, year, value)
        VALUES (?, ?, ?)
        ON CONFLICT(metric_id, year)
        DO UPDATE SET value = excluded.value
    """, (metric_id, year, value))



def save_to_db(year, 
                grain_received_list, 
                aifr_list, 
                fertiliser_list, 
                revenue_list, 
                pool_revenue_list, 
                othergains_and_losses_list, 
                total_revenue_list):
    
    conn = get_connection()
    cursor = conn.cursor()

    temp_year_list = [year] * len(grain_received_list)
    year_list = [x - i for i, x in enumerate(temp_year_list)]

    for value in grain_received_list:
        year = year_list[grain_received_list.index(value)]
        insert_data(cursor, "Tonnes received", year, float(value))

    for value in aifr_list:
        year = year_list[aifr_list.index(value)]
        insert_data(cursor, "AIFR", year, float(value))
    
    for value in fertiliser_list:
        year = year_list[fertiliser_list.index(value)]
        insert_data(cursor, "Fertiliser tonnes outturned", year, float(value.replace(",", "")))
    
    for value in revenue_list:
        year = year_list[revenue_list.index(value)]
        insert_data(cursor, "Revenue from continuing operations", year, float(value.replace(",", "")))
    
    for value in pool_revenue_list:
        year = year_list[pool_revenue_list.index(value)]
        insert_data(cursor, "Pools revenue", year, float(value.replace(",", "")))
    
    for value in othergains_and_losses_list:
        year = year_list[othergains_and_losses_list.index(value)]
        insert_data(cursor, "Other gains and losses", year, float(value))
    
    for value in total_revenue_list:
        year = year_list[total_revenue_list.index(value)]
        insert_data(cursor, "Total revenue including other income", year, float(value.replace(",", "")))
    
    conn.commit()
    conn.close()


# id | name
# ---|-------------------------------
# 1  | Tonnes received
# 2  | AIFR
# 3  | Fertiliser tonnes outturned
# 4  | Revenue


# id | metric_id | year | value
# ---|-----------|------|------
# 1  | 1         | 2025 | 20.4
# 2  | 1         | 2024 | 12.5
# 3  | 2         | 2025 | 4.5