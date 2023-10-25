

def pswd_check(passwd):
     
    SpecialSym =['$', '@', '#', '%']
    if len(passwd) < 8:
        return 'length should be at least 8'
         
    if not any(char.isdigit() for char in passwd):
        return 'Password should have at least one numeral'
         
    if not any(char.isupper() for char in passwd):
        return 'Password should have at least one uppercase letter'
         
    if not any(char.islower() for char in passwd):
        return 'Password should have at least one lowercase letter'
         
    if not any(char in SpecialSym for char in passwd):
        return 'Password should have at least one of the symbols $@#'
    
    return True