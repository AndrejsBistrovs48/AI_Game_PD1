import random

def generate_initial_numbers():
    # total_numbers is the total numbers  between 10000 and 20000 that is divided by 6 without remainder
    total_numbers= (19998-10002)//6 +1
    # generating 5 random numbers that define i's element in range
    nums=random.sample(range(total_numbers), 5)
    #calculating generated numbers
    generated_numbers=[10002+ 6*number for number in nums]

    return generated_numbers

#testing purposes
#print(generate_initial_numbers())

