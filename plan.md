# Psychology & Neuroscience Research Recruitment Platform

## Phase 1: Database Schema, Authentication & User Management ✅
- [x] Design and implement database schema (users, studies, applications tables)
- [x] Create user registration system with role selection (researcher/participant)
- [x] Implement login/logout functionality with session management
- [x] Build role-based access control middleware
- [x] Create user profile pages showing role-specific information

---

## Phase 2: Researcher Dashboard & Study Announcement Creation ✅
- [x] Build researcher dashboard layout with navigation (My Studies, Create Study, Applications)
- [x] Implement comprehensive study announcement creation form with all required fields
- [x] Create "My Studies" page listing all researcher's posted announcements with edit/delete capabilities
- [x] Add form validation and error handling for study creation
- [x] Implement study status toggle (open/closed)

---

## Phase 3: Participant Study Browsing & Filtering ✅
- [x] Create public study browsing page with card-based layout showing all open studies
- [x] Implement study detail page with comprehensive information display
- [x] Build multi-criteria filtering system (compensation, participant type, duration, location type)
- [x] Add search functionality for study titles and keywords
- [x] Implement pagination for study listings (10 studies per page)

---

## Phase 4: Application System & Researcher Application Management ✅
- [x] Create participant application form with all required fields
- [x] Implement application submission system linking participants to studies
- [x] Build researcher's application inbox showing all applications per study
- [x] Display application details with participant information and contact details
- [x] Add application status tracking (pending, contacted, accepted, rejected)

---

## Phase 5: UI Polish & Additional Features ✅
- [x] Implement favorites/bookmarking system for participants
- [x] Add study statistics to researcher dashboard
- [x] Create homepage with platform introduction, call-to-action buttons, and featured studies
- [x] Implement responsive design for mobile and tablet devices
- [x] Add loading states, empty states, and success/error notifications throughout the application

---

## Phase 6: UI Verification & Testing ✅
- [x] Test homepage layout and featured studies display
- [x] Test authentication flow (register, login, logout)
- [x] Test browse page with filters
- [x] Verify Material Design 3 styling, elevation, and animations
- [x] Responsive design verified

---

## Phase 7: Participant Visibility & Researcher Request System ✅
- [x] Add participant status field (فعال/غیر فعال) to User model with default "غیر فعال"
- [x] Add privacy settings fields to control demographic information sharing (education, age, occupation, field_of_study)
- [x] Create researcher_requests table in Supabase to track researcher-to-participant invitations
- [x] Update participant profile edit modal to include status toggle and privacy settings
- [x] Display current status on participant profile view

---

## Phase 8: Researcher Participant Browser & Request Sending ✅
- [x] Create new "Browse Participants" navigation item in researcher dashboard
- [x] Build participant browser page showing only "فعال" participants
- [x] Display participant cards with profile picture, name, and allowed demographic information only
- [x] Implement filter by education level, age range, and field of study
- [x] Add "Send Request" button for each participant with study selection dropdown
- [x] Create request sending functionality that stores requests in Supabase

---

## Phase 9: Participant Request Management ✅
- [x] Add "Requests Received" section to participant profile/dashboard
- [x] Display researcher requests with researcher info, study details, and message
- [x] Allow participants to accept/decline researcher requests
- [x] Update request status in database when participant responds
- [x] Add notification badge showing number of pending requests in navbar

---

## Phase 10: UI Verification for Participant Visibility Features
- [ ] Test researcher participant browser with filters
- [ ] Test request sending flow from researcher to participant
- [ ] Test participant request viewing and accept/decline functionality
- [ ] Verify notification badges display correctly
- [ ] Test privacy settings (share_education, share_age, etc.) work correctly
- [ ] Verify participant status toggle between فعال/غیر فعال works
- [ ] Test responsive design for new features