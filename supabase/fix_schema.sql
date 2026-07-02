-- Fix schema mismatch: skills table has 'last_updated' but trigger expects 'updated_at'
-- Run this in Supabase SQL Editor before running seed.sql

-- Drop the broken trigger on skills
DROP TRIGGER IF EXISTS skills_updated_at ON public.skills;

-- Create a new function that handles 'last_updated'
CREATE OR REPLACE FUNCTION update_last_updated()
RETURNS TRIGGER AS $$
BEGIN
    NEW.last_updated = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create a new trigger for skills using 'last_updated'
CREATE TRIGGER skills_last_updated
BEFORE UPDATE ON public.skills
FOR EACH ROW EXECUTE FUNCTION update_last_updated();

-- Now run the seed.sql — it will work without errors
