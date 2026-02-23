#number=10
#if number > 0:
    #print("Positive number")
#elif number == 0:
    #print("Zero")
#else:
# print("Negative number")


#loop through a list
# fruits=["apples","bananas","cherries"]
#for fruit in fruits:
    #print(fruit)
   
   
   
#for i in range(5):
    #print(i)
    
    
#Prime Numbers
num=int(input("Enter a number: "))
if num > 1:
    for i in range(2,num):
        if (num % i) == 0:
            print(num,"is not a prime number")
            break
    else:
        print(num,"is a prime number") 