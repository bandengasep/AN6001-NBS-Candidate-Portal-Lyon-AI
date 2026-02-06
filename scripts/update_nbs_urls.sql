-- SQL script to update NBS URLs to new NTU Business domain
-- Run this in Supabase SQL Editor after updating the code

-- ============================================
-- Part 1: Update programs table URLs
-- ============================================

UPDATE programs SET url = 'https://www.ntu.edu.sg/business/admissions/graduate-studies/nanyang-mba'
WHERE name = 'Nanyang MBA';

UPDATE programs SET url = 'https://www.ntu.edu.sg/business/admissions/graduate-studies/executive-mba'
WHERE name = 'Executive MBA';

UPDATE programs SET url = 'https://www.ntu.edu.sg/business/admissions/graduate-studies/msc-business-analytics'
WHERE name = 'MSc Business Analytics';

UPDATE programs SET url = 'https://www.ntu.edu.sg/business/admissions/graduate-studies/msc-financial-engineering'
WHERE name = 'MSc Financial Engineering';

UPDATE programs SET url = 'https://www.ntu.edu.sg/business/admissions/graduate-studies/msc-accountancy'
WHERE name = 'MSc Accountancy';

UPDATE programs SET url = 'https://www.ntu.edu.sg/business/admissions/graduate-studies/msc-marketing-science'
WHERE name = 'MSc Marketing Science';

UPDATE programs SET url = 'https://www.ntu.edu.sg/business/admissions/phd-programme'
WHERE name = 'PhD in Business';

UPDATE programs SET url = 'https://www.ntu.edu.sg/business/admissions/ugadmission'
WHERE name = 'Bachelor of Business';

-- ============================================
-- Part 2: Update documents table metadata URLs (for RAG)
-- ============================================

UPDATE documents
SET metadata = jsonb_set(metadata, '{url}',
  CASE
    WHEN metadata->>'url' LIKE '%/programmes/graduate/nanyang-mba%'
      THEN '"https://www.ntu.edu.sg/business/admissions/graduate-studies/nanyang-mba"'
    WHEN metadata->>'url' LIKE '%/programmes/graduate/executive-mba%'
      THEN '"https://www.ntu.edu.sg/business/admissions/graduate-studies/executive-mba"'
    WHEN metadata->>'url' LIKE '%/programmes/graduate/msc-business-analytics%'
      THEN '"https://www.ntu.edu.sg/business/admissions/graduate-studies/msc-business-analytics"'
    WHEN metadata->>'url' LIKE '%/programmes/graduate/msc-financial-engineering%'
      THEN '"https://www.ntu.edu.sg/business/admissions/graduate-studies/msc-financial-engineering"'
    WHEN metadata->>'url' LIKE '%/programmes/graduate/msc-accountancy%'
      THEN '"https://www.ntu.edu.sg/business/admissions/graduate-studies/msc-accountancy"'
    WHEN metadata->>'url' LIKE '%/programmes/graduate/msc-marketing-science%'
      THEN '"https://www.ntu.edu.sg/business/admissions/graduate-studies/msc-marketing-science"'
    WHEN metadata->>'url' LIKE '%/programmes/graduate/master-of-science-in-asset%'
      THEN '"https://www.ntu.edu.sg/business/admissions/graduate-studies/master-of-science-in-asset-and-wealth-management"'
    WHEN metadata->>'url' LIKE '%/programmes/graduate/phd%'
      THEN '"https://www.ntu.edu.sg/business/admissions/phd-programme"'
    WHEN metadata->>'url' LIKE '%/programmes/undergraduate/bachelor%'
      THEN '"https://www.ntu.edu.sg/business/admissions/ugadmission"'
    ELSE metadata->'url'
  END
)
WHERE metadata->>'url' LIKE '%nbs.ntu.edu.sg%';

-- ============================================
-- Part 3: Verification queries (run these to check)
-- ============================================

-- Check programs table URLs
SELECT name, url FROM programs ORDER BY name;

-- Check documents table URLs
SELECT DISTINCT metadata->>'url' as url FROM documents WHERE metadata->>'url' IS NOT NULL;

-- Count documents with old URLs (should be 0 after update)
SELECT COUNT(*) as old_url_count FROM documents WHERE metadata->>'url' LIKE '%nbs.ntu.edu.sg%';

-- ============================================
-- Part 4 (OPTIONAL): Clear old documents for fresh re-scrape
-- Uncomment the line below if you want to clear all documents and re-ingest
-- ============================================

-- TRUNCATE documents;
