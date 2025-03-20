import datetime
import os
import re
import sys #tbd
from processing import load_csv, add_entry, add_registration
# from utilities import get_erps

def register_participant():
    """For registering participants who were unable to register via the form. Stores the participant details in a separate CSV file, having the same details as those taken in the form. It also creates an entry for the participant (I might add a yes/no option for this).
    """

    global invalid

    timestamp = datetime.datetime.now()
    name = input("\nName: ")
    erp = input("ERP ID: ").upper().strip() # Taking ERP twice? Possible to do something better or its just thinking too much?
    year = input("Year: ") # Providing options possible
    branch = input("Branch: ") # Providing options possible

    try:
        phone = int(input("Phone Number: "))
    except ValueError:
        invalid = 6
        main()

    email = input("Email: ")
    if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
        invalid = 7
        main()

    add_registration(timestamp, name, erp, year, branch, phone, email)
    add_entry(timestamp, erp)

    invalid = 4
    main()

def check_in():
    
    global invalid

    erps = [erp[1] for erp in form_registrations]

    if os.path.exists(r"data\\manual_registration.csv"):
        print(manual_registrations)
        erps += [erp[1] for erp in manual_registrations]

    erp = input("\nERP ID: ").upper().strip()
    
    if erp in erps:
        invalid = 2
        add_entry(datetime.datetime.now(), erp)
        main()
    else:
        invalid = 3
        main() # Option to directly go by asking something like. Want to register? (Yes/No)

def invalid_warning(code: str) -> str:
    """Returns corresponding error warning for to be displayed in CLI.

    Args:
        code (int): Code representing the desired message.

    Returns:
        str: Resulting error message.
    """

    # Might need a better name than invalid for this variable
    global invalid

    if code == 1:
        return "Invalid input!\n"
    elif code == 2:
        return "Checked in!\n"
    elif code == 3:
        return "ERP ID is not registered!\n"
    elif code == 4:
        return "Registered!\n"
    elif code == 5:
        return "Dataset loaded!\n"
    elif code == 6:
        return "Invalid phone number!\n"
    elif code == 7:
        return "Invalid email address!\n"

def main():
    
    global form_registrations, manual_registrations, invalid, start

    # Loading parts lying within start means the program will have to be re-started whenever the dataset is updated.
    if start == 0:
        data = input("Enter file name: ") # Need to add exit option (is it necessary?)

        # data = "sample" # TESTING!!

        # Custom data path isn't being used in this iteration
        form_registrations = load_csv(data) # Can be followed by different outcomes based on possible scenarios. Show data has been loaded for 5 sec (too unrealistic?)

        if form_registrations == -1:
            print("\nDataset doesn't exist!\n")
            main()
        else:
            invalid = 5
            start = 1

        # Will no doubt load after creation as main is called in register_participant(), so that corner case is covered.
        if os.path.exists(r"data\\manual_registration.csv"):
            manual_registrations = load_csv("manual_registration")

    print("""\n1 Add Entry\n2 Register Participant\n3 Manual Entry\n4 Export PDF\n5 Close Dataset\n""") # name feature not added yet
    
    if invalid != 0:
        print(invalid_warning(invalid))
        invalid = 0

    choice = int(input("Enter choice: "))

    if choice == 1:
        check_in()
    elif choice == 2:
        register_participant()
    elif choice == 3:
        pass
    elif choice == 4:
        pass
    elif choice == 5:
        start = 0
        print("\nClosing dataset...\n")
        main()
    else:
        invalid = 1
        main()

if __name__ == "__main__":
    global invalid, start
    start, invalid = 0, 0
    main()
