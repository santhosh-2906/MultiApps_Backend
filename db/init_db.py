from .connection import get_db_connection

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ub_users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(100) NOT NULL
        )
    """)

    # Todo table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ub_todos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            task VARCHAR(255) NOT NULL,
            status VARCHAR(20) DEFAULT 'pending',
            FOREIGN KEY (user_id) REFERENCES ub_users(id) ON DELETE CASCADE
        )
    """)

    # Notes table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ub_notes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            title VARCHAR(100),
            content TEXT,
            FOREIGN KEY (user_id) REFERENCES ub_users(id) ON DELETE CASCADE
        )
    """)

    # Expenses table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ub_expenses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            amount DECIMAL(10,2) NOT NULL,
            category VARCHAR(50),
            note VARCHAR(255),
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES ub_users(id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    init_db()
    print(" Database initialized with required tables.")
