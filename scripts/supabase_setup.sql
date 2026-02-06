-- Supabase SQL setup for NBS Degree Advisor
-- Run this in your Supabase SQL Editor

-- Enable pgvector extension for vector similarity search
create extension if not exists vector;

-- Create documents table for RAG
create table if not exists documents (
  id uuid primary key default gen_random_uuid(),
  content text not null,
  metadata jsonb default '{}',
  embedding vector(1536),
  created_at timestamp with time zone default now()
);

-- Create index for vector similarity search
create index if not exists documents_embedding_idx
  on documents using ivfflat (embedding vector_cosine_ops)
  with (lists = 100);

-- Create index for metadata queries
create index if not exists documents_metadata_idx
  on documents using gin (metadata);

-- Create programs table for structured program data
create table if not exists programs (
  id uuid primary key default gen_random_uuid(),
  name text not null unique,
  degree_type text not null,
  description text,
  duration text,
  url text,
  requirements jsonb default '{}',
  metadata jsonb default '{}',
  created_at timestamp with time zone default now(),
  updated_at timestamp with time zone default now()
);

-- Create chat history table
create table if not exists chat_history (
  id uuid primary key default gen_random_uuid(),
  conversation_id text not null,
  role text not null check (role in ('user', 'assistant', 'system')),
  content text not null,
  metadata jsonb default '{}',
  created_at timestamp with time zone default now()
);

-- Create index for conversation lookup
create index if not exists chat_history_conversation_idx
  on chat_history (conversation_id, created_at);

-- Function to match documents by vector similarity
create or replace function match_documents(
  query_embedding vector(1536),
  match_count int default 4,
  match_threshold float default 0.7
)
returns table (
  id uuid,
  content text,
  metadata jsonb,
  similarity float
)
language plpgsql
as $$
begin
  return query
  select
    documents.id,
    documents.content,
    documents.metadata,
    1 - (documents.embedding <=> query_embedding) as similarity
  from documents
  where 1 - (documents.embedding <=> query_embedding) > match_threshold
  order by documents.embedding <=> query_embedding
  limit match_count;
end;
$$;

-- Function to update timestamp on program update
create or replace function update_updated_at()
returns trigger as $$
begin
  new.updated_at = now();
  return new;
end;
$$ language plpgsql;

-- Trigger to auto-update updated_at
create trigger programs_updated_at
  before update on programs
  for each row
  execute function update_updated_at();

-- Insert sample programs (can be updated by scraper)
insert into programs (name, degree_type, description, duration, url) values
  ('Nanyang MBA', 'MBA', 'The Nanyang MBA is a full-time programme designed for ambitious professionals seeking to accelerate their careers.', '12 months', 'https://www.ntu.edu.sg/business/admissions/graduate-studies/nanyang-mba'),
  ('Executive MBA', 'EMBA', 'The Nanyang Executive MBA is designed for senior executives and leaders who want to enhance their strategic thinking.', '18 months', 'https://www.ntu.edu.sg/business/admissions/graduate-studies/executive-mba'),
  ('MSc Business Analytics', 'MSc', 'The MSc in Business Analytics programme equips students with the skills to leverage data for business decision-making.', '12 months', 'https://www.ntu.edu.sg/business/admissions/graduate-studies/msc-business-analytics'),
  ('MSc Financial Engineering', 'MSc', 'The MSc in Financial Engineering programme prepares students for careers in quantitative finance and risk management.', '12 months', 'https://www.ntu.edu.sg/business/admissions/graduate-studies/msc-financial-engineering'),
  ('MSc Accountancy', 'MSc', 'The MSc in Accountancy programme provides advanced knowledge in accounting, auditing, and financial reporting.', '12 months', 'https://www.ntu.edu.sg/business/admissions/graduate-studies/msc-accountancy'),
  ('MSc Marketing Science', 'MSc', 'The MSc in Marketing Science combines marketing theory with data analytics and scientific methods.', '12 months', 'https://www.ntu.edu.sg/business/admissions/graduate-studies/msc-marketing-science'),
  ('PhD in Business', 'PhD', 'The PhD programme prepares students for careers in academic research and teaching at leading business schools.', '4-5 years', 'https://www.ntu.edu.sg/business/admissions/phd-programme'),
  ('Bachelor of Business', 'Bachelor', 'The Bachelor of Business programme provides a comprehensive foundation in business and management.', '4 years', 'https://www.ntu.edu.sg/business/admissions/ugadmission')
on conflict (name) do nothing;

-- Row Level Security (RLS) policies
-- Enable RLS on tables
alter table documents enable row level security;
alter table chat_history enable row level security;
alter table programs enable row level security;

-- Allow read access to documents for authenticated and anon users
create policy "Allow read access to documents" on documents
  for select using (true);

-- Allow read access to programs
create policy "Allow read access to programs" on programs
  for select using (true);

-- Allow read/write access to chat history
create policy "Allow read access to chat history" on chat_history
  for select using (true);

create policy "Allow insert to chat history" on chat_history
  for insert with check (true);

-- Service role can do everything (for ingestion)
create policy "Service role full access to documents" on documents
  for all using (auth.role() = 'service_role');
