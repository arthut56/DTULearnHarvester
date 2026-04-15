from os import mkdir

from file_utils import *
from auth import get_authenticated_session
from courses import get_course_id_from_course_no

session = get_authenticated_session()

course_no = "34370"
#not used
enrollments = session.get("https://learn.inside.dtu.dk/d2l/api/lp/1.47/enrollments/myenrollments/").json()
#DEFAULT PAGE SIZE IS 20, OVERRIDE TO SHOW ALL COURSES
mycourses = session.get("https://learn.inside.dtu.dk/d2l/le/manageCourses/api/mycourses?pageSize=999").json()

course_id = get_course_id_from_course_no(course_no, mycourses)
course_data = session.get(f"https://learn.inside.dtu.dk/d2l/api/le/1.47/{course_id}/content/root/").json()
print(course_id)
print("Downloading...")

no_files = 0
create_directory(course_no)
root_dir = course_no
for tab in course_data:
    top_dir = root_dir + "/" + tab.get("Title")
    create_directory(top_dir)
    for content_item in tab.get("Structure"):
        item_id = content_item.get("Id")
        item_title = sanitize_filename(content_item.get("Title"))
        item_type = content_item.get("Type")
        if item_type == 0:
            #item is a MODULE
            module_id = item_id
            url = f"https://learn.inside.dtu.dk/d2l/api/le/1.47/{course_id}/content/modules/{module_id}/structure/"
            module_response = session.get(url)
            parent_dir = top_dir + "/" + item_title
            create_directory(parent_dir)
            for subfile in module_response.json():
                item_id = subfile.get("Id")
                item_title = sanitize_filename(subfile.get("Title"))
                durl = f"https://learn.inside.dtu.dk/d2l/le/content/{course_id}/topics/files/download/{item_id}/DirectFileTopicDownload"
                final_response = session.get(durl)
                if final_response.status_code != 200:
                    print(item_title, final_response.status_code)
                    continue
                download_file(item_title, final_response, parent_dir,suffix=get_file_type_from_headers(final_response.headers))
                #print(f"(debug-action) {final_response.status_code} Downloaded in {parent_dir}: {item_title}.{get_file_type_from_headers(final_response.headers)}")
                no_files += 1

            continue

        #item is a DOCUMENT
        url = f"https://learn.inside.dtu.dk/d2l/le/content/{course_id}/topics/files/download/{item_id}/DirectFileTopicDownload"

        response = session.get(url)

        if response.status_code != 200:
            print(item_title, response.status_code)
            continue

        # with open(document_title, "wb") as f:
        #     f.write(response.content)
        download_file(item_title, response, top_dir, suffix=get_file_type_from_headers(response.headers)  )

        #print(f"(debug-action) {response.status_code} Downloaded WHOLE: {item_title}.{get_file_type_from_headers(response.headers)}")

        no_files += 1

print(f"Downloaded {no_files} files")

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

