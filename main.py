import os

def main():
    print("Hello from test-interp!")
    
    folders = ['remove', 'mesh', 'results']
    for folder in folders:
        os.makedirs(folder, exist_ok=True)


if __name__ == "__main__":
    main()
