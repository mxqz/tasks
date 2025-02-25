import re

def evaluate_password(password):
    score = 1
    
    if len(password) >= 8:
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if len(re.findall(r'\d', password)) >= 2:
        score += 1
    if re.search(r'[^a-zA-Z0-9]', password):
        score = 0 
    
    return score

if __name__ == "__main__":
    while True:
        pwd = input("Password: ")
        score = evaluate_password(pwd)
        print(f"Strength: {'*' * score}")
