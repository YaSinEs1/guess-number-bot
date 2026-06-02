
import random

name = input("what is your name? ")
play_again = "Y"

while play_again.upper() == "Y":
    answer = random.randint(1, 99)
    print("\nI thought of a number between 1 and 99 ")
    attempts = 0

    while True:
        try:
            guess = int(input("guess a number between 1 to 99: "))
            
            if guess < 1 or guess > 99:
                print("please enter a number between 1 and 99 ")
                continue
            attempts += 1
            if guess < answer:
                 print("the answer is larger!")       
            elif guess > answer:
                print("the answer is smaller!")   
            else:
                print(f"\nYou got it right, {name}! 😎")   
                print(f"Number of attempts: {attempts}")
                break

        except ValueError:
            print("please enter a Valid number!")

    play_again = input("\nDo you want to play again? (Y or N):").upper()
    while play_again not in ["Y", "N"]:
        print("You can only answer whit Y or N.")

        play_again = input("do you want to play again? (Y or N): ").upper()
    
print(f"\nBye {name}!✋")