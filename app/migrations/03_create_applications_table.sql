-- Migration: Create applications table
-- This table stores participant applications to research studies

-- Create applications table
CREATE TABLE IF NOT EXISTS applications (
    id TEXT PRIMARY KEY,
    study_id TEXT NOT NULL REFERENCES experiments(id) ON DELETE CASCADE,
    participant_id TEXT NOT NULL,
    participant_name TEXT NOT NULL,
    age INTEGER NOT NULL,
    gender TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT,
    motivation_message TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Pending' CHECK (status IN ('Pending', 'Contacted', 'Accepted', 'Rejected')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_applications_study_id ON applications(study_id);
CREATE INDEX IF NOT EXISTS idx_applications_participant_id ON applications(participant_id);
CREATE INDEX IF NOT EXISTS idx_applications_status ON applications(status);

-- Enable Row Level Security (optional but recommended)
ALTER TABLE applications ENABLE ROW LEVEL SECURITY;

-- Create policy to allow all operations for now (you can restrict this later)
CREATE POLICY "Enable all access for applications" ON applications
    FOR ALL USING (true);

-- Note: This migration should be run in Supabase SQL Editor
