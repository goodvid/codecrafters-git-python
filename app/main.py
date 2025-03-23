import sys
import os
import zlib
import hashlib

def read_blob():
    dir = ".git/objects/{}/{}".format(sys.argv[3][0:2], sys.argv[3][2:])
    with open(dir,"rb") as f:
            file = zlib.decompress(f.read())
            header, content = file.split(b"\0", maxsplit=1)
            print(content.decode(encoding="utf-8"), end="")
def write_blob(dir):
     #make hash from content + header
        with open(dir, "r") as f:
            content = f.read()
        header = f"blob {len(content)}\x00"
        content = header + content
        store = content.encode()
        sha = hashlib.sha1(store).hexdigest()
        #make folder
        dir = f".git/objects/{sha[0:2]}"
        os.mkdir(dir)
        #write to folder
        with open(f"{dir}/{sha[2:]}","wb") as f:
            f.write(zlib.compress(store))
        #print(sha, end="")
        return sha
def read_tree():
    dir = ".git/objects/{}/{}".format(sys.argv[3][0:2],sys.argv[3][2:])
    with open(dir,"rb") as f:
            file = zlib.decompress(f.read())
            content = file.split(b"\0")[1:]
            print(content[0].decode().split()[1])
            for c in content[1:]:
                if (len(c) > 20):
                    print(c[20: ].decode().split()[1])
def write_tree(dir):
    pass
    # for entry in cd:
        #if entry == file:
            #write blob and store sha
        #if entry == dir:
            #write tree and store sha
    #once all done, create list in form
    """
    tree <size>\0
    <mode> <name>\0<20_byte_sha>
    <mode> <name>\0<20_byte_sha>
    """
    #write to proper file
    #sha the list and return sha + print
    path = dir
    store = b""
    
    with os.scandir(path) as it:
        for entry in sorted(it, key=lambda e: e.name):
            full = os.path.join(path, entry.name)
            if entry.name == ".git":
                 continue
            if entry.is_file():
                #print(f"File: {entry.name}")
                
                sha_20 = write_blob(full) 
                sha_bytes = bytes.fromhex(sha_20)  # Convert hex to 20-byte binary
                string = f"100644 {entry.name}\x00".encode() + sha_bytes  # Ensure it's a binary string
                
            elif entry.is_dir():
                #print(f"Directory: {entry.name}")
                sha_20 = write_tree(full)  # Returns a 40-character hex SHA-1 string
                sha_bytes = bytes.fromhex(sha_20)  # Convert hex to 20-byte binary
                string = f"40000 {entry.name}\x00".encode() + sha_bytes  # Ensure it's a binary string
            store += string
    header = f"tree {len(store)}\x00"
    store = header.encode() + store
    sha = hashlib.sha1(store).hexdigest()
    git_path = f".git/objects/{sha[0:2]}"
    os.mkdir(git_path)
        #write to folder
    with open(f"{git_path}/{sha[2:]}","wb") as f:
            f.write(zlib.compress(store))
    #print(sha, end="")
    return sha

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    command = sys.argv[1]
    if command == "init":
        os.mkdir(".git")
        os.mkdir(".git/objects")
        os.mkdir(".git/refs")
        with open(".git/HEAD", "w") as f:
            f.write("ref: refs/heads/main\n")
        print("Initialized git directory")
    elif command == "cat-file" and sys.argv[2] == '-p':
        read_blob()
    elif command == "hash-object" and sys.argv[2] == '-w':
        print(write_blob(sys.argv[3]))
    elif command == "ls-tree" and sys.argv[2] == "--name-only":
        read_tree()
    elif command == "write-tree":
         print(write_tree(os.getcwd()))
    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
