import json
import sqlite3
from typing import Dict, Any, Optional
from app.storage.base import Store

class SQLiteStore(Store):
    def __init__(self, db_path: str = "sqlite.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS contexts (
                    scope TEXT,
                    context_id TEXT,
                    payload TEXT,
                    version INTEGER,
                    timestamp TEXT,
                    PRIMARY KEY (scope, context_id)
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS conversation_state (
                    merchant_id TEXT PRIMARY KEY,
                    state TEXT
                )
            ''')

    def save_context(self, scope: str, context_id: str, payload: Dict[str, Any], version: int, timestamp: str) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT version FROM contexts WHERE scope = ? AND context_id = ?", (scope, context_id))
            row = cursor.fetchone()
            if row and row[0] >= version:
                return False # Ignore older or same version
            
            cursor.execute('''
                INSERT OR REPLACE INTO contexts (scope, context_id, payload, version, timestamp)
                VALUES (?, ?, ?, ?, ?)
            ''', (scope, context_id, json.dumps(payload), version, timestamp))
            return True

    def get_context(self, scope: str, context_id: str) -> Optional[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT payload FROM contexts WHERE scope = ? AND context_id = ?", (scope, context_id))
            row = cursor.fetchone()
            if row:
                return json.loads(row[0])
            return None

    def save_conversation_state(self, merchant_id: str, state: str) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT OR REPLACE INTO conversation_state (merchant_id, state)
                VALUES (?, ?)
            ''', (merchant_id, state))

    def get_conversation_state(self, merchant_id: str) -> str:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT state FROM conversation_state WHERE merchant_id = ?", (merchant_id,))
            row = cursor.fetchone()
            if row:
                return row[0]
            return "Idle"

    # Maintain backward compatibility with old code if any still exists
    def save_merchant_context(self, merchant_id: str, payload: Dict[str, Any], version: int, timestamp: str) -> bool:
        return self.save_context("merchant", merchant_id, payload, version, timestamp)

    def get_merchant_context(self, merchant_id: str) -> Optional[Dict[str, Any]]:
        return self.get_context("merchant", merchant_id)

    def save_customer_context(self, customer_id: str, payload: Dict[str, Any], version: int, timestamp: str) -> bool:
        return self.save_context("customer", customer_id, payload, version, timestamp)

    def get_customer_context(self, customer_id: str) -> Optional[Dict[str, Any]]:
        return self.get_context("customer", customer_id)
