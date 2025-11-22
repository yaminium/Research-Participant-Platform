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
    migration_path_03 = os.path.join(
        os.path.dirname(__file__), "../migrations/03_create_applications_table.sql"
    )
    migration_path_04 = os.path.join(
        os.path.dirname(__file__), "../migrations/04_add_participant_visibility.sql"
    )
    migration_path_05 = os.path.join(
        os.path.dirname(__file__), "../migrations/05_add_user_profile_columns.sql"
    )
    try:
        with open(migration_path, "r") as f:
            sql_content = f.read()
        sql_content_02 = ""
        if os.path.exists(migration_path_02):
            with open(migration_path_02, "r") as f:
                sql_content_02 = f.read()
        sql_content_03 = ""
        if os.path.exists(migration_path_03):
            with open(migration_path_03, "r") as f:
                sql_content_03 = f.read()
        sql_content_04 = ""
        if os.path.exists(migration_path_04):
            with open(migration_path_04, "r") as f:
                sql_content_04 = f.read()
        sql_content_05 = ""
        if os.path.exists(migration_path_05):
            with open(migration_path_05, "r") as f:
                sql_content_05 = f.read()
        print("""
--- SQL MIGRATION REQUIRED ---""")
        print("Please run the following SQL in your Supabase Dashboard SQL Editor:")
        print("-" * 80)
        print(sql_content)
        if sql_content_02:
            print("""
--- MIGRATION 02: Create User Tables ---""")
            print(sql_content_02)
        if sql_content_03:
            print("""
--- MIGRATION 03: Create Applications Table ---""")
            print(sql_content_03)
        if sql_content_04:
            print("""
--- MIGRATION 04: Add Participant Visibility & Requests ---""")
            print(sql_content_04)
        if sql_content_05:
            print("""
--- MIGRATION 05: Add User Profile Columns ---""")
            print(sql_content_05)
        print("-" * 80)
        print("""
(Note: The Supabase Python client cannot execute DDL statements like ALTER TABLE directly via the REST API.)
""")
    except FileNotFoundError as e:
        logging.exception(f"Warning: Could not find migration file at {migration_path}")
    print("--- VERIFYING EXPERIMENTS TABLE STRUCTURE ---")
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
    except Exception as e:
        logging.exception(f"Error verifying experiments table: {str(e)}")
        print("❌ FAILURE: Could not query the new columns in experiments.")
    print("""
--- VERIFYING PARTICIPANT VISIBILITY & REQUESTS ---""")
    try:
        response = (
            supabase.table("participants")
            .select("participant_status, share_education")
            .limit(1)
            .execute()
        )
        print("✅ SUCCESS: The 'participants' table contains visibility columns.")
        response = (
            supabase.table("researcher_requests")
            .select("id, status")
            .limit(1)
            .execute()
        )
        print("✅ SUCCESS: The 'researcher_requests' table exists.")
    except Exception as e:
        logging.exception(
            f"❌ FAILURE: Could not query new participant columns or request table. Error: {str(e)}"
        )
        print("Please execute MIGRATION 04.")
    print("""
--- VERIFYING USER PROFILE COLUMNS ---""")
    try:
        response = (
            supabase.table("participants")
            .select("date_of_birth, phone_number, profile_picture")
            .limit(1)
            .execute()
        )
        print("✅ SUCCESS: The 'participants' table contains profile columns.")
        response = (
            supabase.table("researchers")
            .select(
                "date_of_birth, phone_number, profile_picture, education_level, field_of_study, occupation"
            )
            .limit(1)
            .execute()
        )
        print("✅ SUCCESS: The 'researchers' table contains profile columns.")
    except Exception as e:
        logging.exception(
            f"❌ FAILURE: Could not query profile columns. Error: {str(e)}"
        )
        print("Please execute MIGRATION 05.")


if __name__ == "__main__":
    run_migration_verification()