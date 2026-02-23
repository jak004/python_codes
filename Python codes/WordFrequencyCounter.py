
import  nummpy as np
sentence=input("Enter a sentence:")



#Split sentence into list 
words=sentence.split()
 
 #Initialize a dictionary
word_count={}
 
 #count word frequency
for word in words:
    word=word.lower()
    if word in word_count:
       word_count[word]+=1
    else:
       word_count[word]=1
        
        
print(word_count)