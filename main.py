from university import University, College, Program

colleges = [
    College(1, "Engineering", 1990, 50000, 20000),
    College(2, "Business", 1985, 45000, 18000),
    College(3, "Arts", 1970, 30000, 15000),
]


def pick_college(available_colleges):
    print("Pick a college to establish with...")
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
    name = input("Please input the name of the university to start the game... ").strip()
    if not name:
        name = "Unnamed University"

    uni = University(name, 1900, 10_000_000)

    available_colleges = colleges.copy()

    selected_college = pick_college(available_colleges)
    uni.colleges.append(selected_college)

    available_colleges.remove(selected_college)

    print(f"You selected: {selected_college.name}")
    print(f"{selected_college.name} added to {uni.name}")

    program = create_program(selected_college)

    print("\n--- CURRENT STATUS ---")
    print(f"University: {uni.name}, Budget: {uni.budget}, Year: {uni.year}")
    print(f"College: {selected_college.name}, Tuition: {selected_college.tuition_fee}")
    print(f"Program: {program.name}, Quality: {program.quality}")


if __name__ == "__main__":
    main()