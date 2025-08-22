-- Enable required extensions
create extension if not exists "uuid-ossp";
create extension if not exists "pgcrypto";
-- create extension if not exists vector;  -- Removed to avoid errors

-- USERS
create table if not exists users (
  id uuid primary key default gen_random_uuid(),
  student_number text unique,
  full_name text not null,
  email text unique,
  role text not null default 'student', -- 'student' | 'admin' | 'lecturer'
  created_at timestamptz not null default now()
);

-- VENUES
create table if not exists venues (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  building text,
  latitude double precision,
  longitude double precision,
  radius_m integer default 30,
  wifi_ssid text[],
  wifi_bssid text[],
  allowed_cidrs text[],
  created_at timestamptz not null default now()
);

-- LECTURES
create table if not exists lectures (
  id uuid primary key default gen_random_uuid(),
  module_code text not null,
  title text,
  venue_id uuid references venues(id) on delete set null,
  start_time timestamptz not null,
  end_time timestamptz not null,
  late_after_minutes integer default 10
);

-- ENROLLMENTS
create table if not exists enrollments (
  user_id uuid references users(id) on delete cascade,
  module_code text not null,
  primary key (user_id, module_code)
);

-- FACE TEMPLATES
create table if not exists face_templates (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references users(id) on delete cascade,
  model text not null,
  embedding BYTEA,  -- replaced vector(512) with BYTEA
  image_url text,
  created_at timestamptz not null default now()
);

-- ATTENDANCE LOGS
create table if not exists attendance_logs (
  id uuid primary key default gen_random_uuid(),
  lecture_id uuid references lectures(id) on delete cascade,
  user_id uuid references users(id) on delete cascade,
  checkin_time timestamptz not null default now(),
  status text not null,         -- 'on_time' | 'late' | 'invalid_geofence' | 'invalid_match' | 'invalid_network'
  client_lat double precision,
  client_lng double precision,
  client_accuracy_m double precision,
  server_ip text,
  client_local_ip text,
  client_public_ip text,
  client_user_agent text,
  liveness_score double precision,
  match_score double precision,
  notes text,
  created_at timestamptz not null default now()
);

-- OPTIONAL: sample admin user for testing
insert into users (student_number, full_name, email, role)
values ('0001', 'Admin User', 'admin@example.com', 'admin')
on conflict do nothing;

-- OPTIONAL: sample venue
insert into venues (name, building, latitude, longitude, radius_m, allowed_cidrs)
values ('Main Lecture Hall', 'Building A', -29.860, 31.030, 50, '{"0.0.0.0/0"}')
on conflict do nothing;

-- OPTIONAL: sample lecture
insert into lectures (module_code, title, venue_id, start_time, end_time)
select 'CS101', 'Intro to Programming', id, now() + interval '1 hour', now() + interval '2 hour' from venues limit 1
on conflict do nothing;
