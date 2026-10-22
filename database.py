"""
AI-Based Smart Waste Segregation and Classification System
SQLite Database Management Module

Handles:
- Classification records persistence
- History retrieval
- Aggregated statistics computation
- History deletion with safety
"""

import os
import sqlite3
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

# Canonical 5 categories required by project specifications
CANONICAL_CATEGORIES = ["Plastic", "Paper", "Metal", "Glass", "Organic"]


def get_db_connection():
    """Create and return a thread-safe connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database schema if tables do not exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS classifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            confidence REAL NOT NULL,
            image_filename TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()
    logger.info("SQLite database initialized at: %s", DB_PATH)


def normalize_category_name(category: str) -> str:
    """
    Normalize category names so that 'Organic Waste' and 'Organic'
    map to the standard 5 categories (Plastic, Paper, Metal, Glass, Organic).
    """
    cat = (category or "").strip()
    if cat.lower() in ["organic waste", "organic"]:
        return "Organic"
    for canonical in ["Plastic", "Paper", "Metal", "Glass"]:
        if cat.lower() == canonical.lower():
            return canonical
    return cat


def insert_classification(category: str, confidence: float, image_filename: str = None) -> int:
    """
    Save a successful classification record.
    Returns the newly created record ID.
    Only called for real, validated model predictions.
    """
    norm_cat = normalize_category_name(category)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO classifications (category, confidence, image_filename, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (norm_cat, round(float(confidence), 2), image_filename, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    logger.info("Saved classification #%d: %s (%.2f%%)", new_id, norm_cat, confidence)
    return new_id


def get_all_classifications(limit: int = 200):
    """
    Retrieve classification history ordered newest first.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, category, confidence, image_filename, created_at
        FROM classifications
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,)
    )
    rows = cursor.fetchall()
    conn.close()

    records = []
    for row in rows:
        records.append({
            "id": row["id"],
            "category": row["category"],
            "confidence": round(float(row["confidence"]), 2),
            "image_filename": row["image_filename"],
            "created_at": row["created_at"]
        })
    return records


def get_classification_stats():
    """
    Compute real-time statistics strictly from actual database records:
    - Total classifications
    - Count per category (Plastic, Paper, Metal, Glass, Organic)
    - Percentage distribution
    Returns 0 when there are no records (never hardcoded or fabricated).
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) AS total FROM classifications")
    total_row = cursor.fetchone()
    total = total_row["total"] if total_row else 0

    counts = {cat: 0 for cat in CANONICAL_CATEGORIES}
    percentages = {cat: 0.0 for cat in CANONICAL_CATEGORIES}

    cursor.execute("SELECT category, COUNT(*) as count FROM classifications GROUP BY category")
    grouped = cursor.fetchall()
    conn.close()

    for row in grouped:
        cat_norm = normalize_category_name(row["category"])
        if cat_norm in counts:
            counts[cat_norm] += int(row["count"])
        else:
            counts[cat_norm] = int(row["count"])

    if total > 0:
        for cat in CANONICAL_CATEGORIES:
            percentages[cat] = round((counts[cat] / total) * 100, 1)

    return {
        "total": total,
        "counts": counts,
        "percentages": percentages,
        "categories": CANONICAL_CATEGORIES
    }


def clear_all_classifications():
    """
    Clear all records from classification history.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM classifications")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='classifications'")
    conn.commit()
    cursor.execute("VACUUM")
    conn.commit()
    conn.close()
    logger.info("Cleared all classification history records.")
    return True
