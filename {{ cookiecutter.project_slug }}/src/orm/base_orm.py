from os import environ, path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from orm.retrying_query_orm import RetryingQuery

from dotenv import load_dotenv


# Load the basic environment variables from .env
load_dotenv()

# Get the current environment (default to 'DEV' if not set)
env = environ.get('ENVIRONMENT', 'DEV')

# Construct the environment-specific .env filename
env_file = f".env.{env.lower()}"

# Check if the environment-specific .env file exists
if path.exists(env_file):
    load_dotenv(env_file)
else:
    raise FileNotFoundError(f"Environment file '{env_file}' not found.")


class ORMBase:
    engines = {}
    sessions = {}
    Base = declarative_base()

    @classmethod
    def get_mysql_connection_string(cls, db_name):
        """Constructs the connection string for a MySQL database."""
        user = environ.get(f'{db_name}_USERNAME')
        password = environ.get(f'{db_name}_PASSWORD')
        database = environ.get(f'{db_name}_DATABASE')
        host = environ.get(f'{db_name}_HOST')

        return f"mysql+pymysql://{user}:{password}@{host}/{database}"

    @classmethod
    def get_mssql_connection_string(cls, db_name):
        """Constructs the connection string for a MSSQL database."""
        user = environ.get(f'{db_name}_USERNAME')
        password = environ.get(f'{db_name}_PASSWORD')
        database = environ.get(f'{db_name}_DATABASE')
        host = environ.get(f'{db_name}_HOST')

        return f"mssql+pyodbc://{user}:{password}@{host}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
    
    @classmethod
    def get_connection_string(cls, db_name):
        """Returns the connection string based on the database type."""
        db_type = environ.get(f'{db_name}_TYPE') # Example values: 'mysql', 'mssql', etc.
        if db_type == 'mysql':
            return cls.get_mysql_connection_string(db_name)
        elif db_type == 'mssql':
            return cls.get_mssql_connection_string(db_name)

    @classmethod
    def get_engine(cls, db_name):
        """Returns the SQLAlchemy engine for the specified database."""
        if db_name not in cls.engines:
            connection_string = cls.get_connection_string(db_name) 
            cls.engines[db_name] = create_engine(connection_string, pool_recycle=True)
        return cls.engines[db_name]

    @classmethod
    def get_session(cls, db_name):
        """Returns the SQLAlchemy session for the specified database."""
        if db_name not in cls.sessions:
            engine = cls.get_engine(db_name)
            session = sessionmaker(bind=engine, query_cls=RetryingQuery)
            cls.sessions[db_name] = session()
        return cls.sessions[db_name]
