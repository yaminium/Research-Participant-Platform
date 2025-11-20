import os
import logging
from supabase import create_client, Client


def run_migration_verification():
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    if not supabase_url or not supabase_key:
        print("Error: SUPABASE_URL and SUPABASE_KEY environment variables must be set.")
        return
    print(f"Connecting to Supabase at {supabase_url}...")
    supabase: Client = create_client(supabase_url, supabase_key)
    migration_path = os.path.join(
        os.path.dirname(__file__), "../migrations/01_add_experiments_columns.sql"
    )
    migration_path_02 = os.path.join(
        os.path.dirname(__file__), "../migrations/02_create_user_tables.sql"
    )
    try:
        with open(migration_path, "r") as f:
            sql_content = f.read()
        sql_content_02 = ""
        if os.path.exists(migration_path_02):
            with open(migration_path_02, "r") as f:
                sql_content_02 = f.read()
        print("""
--- SQL MIGRATION REQUIRED ---""")
        print("Please run the following SQL in your Supabase Dashboard SQL Editor:")
        print("-" * 80)
        print(sql_content)
        if sql_content_02:
            print("""
--- MIGRATION 02: Create User Tables ---""")
            print(sql_content_02)
        print("-" * 80)
        print("""
(Note: The Supabase Python client cannot execute DDL statements like ALTER TABLE directly via the REST API.)
""")
    except FileNotFoundError as e:
        logging.exception(f"Warning: Could not find migration file at {migration_path}")
    print("--- VERIFYING TABLE STRUCTURE ---")
    try:
        response = (
            supabase.table("experiments")
            .select(
                "title, date, description, number_of_participants, inclusion_criteria, exclusion_criteria"
            )
            .limit(1)
            .execute()
        )
        print("✅ SUCCESS: The 'experiments' table contains all required columns.")
        print(f"Sample query result: {response.data}")
    except Exception as e:
        logging.exception(f"Error details: {str(e)}")
        print("❌ FAILURE: Could not query the new columns.")
        print("""
Please execute the SQL migration shown above to fix this.""")


if __name__ == "__main__":
    run_migration_verification()