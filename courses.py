

def get_course_id_from_course_no(course_no, users_courses):
    for course_metadata_ in users_courses.get("Courses"):
        if course_metadata_.get("Name").split(" ")[0] == course_no:
            return course_metadata_.get("OrgUnitId")
