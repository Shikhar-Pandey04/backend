#!/bin/bash

# Build script for Contract Management Backend

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Generating Prisma client..."
prisma generate

echo "Build completed successfully!"
