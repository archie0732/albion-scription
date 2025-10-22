import os


def rename_img(folder_path: str, rename_file_name: str):
    ALLOWED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif"]

    if not os.path.isdir(folder_path):
        print(f"cannot find the folder in path {folder_path}")
        return

    print("start rename image")

    try:
        file_list = os.listdir(folder_path)
    except Exception as e:
        print(f"cannot read the file, {e}")
        return

    images = []

    for file in file_list:
        name, ext = os.path.splitext(file)
        if ext.lower() in ALLOWED_EXTENSIONS:
            images.append(file)

    if not images:
        print("cannot find any images in this folder")
        return

    count = 1

    for index, old_filename in enumerate(images):
        new_filename = f"{rename_file_name}_{index+1}{ext}"

        old_filepath = os.path.join(folder_path, old_filename)
        new_filepath = os.path.join(folder_path, new_filename)

        try:
            os.rename(old_filepath, new_filepath)
            print(f"{index+1}. {old_filename} -> {new_filename}")
        except Exception as e:
            print(f"Error, {e}")


path = (input("Enter folder path: ")).strip()
filename = input("Enter images name: ").strip()
if filename == "" or filename == " ":
    raise NameError("file name cannot be space")
rename_img(path, filename)
