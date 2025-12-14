-- Migration: Add legal and profile fields to user table
-- Date: 2025-12-14
-- Description: Extends user table with profile and legal compliance fields
-- IMPORTANT: This migration is idempotent and safe to run multiple times

-- Add profile fields (all optional except birth_date)
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS full_name TEXT;
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS phone_number TEXT;
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS birth_date DATE;
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS country TEXT;

-- Add legal/compliance fields
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS accepted_terms BOOLEAN DEFAULT FALSE;
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS accepted_privacy_policy BOOLEAN DEFAULT FALSE;
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS is_adult BOOLEAN;
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS verified_at TIMESTAMP;

-- Add timestamp fields
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT NOW();
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT NOW();

-- TODO: Add trigger to automatically update updated_at on row UPDATE
-- For now, application must manually set updated_at = NOW() on updates
-- Example trigger (to be added later):
-- CREATE OR REPLACE FUNCTION update_updated_at_column()
-- RETURNS TRIGGER AS $$
-- BEGIN
--     NEW.updated_at = NOW();
--     RETURN NEW;
-- END;
-- $$ language 'plpgsql';
--
-- CREATE TRIGGER update_user_updated_at BEFORE UPDATE ON "user"
-- FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Add constraints only if they don't exist
DO $$
BEGIN
    -- Check constraint: user must be adult (no NULL allowed - birth_date is required)
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint 
        WHERE conname = 'user_must_be_adult' 
        AND conrelid = '"user"'::regclass
    ) THEN
        ALTER TABLE "user" ADD CONSTRAINT user_must_be_adult 
        CHECK (is_adult = TRUE);
    END IF;

    -- Check constraint: user must accept terms (no NULL allowed - required field)
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint 
        WHERE conname = 'user_must_accept_terms' 
        AND conrelid = '"user"'::regclass
    ) THEN
        ALTER TABLE "user" ADD CONSTRAINT user_must_accept_terms 
        CHECK (accepted_terms = TRUE);
    END IF;

    -- Check constraint: user must accept privacy policy (no NULL allowed - required field)
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint 
        WHERE conname = 'user_must_accept_privacy' 
        AND conrelid = '"user"'::regclass
    ) THEN
        ALTER TABLE "user" ADD CONSTRAINT user_must_accept_privacy 
        CHECK (accepted_privacy_policy = TRUE);
    END IF;
END $$;

-- Update existing users to have timestamps if they don't have them
UPDATE "user" SET created_at = NOW() WHERE created_at IS NULL;
UPDATE "user" SET updated_at = NOW() WHERE updated_at IS NULL;

-- Migration completed
SELECT 'Migration completed successfully' AS status;

