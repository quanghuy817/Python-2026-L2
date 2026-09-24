def remove_dollar_sign(s):
    return s.replace("$", "")
if __name__ == "__main__":
    print(remove_dollar_sign("$100"))    
    print(remove_dollar_sign("$1$2$3"))   
    print(remove_dollar_sign("no dollar"))  