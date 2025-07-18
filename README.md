# 📚 eduTrack – Timetable & Announcement Portal

**eduTrack** is a comprehensive timetable management and notification portal designed for both **students** and **faculty members** of an educational institution. It provides real-time access to class schedules, announcements, and classroom availability — all in one place.

---

## 🚀 Features

### 👨‍🎓 For Students:
- **Personal Timetable View**: See your live, updated class schedule.
- **Faculty Timetables**: Explore the timetable of any faculty member.
- **Classroom-wise Schedule**: View which teacher is teaching in which room.
- **Notification Center**: Access announcements relevant to your year, branch, division, and batch.
- **Branch Schedule Explorer**: Select any department and division to explore their weekly schedule.

---

### 👩‍🏫 For Faculty:
- **Editable Timetables**:
  - **Permanent**: Modify your default timetable.
  - **Temporary**: Make short-term schedule changes with date ranges.
- **Classroom Availability**: View all rooms and book vacant classrooms for extra classes.
- **Faculty Timetable Lookup**: Check the schedule of any other faculty member.
- **Room Status Page**: Know which rooms are free or occupied based on the current time.
- **Announcement System**:
  - Send announcements with attachments to selected students.
  - Filter by year, branch, division, and batch.
  - Browse history of previously sent announcements.

---

## 🛠️ Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite3 (can be upgraded to PostgreSQL)
- **Mailing**: Django's email backend for sending announcements
- **Template Engine**: Django Templates
- **Session Management**: Django sessions

---

## 🧩 Modules Overview

| Module               | Description |
|----------------------|-------------|
| `login/`             | User login (Faculty or Student role) |
| `schedule/`          | Timetable view (auto-adapts to role or identifier like teacher name, room number, or class group) |
| `faculty_timetable/` | Editable timetable view for teachers |
| `RoomStatusPage/`    | Shows classroom-wise occupancy status in real-time |
| `branchschedule/`    | Select branch, year, and division to view full schedule |
| `announcements/`     | View/send announcements with filters and attachments |

---

## 📦 How to Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/eduTrack.git
cd eduTrack

# 2. Create virtual environment & install dependencies
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Apply migrations
python manage.py migrate

# 4. Start the development server
python manage.py runserver
