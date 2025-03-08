from env_variables import db_params
import psycopg2

def is_connected():
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cursor:
                print("Connected to the database successfully!")
                return True
    except Exception as e:
        print("Error:", e)
        return False


def create_tables():
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS warrior (
                        id SERIAL PRIMARY KEY,
                        tlg_id VARCHAR(32) NOT NULL,
                        nick VARCHAR(25) NOT NULL
                    )
                """)

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS cash_check (
                        id SERIAL PRIMARY KEY,
                        warrior_id INT NOT NULL,
                        image_url TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        amount DECIMAL(10,2) NOT NULL,
                        CONSTRAINT fk_warrior FOREIGN KEY (warrior_id) REFERENCES warrior (id) ON DELETE CASCADE
                    )
                """)

                conn.commit()
                print("Tables created successfully!")
    except Exception as e:
        print("Error while creating tables:", e)


if is_connected():
    create_tables()
else:
    print("Not connected to the database.")
