# This file redirects to the Prisma-based contracts implementation
# to avoid conflicts with the old SQLAlchemy code

from .contracts_prisma import router

# All routes are now handled by contracts_prisma.py
