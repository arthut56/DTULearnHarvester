

def get_course_id_from_course_no(course_no, users_courses):
    results = []
    for course_metadata_ in users_courses.get("Courses"):
        if course_metadata_.get("Name").split(" ")[0] == course_no:
            results.append(course_metadata_.get("OrgUnitId"))

    if len(results) == 0:
        print("Found no results")
        return None

    if len(results) > 1:
        print(f"WARNING: Found {len(results)} results: {results}. Using the first entry...")

    return results[0]


def get_course_name_from_course_no(course_no, users_courses):
    for course_metadata_ in users_courses.get("Courses"):
        if course_metadata_.get("Name").split(" ")[0] == course_no:
            return course_metadata_.get("Name")
    return None
