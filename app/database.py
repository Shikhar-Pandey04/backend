from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env file from the backend directory
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Database URL - use environment variable or default to PostgreSQL
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:password@localhost:5432/contract_db"
)

# Debug: Print the database URL (hide password for security)
if DATABASE_URL:
    # Hide password in logs
    url_for_display = DATABASE_URL.replace(DATABASE_URL.split('@')[0].split(':')[-1], "***") if '@' in DATABASE_URL else DATABASE_URL
    print(f"🔗 Using database URL: {url_for_display}")
else:
    print("❌ No DATABASE_URL found in environment variables")

# Create engine with better connection handling for cloud databases
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,    # Recycle connections every 5 minutes
    connect_args={"sslmode": "require"} if "neon.tech" in DATABASE_URL else {}
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_connection():
    """Test basic database connection"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def init_pgvector():
    """Initialize pgvector extension"""
    try:
        with engine.connect() as conn:
            # First check if extension exists
            result = conn.execute(text(
                "SELECT EXISTS(SELECT 1 FROM pg_extension WHERE extname = 'vector')"
            ))
            extension_exists = result.scalar()
            
            if not extension_exists:
                conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
                conn.commit()
                print("✅ pgvector extension created successfully")
            else:
                print("✅ pgvector extension already exists")
            return True
    except Exception as e:
        print(f"⚠️  Warning: Could not initialize pgvector: {e}")
        print("The application will continue without vector search functionality.")
        return False

# Test connection and initialize pgvector when module is imported
print("🔄 Testing database connection...")
if test_connection():
    print("🔄 Initializing pgvector extension...")
    init_pgvector()
else:
    print("⚠️  Starting in limited mode - database features may not work.")
