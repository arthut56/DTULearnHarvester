from auth import get_authenticated_session
from courses import get_course_metadata
from downloader import CourseDownloader
from file_utils import FORMAT_MAPPING

print("Enter course number: ", end="")
course_no = input()

print("Enter custom formatting (empty for default): ", end="")
formatting = input().lower()
if formatting == "":
    formatting = "default"

session = get_authenticated_session()
user_courses = session.get("https://learn.inside.dtu.dk/d2l/le/manageCourses/api/mycourses?pageSize=999").json()

course_meta = get_course_metadata(course_no, user_courses)
course_data = session.get(f"https://learn.inside.dtu.dk/d2l/api/le/1.47/{course_meta.get("OrgUnitId")}/content/root/").json()

course_downloader = CourseDownloader(session, course_meta.get("OrgUnitId"), course_meta.get("Name"), FORMAT_MAPPING[formatting])

print(f"Downloading from {course_meta.get("Name")}...")
no_files = course_downloader.download_everything(course_data)
print(f"Downloaded {no_files} files")
