"""
Database configuration using Prisma ORM
"""
import os
from prisma import Prisma
from dotenv import load_dotenv
from pathlib import Path

# Load .env file from the backend directory
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Create a global Prisma instance
prisma = Prisma()

async def connect_db():
    """Connect to the database"""
    try:
        await prisma.connect()
        print("✅ Database connected successfully with Prisma!")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

async def disconnect_db():
    """Disconnect from the database"""
    try:
        await prisma.disconnect()
        print("✅ Database disconnected successfully!")
    except Exception as e:
        print(f"⚠️  Warning during disconnect: {e}")

async def get_db():
    """Dependency to get database client"""
    return prisma

# Context manager for database operations
class DatabaseManager:
    def __init__(self):
        self.prisma = prisma
    
    async def __aenter__(self):
        await self.prisma.connect()
        return self.prisma
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.prisma.disconnect()
