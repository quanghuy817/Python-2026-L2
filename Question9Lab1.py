def factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result
if __name__ == "__main__":
    print(factorial(0)) 
    print(factorial(5))  
    print(factorial(6))  