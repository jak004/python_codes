import re
def clear_text(text):
    #Remove punctuation
    text=re.sub(r"[^\w\s]","",text)
    #Remove extra spaces
    text="".join(text.split())
#Convert to lowercase
    return text.lower()
input_text="  Hello,World!!!. Welcome to Python, programming...  "
cleaned_text=clear_text(input_text)
print("Cleaned Text:",cleaned_text)