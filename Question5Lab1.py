colors = ["Blue", "Yellow", "Purple", "Red", "Orange"]
color = input("What is your favorite color? ")
if color in colors:
    index = colors.index(color)
    print(f"Your color is at index {index} in my list")
else:
    print("Sorry, I could not find your color")