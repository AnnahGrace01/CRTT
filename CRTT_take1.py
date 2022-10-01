import random
import time

input("Welcome: ")
player_1 = input("Player one: ")
player_2 = input("Player two: ")

for i in range(3):
    print("Get ready...")
    time.sleep(1)
    print("set...")
    time.sleep(random.randint(1, 8))
    pressed = input("GO!!")
    if pressed == "":
        print("{} wins!".format(player_1)),
        time.sleep(1)
        blast = input("{}, what blast level do you want to deliver? Select 1-10 then hit enter: ".format(player_1))
        print("{}".format(player_1), "chose blast level {}".format(blast), "\n{} stand by for blast".format(player_2))
    if pressed == " ":
        print("{} wins!".format(player_2)),
        time.sleep(1)
        blast = input("{}, what blast level do you want to deliver? Select 1-10 then hit enter: ".format(player_2)),
        print("{}".format(player_2), "chose blast level {}".format(blast), "\n{}, stand by for blast".format(player_1))
    time.sleep(4)

print("Game Over \nThanks for playing.")
time.sleep(10)

with open('p_number.txt', 'w') as f:
    f.write(data)
