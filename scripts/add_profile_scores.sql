-- Add spider chart profile scores to programs table
-- 7 axes: quantitative, experience, leadership, tech_analytics, business_domain, career_ambition, study_flexibility
-- Each score is 1-5

ALTER TABLE programs
ADD COLUMN IF NOT EXISTS profile_scores jsonb DEFAULT '{}';

COMMENT ON COLUMN programs.profile_scores IS 'Spider chart scores: {quantitative, experience, leadership, tech_analytics, business_domain, career_ambition, study_flexibility} each 1-5';
