with open("sample.txt","w") as file:
    #content=file.read()
    #print(content)
    file.write("Hello, World")
    file.writelines(["Alice","Bob","Cherry"])

try:
    with open("sample.txt","r") as file:
        content=file.read()
        print(content)
except FileNotFoundError:
    print("File not found.")