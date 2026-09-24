num = int(input("Enter a number? "))
total = 0
for i in range(1, num):
    if num % i == 0:
        total += i
if total == num:
    print(f"{num} is a perfect number")
else:
    print(f"{num} is a NOT perfect number")