import shutil
import os
from blocks import generate_page

# copy contents from source to destination
def copy_contents(source, destination):
    # source folder must be present
    if not os.path.exists(source):
        raise Exception("source doenst exist")

    # if destination doesn't exist, create it
    if not os.path.exists(destination):
        os.mkdir(destination)
    # destination exists
    print("destination exists")
    # clear destination directory
    shutil.rmtree(destination)
    os.mkdir(destination)

    # destination is now empty, copy contents from source
    print("clearing destination")
    print(f"copying contents from {source}")
    
    recursive_helper(source, destination)
    

def recursive_helper(src, des):
    ls = os.listdir(src)
    for item in ls:
        try:
            des_path = os.path.join(des, item)
            src_path = os.path.join(src, item)
            if os.path.isfile(src_path):
                print(f"path of file: {src_path}")
                shutil.copy(src_path, des_path)
            else:
                # it is a directory, add it to the path
                os.mkdir(des_path)
                print(f"directory: {des_path} created successfully")
                recursive_helper(src_path, des_path)
        except IOError as e:
            print(f"could not copy {e}")
        except Exception as e:
            print(f"unexpected error. {e}")


def main():
    copy_contents("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")

main()
