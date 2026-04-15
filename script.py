
from auth import get_authenticated_session
from courses import *
from downloader import *

print("Enter course number: ", end="")
course_no = input()

session = get_authenticated_session()
user_courses = session.get("https://learn.inside.dtu.dk/d2l/le/manageCourses/api/mycourses?pageSize=999").json()

course_id = get_course_id_from_course_no(course_no, user_courses)
course_name = get_course_name_from_course_no(course_no, user_courses)
print(f"Downloading from {course_name}...")
course_data = session.get(f"https://learn.inside.dtu.dk/d2l/api/le/1.47/{course_id}/content/root/").json()


no_files = download_everything(session, course_id, course_name, course_data)
print(f"Downloaded {no_files} files")
