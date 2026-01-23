from university import University, College, Program

colleges = [
    College(1, "Engineering", 1990, 50000, 20000),
    College(2, "Business", 1985, 45000, 18000),
    College(3, "Arts", 1970, 30000, 15000),
]

def main_menu():
    print("\n--- MAIN MENU ---")
    print("1. Pick a College to Establish")
    print("2. Create a Program for a College")
    print("3. View University Status")
    print("4. Exit")
    choice = input("Select an option (1–4): ").strip()
    return choice

def view_status(uni):
    print("\n--- CURRENT STATUS ---")
    print(f"University: {uni.name}, Budget: {uni.budget}, Year: {uni.year}")

    if not uni.colleges:
        print("No colleges added yet.")
    else:
        for college in uni.colleges:
            print(f"\nCollege: {college.name}, Tuition: {college.tuition_fee}")
            if hasattr(college, "programs") and college.programs:
                for program in college.programs:
                    print(f"  - Program: {program.name}, Quality: {program.quality}")
            else:
                print("  No programs yet.")

def pick_college(available_colleges):
    print("Colleges")
    for college in available_colleges:
        print(f"{college.id}. {college.name}")

    while True:
        try:
            choice = int(input("Enter a college ID: "))
            for college in available_colleges:
                if choice == college.id:
                    return college
            print("Please enter one of the available college IDs.")
        except ValueError:
            print("Please enter a valid number.")


def create_program(college):
    program_name = input("Enter the name of a program to establish: ").strip()
    if not program_name:
        program_name = "General Studies"

    program_id = len(college.programs) + 1
    program_year = 1900

    program = Program(program_id, program_name, program_year)
    college.programs.append(program)

    return program


def main():
    print("Hello, Welcome to the University Creation Simulator (Pending)!")
    print("Please input the name of the university to start the game... ")
    name = input().strip()
    if not name:
        name = "Unnamed University"

    uni = University(name, 1900, 10_000_000)

    available_colleges = colleges.copy()

    while True:
        choice = main_menu()

        # Pick a College
        if choice == "1":
            if not available_colleges:
                print("No more colleges available to pick.")
                continue

            selected_college = pick_college(available_colleges)
            uni.colleges.append(selected_college)
            available_colleges.remove(selected_college)

            print(f"You selected: {selected_college.name}")
            print(f"{selected_college.name} added to {uni.name}")

        # Create a Program
        elif choice == "2":
            if not uni.colleges:
                print("You must pick a college first.")
                continue

            print("\nChoose a college to add a program to:")
            for i, college in enumerate(uni.colleges, start=1):
                print(f"{i}. {college.name}")

            try:
                idx = int(input("Enter choice: ")) - 1
                if idx < 0 or idx >= len(uni.colleges):
                    raise ValueError
            except ValueError:
                print("Invalid choice.")
                continue

            selected_college = uni.colleges[idx]
            program = create_program(selected_college)

            print(f"Program '{program.name}' added to {selected_college.name}")

        # View Status
        elif choice == "3":
            view_status(uni)

        # Exit
        elif choice == "4":
            print("Exiting game. Goodbye!")
            break

        else:
            print("Invalid menu option. Please choose 1–4.")

if __name__ == "__main__":
    main()