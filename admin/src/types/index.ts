export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  role: 'admin' | 'lecturer' | 'student';
  is_active: boolean;
  created_at: string;
}

export interface Student extends User {
  student_id: string;
  department?: string;
  year_of_study?: number;
}

export interface Venue {
  id: string;
  name: string;
  description?: string;
  latitude?: number;
  longitude?: number;
  radius_m: number;
  allowed_cidrs: string[];
  is_active: boolean;
  created_at: string;
}

export interface Lecture {
  id: string;
  venue_id: string;
  course_code: string;
  course_name: string;
  lecturer_id: string;
  start_time: string;
  end_time: string;
  is_active: boolean;
  created_at: string;
}

export interface AttendanceRecord {
  id: string;
  user_id: string;
  lecture_id: string;
  status: 'present' | 'late' | 'absent' | 'invalid_geofence' | 'invalid_match';
  match_score?: number;
  server_ip?: string;
  client_local_ip?: string;
  gps_lat?: number;
  gps_lng?: number;
  gps_accuracy_m?: number;
  notes?: string;
  created_at: string;
}

export interface FaceEnrollment {
  id: string;
  user_id: string;
  model: string;
  embedding: number[];
  quality_score?: number;
  created_at: string;
}