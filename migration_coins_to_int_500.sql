-- Migration: Add coins column to user table
-- Date: 2025-12-14
-- Description: Adds coins INTEGER column with DEFAULT 500 to user table
-- IMPORTANT: This migration assumes the coins column does NOT exist yet

-- Idempotent migration: Only add column if it doesn't exist
DO $$
BEGIN
    -- Check if coins column exists
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'user' 
        AND column_name = 'coins'
    ) THEN
        -- Add coins column with INTEGER type and DEFAULT 500
        ALTER TABLE "user" 
        ADD COLUMN coins INTEGER NOT NULL DEFAULT 500;
        
        -- Add constraint to ensure coins are never negative
        ALTER TABLE "user" 
        ADD CONSTRAINT user_coins_non_negative CHECK (coins >= 0);
        
        RAISE NOTICE 'Column coins added successfully to user table';
    ELSE
        RAISE NOTICE 'Column coins already exists in user table';
    END IF;
END $$;

-- Optional: Update any existing users to have 500 coins if they somehow have NULL
-- (This is just a safety measure, should not be needed with NOT NULL DEFAULT)
UPDATE "user" SET coins = 500 WHERE coins IS NULL;

