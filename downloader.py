from file_utils import *


class CourseDownloader:

    MODULE_ACCESS_BASE_URL = "https://learn.inside.dtu.dk/d2l/api/le/1.47/"
    FILE_DOWNLOAD_BASE_URL = "https://learn.inside.dtu.dk/d2l/le/content/"

    def __init__(self, session, course_id, course_name, format=default_format):
        self.session     = session
        self.course_id   = course_id
        self.course_name = sanitize_filename(course_name)
        self.format = format


    def download_everything(self, course_rootdata):
        root_dir = self.format(self.course_name).split(",")[0]
        create_directory(root_dir)

        no_downloads = 0
        for tab in course_rootdata:
            tab_dir = self.format(root_dir + "/" + sanitize_filename(tab.get("Title")))
            create_directory(tab_dir)

            for content_item in tab.get("Structure"):
                item_id    = content_item.get("Id")
                item_title = sanitize_filename(content_item.get("Title"))
                item_type  = content_item.get("Type")

                no_downloads = no_downloads + self.download_item(item_id, item_title, item_type, tab_dir)
                #if item type 0 then recurse

        return no_downloads


    """An item can be a module (type 0) or a file (type 1).
    Modules need to be unpackaged and recursed to download."""
    def download_item(self, item_id, item_title, item_type, tab_dir):
        if item_type == 0:
            #item is a module
            module_url = f"{self.MODULE_ACCESS_BASE_URL}{self.course_id}/content/modules/{item_id}/structure/"
            response = self.session.get(module_url)
            module_dir = self.format(tab_dir + "/" + item_title)
            create_directory(module_dir)
            no_downloads = 0
            for subfile in response.json():
                submodule_id = subfile.get("Id")
                submodule_title = sanitize_filename(subfile.get("Title"))
                submodule_type = subfile.get("Type")
                no_downloads += self.download_item(submodule_id, submodule_title, submodule_type, module_dir)

            return no_downloads

        if item_type == 1:
            file_url = f"{self.FILE_DOWNLOAD_BASE_URL}{self.course_id}/topics/files/download/{item_id}/DirectFileTopicDownload"
            response = self.session.get(file_url)

            if response.status_code != 200:
                print(f"Unable to download: {item_title} - HTTP {response.status_code}")
                return 0

            write_file(self.format(item_title), response, tab_dir, file_extension=get_file_extension_from_headers(response.headers))

            return 1

        return 0
