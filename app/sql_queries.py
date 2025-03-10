def select_by_tlg_id(table_name):
    return f"SELECT id, nic FROM {table_name} WHERE tlg_id = %s"

def select_all_users(table_name):
    return f"SELECT tlg_id, nic FROM {table_name}"

def create_table_warrior():
    return """
        CREATE TABLE IF NOT EXISTS warrior (
            id SERIAL PRIMARY KEY,
            tlg_id VARCHAR(32) NOT NULL,
            nic VARCHAR(25) NOT NULL
        )
    """

def create_table_candidate():
    return """
        CREATE TABLE IF NOT EXISTS candidate (
            id SERIAL PRIMARY KEY,
            tlg_id VARCHAR(32) NOT NULL,
            nic VARCHAR(25) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """

def create_table_banned():
    return """
        CREATE TABLE IF NOT EXISTS banned (
            id SERIAL PRIMARY KEY,
            tlg_id VARCHAR(32) NOT NULL,
            nic VARCHAR(25) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """

def create_table_cash_check():
    return """
        CREATE TABLE IF NOT EXISTS cash_check (
            id SERIAL PRIMARY KEY,
            warrior_id INT NOT NULL,
            image_url TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            amount DECIMAL(10,2) NOT NULL,
            CONSTRAINT fk_warrior FOREIGN KEY (warrior_id) REFERENCES warrior (id) ON DELETE CASCADE
        )
    """

def create_table_cash_back():
    return """
        CREATE TABLE IF NOT EXISTS cash_back (
            id SERIAL PRIMARY KEY,
            warrior_id INT NOT NULL,
            image_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            amount DECIMAL(10,2) NOT NULL,
            CONSTRAINT fk_warrior FOREIGN KEY (warrior_id) REFERENCES warrior (id) ON DELETE CASCADE
        )
    """

def insert_new_user_to_db(table_name):
    return (
            f"INSERT INTO {table_name} (tlg_id, nic)"
            f"VALUES (%s, %s)"
    )

def delete_by_tlg_id(table_name):
    return (
        f"DELETE FROM {table_name} WHERE tlg_id = %s;"
    )
