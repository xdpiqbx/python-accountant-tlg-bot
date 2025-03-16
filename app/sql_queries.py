def select_by_tlg_id(table_name):
    return f"SELECT id, nic FROM {table_name} WHERE tlg_id = %s"


def select_all_users(table_name):
    return f"SELECT tlg_id, nic FROM {table_name}"


def select_balance_by_tlg_id():
    return f"SELECT balance FROM warrior WHERE tlg_id = %s"


def select_all_checks_for_current_user():
    return (f"SELECT id, created_at, amount "
            f"FROM cash_check "
            f"WHERE warrior_id = %s "
            f"ORDER BY amount DESC ")


def select_check_by_id():
    return (f"SELECT warrior_id, image_url, created_at, amount, comment "
            f"FROM cash_check WHERE id = %s")


def update_balance_by_tlg_id():
    return f"UPDATE warrior SET balance = %s WHERE tlg_id = %s"


def create_table_warrior():
    return """
        CREATE TABLE IF NOT EXISTS warrior (
            id SERIAL PRIMARY KEY,
            tlg_id VARCHAR(32) NOT NULL UNIQUE,
            nic VARCHAR(25) NOT NULL,
            balance INT NOT NULL DEFAULT 0.00
        )
    """


def create_table_candidate():
    return """
        CREATE TABLE IF NOT EXISTS candidate (
            id SERIAL PRIMARY KEY,
            tlg_id VARCHAR(32) NOT NULL UNIQUE,
            nic VARCHAR(25) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """


def create_table_banned():
    return """
        CREATE TABLE IF NOT EXISTS banned (
            id SERIAL PRIMARY KEY,
            tlg_id VARCHAR(32) NOT NULL UNIQUE,
            nic VARCHAR(25) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """


def create_table_cash_check():
    return """
        CREATE TABLE IF NOT EXISTS cash_check (
            id SERIAL PRIMARY KEY,
            warrior_id VARCHAR(32) NOT NULL,
            image_url TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            amount INT NOT NULL,
            comment TEXT,
            CONSTRAINT fk_warrior FOREIGN KEY (warrior_id) REFERENCES warrior (tlg_id) ON DELETE CASCADE
        )
    """


def create_table_cash_back():
    return """
        CREATE TABLE IF NOT EXISTS cash_back (
            id SERIAL PRIMARY KEY,
            warrior_id VARCHAR(32) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            amount INT NOT NULL,
            comment TEXT,
            CONSTRAINT fk_warrior FOREIGN KEY (warrior_id) REFERENCES warrior (tlg_id) ON DELETE CASCADE
        )
    """


def create_table_check_archive():
    return """
        CREATE TABLE IF NOT EXISTS check_archive (
            id SERIAL PRIMARY KEY,
            warrior_id VARCHAR(32) NOT NULL,
            image_url TEXT,
            created_at TIMESTAMP,
            amount INT NOT NULL,
            comment TEXT,
            added_to_archive TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT fk_warrior FOREIGN KEY (warrior_id) REFERENCES warrior (tlg_id) ON DELETE SET NULL
        )
    """


def insert_new_user_to_db(table_name):
    return (
        f"INSERT INTO {table_name} (tlg_id, nic)"
        f"VALUES (%s, %s)"
    )


def insert_check_to_db():
    return (
        f"INSERT INTO cash_check (warrior_id, image_url, amount, comment)"
        f"VALUES (%s, %s, %s, %s)"
    )


def insert_check_to_archive():
    return (
        f"INSERT INTO check_archive (warrior_id, image_url, created_at, amount, comment)"
        f"VALUES (%s, %s, %s, %s, %s)"
    )


def insert_refund_to_db():
    return (
        f"INSERT INTO cash_back (warrior_id, amount, comment)"
        f"VALUES (%s, %s, %s)"
    )


def delete_by_tlg_id(table_name):
    return (
        f"DELETE FROM {table_name} WHERE tlg_id = %s;"
    )


def delete_check_from_cash_check_by_id():
    return (
        f"DELETE FROM cash_check WHERE id = %s;"
    )
