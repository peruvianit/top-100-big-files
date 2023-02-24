import os


class FileDetails:

    __list_files = []
    __max_files = 50
    __file_analized_count = 0
    __file_analized_size = 0

    def __init__(self, name, size):
        assert name is not None, f"Name is required"
        assert size is not None, f"Size is required"
        self.name = name
        self.size = size

    @classmethod
    def get_list_file(cls):
        return FileDetails.__list_files

    @classmethod
    def clear_list_file(cls):
        return FileDetails.__list_files.clear()

    @classmethod
    def add_file(cls, file_details):
        is_add_file = False

        list_files = FileDetails.__list_files
        list_files_size = len(list_files)
        min_size_file_list = 0 if list_files_size == 0 else list_files[list_files_size-1].size

        # remove last file with the minor size
        if len(list_files) == FileDetails.__max_files:
            if file_details.size > min_size_file_list:
                list_files.pop(list_files_size-1)

        if len(list_files) < FileDetails.__max_files:
            is_add_file = True
            list_files.append(file_details)
            # sorted list
            list_files.sort(key=lambda file_detail: file_detail.size, reverse=True)

        FileDetails.__file_analized_count = FileDetails.__file_analized_count + 1
        FileDetails.__file_analized_size = FileDetails.__file_analized_size + file_details.size

        return is_add_file

    @classmethod
    def remove_file(cls, name):
        name = os.path.abspath(name)
        for idx, item in enumerate(FileDetails.__list_files):
            if os.path.abspath(item.name) == name:
                FileDetails.__list_files.pop(idx)
                break

        print('Il elemento stato cancellato e rimangono nella lista ', len(FileDetails.__list_files), 'elementi' )

    @classmethod
    def total_size_analized(cls):
        return FileDetails.__file_analized_size

    @classmethod
    def total_files_count(cls):
        return FileDetails.__file_analized_count

    @classmethod
    def analizer_extensions(cls):
        extensions_files_dic = {}
        for file in FileDetails.__list_files:
            file_name, ext = os.path.splitext(file.name)
            print(f'([{file_name}]::[{ext}]')
            if ext == '':
                ext = "N/A"

            if ext in extensions_files_dic:
                extensions_files_dic[ext] = extensions_files_dic.get(ext) + 1
            else:
                extensions_files_dic[ext] = 1

        return extensions_files_dic
