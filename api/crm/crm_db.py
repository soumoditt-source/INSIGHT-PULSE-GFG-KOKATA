"""
InsightPulse AI - CRM Database Module
Manages user sessions, query history, and starred dashboards using SQLite.
"""
import sqlite3
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

CRM_DB_PATH = Path(__file__).parent.parent / "data" / "crm.db"


def get_connection() -> sqlite3.Connection:
    CRM_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(CRM_DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create all CRM tables if they don't exist."""
    conn = get_connection()
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            created_at TEXT NOT NULL,
            last_active TEXT NOT NULL,
            dataset_name TEXT,
            query_count INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS query_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            user_query TEXT NOT NULL,
            generated_sql TEXT,
            chart_types TEXT,
            insights TEXT,
            error TEXT,
            duration_ms INTEGER,
            FOREIGN KEY (session_id) REFERENCES sessions(session_id)
        );

        CREATE TABLE IF NOT EXISTS starred_dashboards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            title TEXT NOT NULL,
            user_query TEXT NOT NULL,
            generated_sql TEXT,
            chart_configs TEXT,
            insights TEXT,
            starred_at TEXT NOT NULL,
            notes TEXT DEFAULT '',
            FOREIGN KEY (session_id) REFERENCES sessions(session_id)
        );

        CREATE TABLE IF NOT EXISTS faq_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            category TEXT DEFAULT 'General',
            tags TEXT DEFAULT '[]',
            created_at TEXT NOT NULL,
            views INTEGER DEFAULT 0
        );
    """)
    conn.commit()
    conn.close()


def create_session(dataset_name: str = "India Life Insurance Claims") -> str:
    """Create a new CRM session and return session_id."""
    conn = get_connection()
    sess_id = uuid.uuid4().hex[:8].upper()
    now = datetime.now().isoformat()
    conn.execute(
        "INSERT INTO sessions (session_id, created_at, last_active, dataset_name, query_count) VALUES (?, ?, ?, ?, 0)",
        (sess_id, now, now, dataset_name)
    )
    conn.commit()
    conn.close()
    return sess_id


def update_session(session_id: str):
    """Update last active timestamp and increment query count."""
    conn = get_connection()
    now = datetime.now().isoformat()
    conn.execute(
        "UPDATE sessions SET last_active=?, query_count=query_count+1 WHERE session_id=?",
        (now, session_id)
    )
    conn.commit()
    conn.close()


def log_query(session_id: str, user_query: str, generated_sql: Optional[str],
              chart_types: List[str], insights: List[str], error: Optional[str],
              duration_ms: int = 0):
    """Log a completed query to history."""
    conn = get_connection()
    now = datetime.now().isoformat()
    conn.execute(
        """INSERT INTO query_history 
           (session_id, timestamp, user_query, generated_sql, chart_types, insights, error, duration_ms)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (session_id, now, user_query, generated_sql,
         json.dumps(chart_types), json.dumps(insights), error, duration_ms)
    )
    conn.commit()
    conn.close()
    update_session(session_id)


def get_history(session_id: str, limit: int = 50) -> List[Dict]:
    """Retrieve query history for a session."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM query_history WHERE session_id=? ORDER BY timestamp DESC LIMIT ?",
        (session_id, limit)
    ).fetchall()
    conn.close()
    results = []
    for row in rows:
        r = dict(row)
        r['chart_types'] = json.loads(r.get('chart_types', '[]'))
        r['insights'] = json.loads(r.get('insights', '[]'))
        results.append(r)
    return results


def star_dashboard(session_id: str, title: str, user_query: str,
                   generated_sql: str, chart_configs: list, insights: list) -> int:
    """Star/save a dashboard."""
    conn = get_connection()
    now = datetime.now().isoformat()
    cursor = conn.execute(
        """INSERT INTO starred_dashboards 
           (session_id, title, user_query, generated_sql, chart_configs, insights, starred_at)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (session_id, title, user_query, generated_sql,
         json.dumps(chart_configs), json.dumps(insights), now)
    )
    conn.commit()
    conn.close()
    return cursor.lastrowid or 0


def get_starred(session_id: str) -> List[Dict]:
    """Get all starred dashboards for a session."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM starred_dashboards WHERE session_id=? ORDER BY starred_at DESC",
        (session_id,)
    ).fetchall()
    conn.close()
    results = []
    for row in rows:
        r = dict(row)
        r['chart_configs'] = json.loads(r.get('chart_configs', '[]'))
        r['insights'] = json.loads(r.get('insights', '[]'))
        results.append(r)
    return results


def update_notes(star_id: int, notes: str):
    """Update notes for a starred dashboard."""
    conn = get_connection()
    conn.execute("UPDATE starred_dashboards SET notes=? WHERE id=?", (notes, star_id))
    conn.commit()
    conn.close()


def delete_starred(star_id: int):
    """Remove a starred dashboard."""
    conn = get_connection()
    conn.execute("DELETE FROM starred_dashboards WHERE id=?", (star_id,))
    conn.commit()
    conn.close()


def get_session_info(session_id: str) -> Optional[Dict]:
    """Get session metadata."""
    conn = get_connection()
    row = conn.execute("SELECT * FROM sessions WHERE session_id=?", (session_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


# Initialize DB on import
init_db()
