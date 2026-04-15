from file_utils import *


def download_everything(session, course_id, course_name, course_rootdata):
    root_dir = course_name
    create_directory(root_dir)

    no_downloads = 0
    for tab in course_rootdata:
        tab_dir = root_dir + "/" + sanitize_filename(tab.get("Title"))
        create_directory(tab_dir)

        for content_item in tab.get("Structure"):
            item_id    = content_item.get("Id")
            item_title = sanitize_filename(content_item.get("Title"))
            item_type  = content_item.get("Type")

            no_downloads = no_downloads + download_item(session, course_id, item_id, item_title, item_type, tab_dir)
            #if item type 0 then recurse

    return no_downloads

"""An item can be a module (type 0) or a file (type 1).
Modules need to be unpackaged and recursed to download."""
def download_item(session, course_id, item_id, item_title, item_type, tab_dir):
    if item_type == 0:
        #item is a module
        module_url = f"https://learn.inside.dtu.dk/d2l/api/le/1.47/{course_id}/content/modules/{item_id}/structure/"
        response = session.get(module_url)
        module_dir = tab_dir + "/" + item_title
        create_directory(module_dir)
        no_downloads = 0
        for subfile in response.json():
            submodule_id = subfile.get("Id")
            submodule_title = sanitize_filename(subfile.get("Title"))
            submodule_type = subfile.get("Type")
            download_item(session, course_id, submodule_id, submodule_title, submodule_type, module_dir)
            no_downloads += 1

        return no_downloads

        #define this module as a directory, download files under module

    if item_type == 1:
        file_url = f"https://learn.inside.dtu.dk/d2l/le/content/{course_id}/topics/files/download/{item_id}/DirectFileTopicDownload"
        response = session.get(file_url)

        if response.status_code != 200:
            print(f"Unable to download: {item_title} - HTTP {response.status_code}")
            return 0

        download_file(item_title, response, tab_dir, file_extension=get_file_extension_from_headers(response.headers))

        return 1

    return 0


def download_file(name, api_response, directory="", file_extension="pdf"):
    filename = os.path.join(directory, name)
    with open(f"{filename}.{file_extension}", "wb") as f:
        f.write(api_response.content)
