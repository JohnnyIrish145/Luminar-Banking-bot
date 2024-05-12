import json
filename = "Bal.json"

# Retreives data on "Bal.json"
def view_data():
    with open(filename, mode="r") as f:
        temp = json.load(f)
        f.close()
    entry = temp["accounts"]
    return entry

# Gets a balance of a user by there id
def my_balance(user_id):
    entry = view_data()
    data_length = len(entry) - 1
    i = 0
    for entry in entry:
        entry3 = int(entry["user_id"])
        user_id = int(user_id)
        if entry3 == user_id:
            balance = entry["balance"]
            break
        elif data_length == i or data_length < i:
            with open(filename) as f:
                temp = json.load(f)
                f.close()
            entry = temp["accounts"]
            with open(filename, mode = "w") as f:
                entry = temp["accounts"]
                new_account = {"user_id": user_id, "balance": 0}
                entry.append(new_account)
                temp = json.dump(temp, f, indent=4)
            f.close()
            balance = "Acount has been made"
            break
        else:
            i+=1
    return balance

# Finds if user has an account, if not, makes an account for that user
def response_balance(user_id):
    process = my_balance(user_id)
    if process == "Acount has been made":
        response = "null"
    else:
        response = process
    return response 

# Payment manager
# Opens file, get data about both user (sender and receiver)
# Checks the balance of both users
# Takes away and adds to their respective balances
def payment(sender, receiver, amount, sender_old_balance):
    entry = view_data()
    data_length = len(entry) - 1
    i = 0
    entry2 = entry
    for entry in entry:
        entry3 = int(entry["user_id"])
        if entry3 == receiver:
            receiver = int(receiver)
            receiver_old_balance = int(my_balance(receiver))
            receiver_old_balance = receiver_old_balance
            receiver_new_balance = receiver_old_balance + int(amount)
            balance = entry["balance"]
            with open(filename) as f:
                temp = json.load(f)
                f.close()
            entry = temp["accounts"]
            del entry[i]
            with open(filename, mode = "w") as f:
                entry = temp["accounts"]
                entry2 = entry2[i]
                entry2 = entry2["user_id"]
                append_account = {"user_id": entry2, "balance": receiver_new_balance}                
                entry.append(append_account)
                temp = json.dump(temp, f, indent=4)
                f.close()
            entry = view_data()
            data_length = len(entry) - 1
            i = 0
            entry2 = entry
            for entry in entry:
                entry3 = int(entry["user_id"])
                if entry3 == sender:
                    sender_new_balance = int(sender_old_balance) - amount
                    balance = entry["balance"]
                    with open(filename) as f:
                        temp = json.load(f)
                        f.close()
                    entry = temp["accounts"]
                    del entry[i]
                    with open(filename, mode = "w") as f:
                        #entry2 = entry2["user_id"]
                        append_account = {"user_id": sender, "balance": sender_new_balance}                
                        entry.append(append_account)
                        temp = json.dump(temp, f, indent=4)
                        f.close()
                i+=1
            balance = True
            break
        elif data_length == i or data_length < i:
            balance = False
            receiver_old_balance = 0
            print("Account does not exist")
            break
        else:
            i+=1
    return balance, receiver_old_balance