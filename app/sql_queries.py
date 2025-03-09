def select_by_tlg_id():
    return "SELECT id, nic FROM warrior WHERE tlg_id = %s"

def create_table_warrior():
    return """
        CREATE TABLE IF NOT EXISTS warrior (
            id SERIAL PRIMARY KEY,
            tlg_id VARCHAR(32) NOT NULL,
            nic VARCHAR(25) NOT NULL
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

def insert_new_warrior_to_db():
    return """
        INSERT INTO warrior (tlg_id, nic)
        VALUES (%s, %s)
    """