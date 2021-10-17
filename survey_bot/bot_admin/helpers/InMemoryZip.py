import zipfile
import io


class InMemoryZip(object):
    def __init__(self):
        self.in_memory_zip = io.BytesIO()


    def append(self, filename_in_zip, file_contents):
        zip_file = zipfile.ZipFile(file=self.in_memory_zip, 
                             mode='a', 
                             compression=zipfile.ZIP_DEFLATED, 
                             allowZip64=False)
        
        zip_file.writestr(filename_in_zip, file_contents)

        for file in zip_file.filelist:
            file.create_system = 0        

        return self


    def read(self):
        self.in_memory_zip.seek(0)
        return self.in_memory_zip.read()


    def save_to_file(self, filename):
        with open(filename, 'wb') as f:
            f.write(self.read())
