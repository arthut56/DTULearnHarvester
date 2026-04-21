from auth import get_authenticated_session
from courses import get_course_metadata
from downloader import CourseDownloader
from file_utils import FORMAT_MAPPING

def download_course(course_no, formatting):
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

if __name__ == "__main__":
    print("Enter course number: ", end="")
    course_to_download = input()
    print("Enter custom formatting (empty for default): ", end="")
    format_style = input().lower()


    download_course(course_to_download, format_style)
