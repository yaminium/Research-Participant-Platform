-- Migration: Add User Profile Columns
-- This migration adds missing profile columns to participants and researchers tables

-- Add missing profile columns to participants table
ALTER TABLE participants 
ADD COLUMN IF NOT EXISTS date_of_birth DATE,
ADD COLUMN IF NOT EXISTS phone_number TEXT DEFAULT '',
ADD COLUMN IF NOT EXISTS profile_picture TEXT DEFAULT '';

-- Add missing profile columns to researchers table
ALTER TABLE researchers 
ADD COLUMN IF NOT EXISTS date_of_birth DATE,
ADD COLUMN IF NOT EXISTS phone_number TEXT DEFAULT '',
ADD COLUMN IF NOT EXISTS profile_picture TEXT DEFAULT '',
ADD COLUMN IF NOT EXISTS education_level TEXT DEFAULT '',
ADD COLUMN IF NOT EXISTS field_of_study TEXT DEFAULT '',
ADD COLUMN IF NOT EXISTS occupation TEXT DEFAULT '';

-- Note: This migration should be run in Supabase SQL Editor
