username = input("Enter username: ")
password = input("Enter password: ")

info = open("studentinfo.txt", "r")
info_list = info.read().split()
stored_user = info_list[0]
stored_pass = info_list[1]
stored_name = info_list[2]

def check_username(user):
    return user == stored_user
def check_password(pwd):
    return pwd == stored_pass

if check_username(username) and check_password(password):
    print("Access Granted")
else:
    print("Access Denied")