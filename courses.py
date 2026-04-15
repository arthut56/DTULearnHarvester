

def get_course_metadata(course_no, users_courses):
    results = []
    for course_metadata in users_courses.get("Courses"):
        if course_metadata.get("Name").split(" ")[0] == course_no:
            results.append(course_metadata)

    if len(results) == 0:
        print("Found no results")
        return None

    if len(results) > 1:
        print(f"WARNING: Found {len(results)} results: {list(map(lambda x : x["Code"], results))}. Using the first entry...")

    return results[0]
