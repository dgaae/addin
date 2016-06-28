import os
import re
import zipfile
import compileall

current_path = os.path.dirname(os.path.abspath(__file__))

compileall.compile_dir(os.path.join(current_path,*("Install","addin")), force=True)

out_zip_name = os.path.join(current_path, 
                            "DGAAE" + ".esriaddin")
if os.path.exists(out_zip_name):
    copy = out_zip_name
    i = 0
    while os.path.exists(copy):
        i+=1
        copy = os.path.join(current_path, 
                                "DGAAE_{0}".format(i) + ".esriaddin")
    os.rename(out_zip_name,copy)

BACKUP_FILE_PATTERN = re.compile(".*_addin_[0-9]+[.]py$", re.IGNORECASE)

def looks_like_a_backup(filename):
    return bool(BACKUP_FILE_PATTERN.match(filename))

with zipfile.ZipFile(out_zip_name, 'w', zipfile.ZIP_DEFLATED) as zip_file:
    for filename in ('config.xml', 'README.txt', 'makeaddin.py'):
        zip_file.write(os.path.join(current_path, filename), filename)
    dirs_to_add = ['Images', 'Install']
    for directory in dirs_to_add:
        for (path, dirs, files) in os.walk(os.path.join(current_path,
                                                        directory)):
            archive_path = os.path.relpath(path, current_path)
            found_file = False
            for file in (f for f in files if not looks_like_a_backup(f)):
                archive_file = os.path.join(archive_path, file)
                print archive_file
                zip_file.write(os.path.join(path, file), archive_file)
                found_file = True
            if not found_file:
                zip_file.writestr(os.path.join(archive_path,
                                               'placeholder.txt'),
                                  "(Empty directory)")