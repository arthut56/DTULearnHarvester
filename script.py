
from file_utils import *
from auth import get_authenticated_session
from courses import get_course_id_from_course_no

session = get_authenticated_session()

#not used
enrollments = session.get("https://learn.inside.dtu.dk/d2l/api/lp/1.47/enrollments/myenrollments/").json()
mycourses = session.get("https://learn.inside.dtu.dk/d2l/le/manageCourses/api/mycourses").json()


course_id = get_course_id_from_course_no("02160", mycourses)
course_data = session.get(f"https://learn.inside.dtu.dk/d2l/api/le/1.47/{course_id}/content/root/").json()
print(course_id)
print("Downloading...")
no_files = 0
for tab in course_data:
    for document in tab.get("Structure"):
        document_id = document.get("Id")
        document_title = sanitize_filename(document.get("Title"))
        document_type = document.get("Type")
        url = f"https://learn.inside.dtu.dk/d2l/le/content/{course_id}/topics/files/download/{document_id}/DirectFileTopicDownload"

        response = session.get(url)
        print(get_file_type_from_headers(response.headers))

        if response.status_code != 200:
            print(response.status_code)
            continue

        # with open(document_title, "wb") as f:
        #     f.write(response.content)

        print(f"(fake) {response.status_code} Downloaded: {document_title}.{get_file_type_from_headers(response.headers)}")

        no_files += 1

print(f"Downloaded {no_files} files")

#TODO: add logic for considering modules and take action based on this
#TODO: add alt way of specifying credentials

#Interesting note: courses you TA'd do not count/work

#File type 1 is file i.e. works with DirectFileTopicDownload
#File type 0 is a module/folder, requires recursion

#test ID = 02160 -> 187639 (agile, old PREFERRED) or 296238 (agile, new)
# course ID != course no.
# direct download
#https://learn.inside.dtu.dk/d2l/le/content/{course ID}/topics/files/download/{file ID}/DirectFileTopicDownload
# access a module (appears to be deprecated)
# https://learn.inside.dtu.dk/d2l/api/le/1.47/{course ID}/content/modules/{module ID}/structure/

#https://learn.inside.dtu.dk/d2l/api/le/1.47/296238/content/root/

