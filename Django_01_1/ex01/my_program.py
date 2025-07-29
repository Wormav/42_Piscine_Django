from local_lib.path import Path

def main()-> None:
    #Create folder "folder"
    folder = Path('folder')
    folder.mkdir_p()

    #Create file "file" in folder
    file = folder / "file.txt"
    file.write_text('Hello world !')

    #read file
    content = file.read_text()
    print(content)

if __name__ == "__main__":
    main()