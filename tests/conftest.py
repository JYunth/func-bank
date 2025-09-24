import os
from sqlalchemy import create_engine, text

# Set database URL for tests
os.environ['DATABASE_URL'] = 'postgresql://testuser:testpass@localhost:5432/schema_test_db'

# Create test tables
engine = create_engine(os.environ['DATABASE_URL'])
with engine.connect() as conn:
    # Create test_table for contract tests
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS test_table (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            value INTEGER
        )
    """))

    # Create test_users for integration tests
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS test_users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            active BOOLEAN DEFAULT TRUE
        )
    """))

    # Insert test data
    conn.execute(text("""
        INSERT INTO test_table (name, value) VALUES
        ('test', 1),
        ('another', 2)
        ON CONFLICT DO NOTHING
    """))

    conn.execute(text("""
        INSERT INTO test_users (name, email, active) VALUES
        ('Alice', 'alice@example.com', true),
        ('Bob', 'bob@example.com', false),
        ('Charlie', 'charlie@example.com', true)
        ON CONFLICT (email) DO NOTHING
    """))

    conn.commit()