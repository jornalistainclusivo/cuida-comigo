import asyncio
import asyncpg
import os

POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

async def main():
    print("Connecting...")
    conn = await asyncpg.connect(
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        database="orquestracao"
    )
    print("Connected.")
    print("Executing query...")
    try:
        await conn.execute("INSERT INTO care_groups (id, name, created_at, updated_at) VALUES ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'Test', now(), now())")
        print("Success.")
    except Exception as e:
        print("Error:", e)
    finally:
        await conn.close()

asyncio.run(main())
