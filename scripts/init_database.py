"""Setup database and create tables supporting MySQL and SQLite."""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def get_db_type():
    """Get database type from environment."""
    return os.getenv("DB_TYPE", "sqlite").lower()


def create_sqlite_database():
    """Create SQLite database and tables."""
    try:
        import aiosqlite

        db_path = os.getenv("DB_PATH", "data/telegram_chatbot.db")

        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(db_path) if os.path.dirname(db_path) else ".", exist_ok=True)

        async def create_tables():
            async with aiosqlite.connect(db_path) as conn:
                # Enable foreign keys
                await conn.execute("PRAGMA foreign_keys = ON")
                await conn.execute("PRAGMA journal_mode = WAL")

                # Create users table
                await conn.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY,
                        username TEXT,
                        first_name TEXT NOT NULL,
                        last_name TEXT,
                        language_code TEXT,
                        is_bot INTEGER DEFAULT 0,
                        is_premium INTEGER DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                # Create index for username
                await conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_username ON users(username)
                """)
                print("Table 'users' created")

                # Create conversations table
                await conn.execute("""
                    CREATE TABLE IF NOT EXISTS conversations (
                        conversation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        group_id INTEGER,
                        role TEXT NOT NULL,
                        content TEXT NOT NULL,
                        timestamp TIMESTAMP NOT NULL,
                        message_id INTEGER,
                        style_id INTEGER,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                    )
                """)
                # Create indexes
                await conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_user_id ON conversations(user_id)
                """)
                await conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_group_id ON conversations(group_id)
                """)
                await conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_timestamp ON conversations(timestamp)
                """)
                print("Table 'conversations' created")

                # Create conversation_vectors table
                await conn.execute("""
                    CREATE TABLE IF NOT EXISTS conversation_vectors (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        conversation_id INTEGER NOT NULL,
                        vector BLOB NOT NULL,
                        vector_id TEXT NOT NULL UNIQUE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (conversation_id) REFERENCES conversations(conversation_id) ON DELETE CASCADE
                    )
                """)
                # Create indexes
                await conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_conversation_id ON conversation_vectors(conversation_id)
                """)
                await conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_vector_id ON conversation_vectors(vector_id)
                """)
                print("Table 'conversation_vectors' created")

                # Create group_settings table
                await conn.execute("""
                    CREATE TABLE IF NOT EXISTS group_settings (
                        group_id INTEGER PRIMARY KEY,
                        style_id INTEGER NOT NULL DEFAULT 1,
                        welcome_message TEXT,
                        auto_reply_enabled INTEGER DEFAULT 1,
                        language TEXT DEFAULT 'zh-CN',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        CHECK (style_id BETWEEN 1 AND 6)
                    )
                """)
                print("Table 'group_settings' created")

                # Create user_preferences table
                await conn.execute("""
                    CREATE TABLE IF NOT EXISTS user_preferences (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL UNIQUE,
                        style_id INTEGER NOT NULL DEFAULT 1,
                        language TEXT DEFAULT 'zh-CN',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                        CHECK (style_id BETWEEN 1 AND 6)
                    )
                """)
                print("Table 'user_preferences' created")

                await conn.commit()
                print("\nAll tables created successfully!")

        import asyncio
        asyncio.run(create_tables())
        return True

    except Exception as e:
        print(f"Error creating SQLite database: {e}")
        import traceback
        traceback.print_exc()
        return False


def create_mysql_database():
    """Create MySQL database and tables."""
    try:
        import pymysql

        # Create database
        conn = pymysql.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', '')
        )
        cursor = conn.cursor()

        cursor.execute("""
            CREATE DATABASE IF NOT EXISTS telegram_chatbot
            CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
        """)
        conn.commit()
        print("Database 'telegram_chatbot' created or already exists")
        conn.close()

        # Create tables
        conn = pymysql.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'telegram_chatbot')
        )
        cursor = conn.cursor()

        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id BIGINT PRIMARY KEY,
                username VARCHAR(255),
                first_name VARCHAR(255) NOT NULL,
                last_name VARCHAR(255),
                language_code VARCHAR(10),
                is_bot BOOLEAN DEFAULT FALSE,
                is_premium BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_username (username)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("Table 'users' created")

        # Create conversations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                conversation_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id BIGINT NOT NULL,
                group_id BIGINT,
                role VARCHAR(20) NOT NULL,
                content TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
                message_id BIGINT,
                style_id INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                INDEX idx_user_id (user_id),
                INDEX idx_group_id (group_id),
                INDEX idx_timestamp (timestamp)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("Table 'conversations' created")

        # Create conversation_vectors table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversation_vectors (
                id INT AUTO_INCREMENT PRIMARY KEY,
                conversation_id INT NOT NULL,
                vector BLOB NOT NULL,
                vector_id VARCHAR(255) NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (conversation_id) REFERENCES conversations(conversation_id) ON DELETE CASCADE,
                INDEX idx_conversation_id (conversation_id),
                INDEX idx_vector_id (vector_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("Table 'conversation_vectors' created")

        # Create group_settings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS group_settings (
                group_id BIGINT PRIMARY KEY,
                style_id INT NOT NULL DEFAULT 1,
                welcome_message TEXT,
                auto_reply_enabled BOOLEAN DEFAULT TRUE,
                language VARCHAR(10) DEFAULT 'zh-CN',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                CONSTRAINT chk_style_id CHECK (style_id BETWEEN 1 AND 6)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("Table 'group_settings' created")

        # Create user_preferences table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_preferences (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id BIGINT NOT NULL UNIQUE,
                style_id INT NOT NULL DEFAULT 1,
                language VARCHAR(10) DEFAULT 'zh-CN',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                CONSTRAINT chk_user_style_id CHECK (style_id BETWEEN 1 AND 6)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("Table 'user_preferences' created")

        conn.commit()
        print("\nAll tables created successfully!")
        conn.close()
        return True

    except Exception as e:
        print(f"Error creating MySQL database: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    db_type = get_db_type()

    print(f"Setting up {db_type.upper()} database...")
    print("-" * 40)

    if db_type == "mysql":
        print(f"Host: {os.getenv('DB_HOST')}")
        print(f"Port: {os.getenv('DB_PORT')}")
        print(f"User: {os.getenv('DB_USER')}")
        print(f"Database: {os.getenv('DB_NAME')}")
        print("-" * 40)
        create_mysql_database()
    else:  # sqlite
        print(f"Path: {os.getenv('DB_PATH', 'data/telegram_chatbot.db')}")
        print("-" * 40)
        create_sqlite_database()
