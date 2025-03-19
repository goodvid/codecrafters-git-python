import sys
import os
import zlib
def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    # Uncomment this block to pass the first stage
    #
    command = sys.argv[1]
    if command == "init":
        os.mkdir(".git")
        os.mkdir(".git/objects")
        os.mkdir(".git/refs")
        with open(".git/HEAD", "w") as f:
            f.write("ref: refs/heads/main\n")
        print("Initialized git directory")
    elif command == "cat-file" and sys.argv[2] == '-p':
        dir = ".git/objects/{}/{}".format(sys.argv[3][0:2], sys.argv[3][2:])
        with open(dir,"rb") as f:
            file = zlib.decompress(f.read())
            header, content = file.split(b"\0", maxsplit=1)
            print(content.decode(encoding="utf-8"), end="")
    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
