import sqlite3
from datetime import datetime
from typing import List, Tuple, Optional
import json

class Database:
    def __init__(self, db_path: str = "conversations.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialise la base de données avec les tables nécessaires"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Table des sessions
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    system_prompt TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Table des messages
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    role TEXT,
                    content TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES sessions (session_id)
                )
            """)
            
            conn.commit()

    def create_or_update_session(self, session_id: str, system_prompt: str):
        """Crée ou met à jour une session"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO sessions (session_id, system_prompt, last_updated)
                VALUES (?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(session_id) DO UPDATE SET
                    system_prompt = excluded.system_prompt,
                    last_updated = CURRENT_TIMESTAMP
            """, (session_id, system_prompt))
            conn.commit()

    def add_message(self, session_id: str, role: str, content: str):
        """Ajoute un message à l'historique"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO messages (session_id, role, content)
                VALUES (?, ?, ?)
            """, (session_id, role, content))
            conn.commit()

    def get_session_history(self, session_id: str) -> List[Tuple[str, str]]:
        """Récupère l'historique des messages d'une session"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT role, content FROM messages
                WHERE session_id = ?
                ORDER BY timestamp
            """, (session_id,))
            return cursor.fetchall()

    def get_system_prompt(self, session_id: str) -> Optional[str]:
        """Récupère le prompt système d'une session"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT system_prompt FROM sessions
                WHERE session_id = ?
            """, (session_id,))
            result = cursor.fetchone()
            return result[0] if result else None

    def delete_session(self, session_id: str):
        """Supprime une session et son historique"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
            cursor.execute("DELETE FROM sessions WHERE session_id = ?", (session_id,))
            conn.commit()

    def list_sessions(self) -> List[Tuple[str, str, str]]:
        """Liste toutes les sessions avec leur dernière mise à jour"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT session_id, system_prompt, last_updated
                FROM sessions
                ORDER BY last_updated DESC
            """)
            return cursor.fetchall()