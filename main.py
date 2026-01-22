from university import University, College, Program

colleges = [
    College(1, "Engineering", 1990, 50000, 20000),
    College(2, "Business", 1985, 45000, 18000),
    College(3, "Arts", 1970, 30000, 15000),
]

def main():
    print("Hello, Welcome to the University Creation Simulator (Pending)!")
    name = input("Please input the name of the university to start the game...")
    uni = University(name, 1900, 10_000_000)

    print("Pick a college to start with...")
    while True:
        try:
            coll = int(input("Please Input 1 - 3 for Engineering, Business, Arts in order... "))
            break
        except ValueError:
            print("Please enter a valid number (1–3).")

    selected_college = None
    for college in colleges:
        if coll == college.id:
            selected_college = college
            break

    if selected_college:
        uni.colleges.append(selected_college)
        print(f"You selected: {selected_college.name}")
        print(f"{selected_college.name} added to {uni.name}")
    else:
        print("Invalid choice. Please restart and choose 1–3.")

    program_name = input("Enter the name of the first program to establish: ")
    program_year = 1900

    program = Program(1, program_name, program_year)
    selected_college.programs.append(program)

    print(f"University: {uni.name}, Budget: {uni.budget}, Year: {uni.year}")
    print(f"College: {college.name}, Tuition: {college.tuition_fee}")
    print(f"Program: {program.name}, Quality: {program.quality}")

if __name__ == "__main__":
    main()