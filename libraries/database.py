# -*- coding: utf-8 -*-
"""
database.py -- Antenatal prediction of fetal death, MIMIC-IV

Connection helpers for the local PostgreSQL instance that holds the MIMIC-IV schema
(the same database used by MaternalMortality_MIMIC-IV_Cureus and PerinatalMortality_MIMIC-IV).
All parameters come from environment variables (see .env.example), so no credential
is ever committed.
"""
import os
import sqlalchemy as alchemy

# Optional: load variables from a local .env file if python-dotenv is installed.
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def get_connect_database():
    """Return a SQLAlchemy engine for the local MIMIC-IV PostgreSQL database.

    MIMICIV_DB_PASSWORD has no default on purpose: the function raises if it is
    missing, rather than connecting with a blank password.
    """
    driver = "postgresql+psycopg2"
    user = os.environ.get("MIMICIV_DB_USER", "postgres")
    password = os.environ.get("MIMICIV_DB_PASSWORD")
    host = os.environ.get("MIMICIV_DB_HOST", "localhost")
    port = os.environ.get("MIMICIV_DB_PORT", "5433")
    database = os.environ.get("MIMICIV_DB_NAME", "mimiciv")

    if not password:
        raise RuntimeError(
            "MIMICIV_DB_PASSWORD is not set. Copy .env.example to .env, fill in your "
            "own local Postgres password, and make sure python-dotenv is installed "
            "(see requirements.txt)."
        )

    return alchemy.create_engine(f"{driver}://{user}:{password}@{host}:{port}/{database}")


def disconnect_database(engine):
    engine.dispose()
