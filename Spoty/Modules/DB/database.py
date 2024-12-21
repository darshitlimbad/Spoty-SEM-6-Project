import json
import mysql.connector
from mysql.connector import errorcode
from Modules.logger import logger

class MySQLConnection:
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.conn = None  # Placeholder for the MySQL connection object
        self.init()

    def init(self):
        try:
            logger.info("Initializing database connection...")

            # Load and parse the JSON configuration file
            with open(self.config_file, 'r') as file:
                config = json.load(file)

            # Extract database configuration
            db_host = config['database']['host']
            db_username = config['database']['username']
            db_password = config['database']['password']
            db_name = config['database']['dbname']

            # Connect to MySQL server (without specifying a database)
            conn = mysql.connector.connect(
                host=db_host,
                user=db_username,
                password=db_password
            )
            self.conn = conn  # Store connection object
            cursor = conn.cursor()

            logger.info(f"Connected to MySQL server at {db_host}.")

            # Check if the database exists and create it if not
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`")
            logger.info(f"Database `{db_name}` checked/created successfully.")
            cursor.execute(f"USE `{db_name}`")

            # Create the "users" table if it doesn't exist
            table_query = """
                CREATE TABLE IF NOT EXISTS users (
                    id VARCHAR(20) PRIMARY KEY,        -- Discord user ID
                    username VARCHAR(100),            -- Username
                    discriminator VARCHAR(4),         -- Discriminator (e.g., #1234)
                    avatar VARCHAR(255),              -- Avatar hash
                    access_token TEXT,                -- OAuth2 access token
                    refresh_token TEXT,               -- OAuth2 refresh token
                    token_expires_at DATETIME,        -- Expiry timestamp for the access token
                    last_login DATETIME,               -- Timestamp of the last login
                    premium TINYINT(1) DEFAULT 0      -- Premium status
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """
            cursor.execute(table_query)
            logger.info("Table `users` checked/created successfully.")
            print("-" * 100)

        except FileNotFoundError:
            logger.error("Config file not found.")
        except json.JSONDecodeError:
            logger.error("Invalid JSON in config file.")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                logger.error("Invalid database credentials.")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                logger.error("Database does not exist.")
            else:
                logger.error(f"Database error: {err}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
        finally:
            if 'cursor' in locals():
                cursor.close()

    def get_connection(self):
        """Returns the active MySQL connection object."""
        return self.conn

    def close_connection(self):
        """Closes the MySQL connection."""
        if self.conn and self.conn.is_connected():
            self.conn.close()
            logger.info("MySQL connection closed.")
    
    def is_connected(self):
        """Check if the MySQL connection is active."""
        return self.conn.is_connected() if self.conn else False
    
    def is_user_registered(self, user_id: str):
        """Check if a user is already registered in the database."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        result = cursor.fetchone()
        cursor.close()
        return result is not None
    
    def is_user_premium(self, user_id: str):
        """Check if a user has a premium account."""
        
        # idk why but this is not working i think the problem is with premium value not being updated in db will check it out letter.
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM users WHERE id = {user_id} AND premium = 1")
        result = cursor.fetchone()
        cursor.close()
        print(result)
        return result is not None

