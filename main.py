from university import University, College, Program
import random

colleges = [
    College(1, "Engineering", 1990, 50000, 20000),
    College(2, "Business", 1985, 45000, 18000),
    College(3, "Arts", 1970, 30000, 15000),
]

FACULTY_TIERS = ["S", "A", "B", "C", "D"]

def main_menu():
    print("\n--- MAIN MENU ---")
    print("1. Pick a College to Establish")
    print("2. Create a Program for a College")
    print("3. View University Status")
    print("4. Hire Faculty for a Program")
    print("5. Exit")
    choice = input("Select an option (1–5): ").strip()
    return choice

def view_status(uni):
    print("\n--- CURRENT STATUS ---")
    print(f"University: {uni.name}, Budget: {uni.budget}, Year: {uni.year}")

    if not uni.colleges:
        print("No colleges added yet.")
    else:
        for college in uni.colleges:
            print(f"\nCollege: {college.name}, Tuition: {college.tuition_fee:,}")

            if hasattr(college, "programs") and college.programs:
                for program in college.programs:
                    print(f"  - Program: {program.name}, Quality: {program.quality}, "
                        f"Students: {program.student_stats.total}/{program.capacity} ({program.size})")

                    f = program.faculty_stats
                    print(f"    Faculty: Total={f.total}, "
                        f"S={f.class_s}, A={f.class_a}, B={f.class_b}, "
                        f"C={f.class_c}, D={f.class_d}, "
                        f"Expenses=${f.total_expenses:,}")

                    if hasattr(program, "student_stats"):
                        s = program.student_stats
                        print(f"    Students: Total={s.total}, "
                            f"S={s.class_s}, A={s.class_a}, B={s.class_b}, "
                            f"C={s.class_c}, D={s.class_d}")
                    else:
                        print("    No students yet.")
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

    print("Choose program size:")
    print("1. Small (20–50 students)")
    print("2. Medium (50–200 students)")
    print("3. Large (200–500 students)")

    size_choice = input("Enter choice (1–3): ").strip()
    if size_choice == "1":
        capacity = int(input("Enter capacity for Small program (20–50): "))
        capacity = max(20, min(capacity, 50))
    elif size_choice == "2":
        capacity = int(input("Enter capacity for Medium program (50–200): "))
        capacity = max(50, min(capacity, 200))
    elif size_choice == "3":
        capacity = int(input("Enter capacity for Large program (200–500): "))
        capacity = max(200, min(capacity, 500))
    else:
        capacity = 100
        print("Invalid choice, defaulting to Medium (100 students)")

    program_id = len(college.programs) + 1
    program_year = 1900

    program = Program(program_id, program_name, program_year, capacity)
    college.programs.append(program)

    print(f"Program '{program.name}' established with capacity {program.capacity} ({program.size})")
    return program

def hire_faculty(program, university):
    print("\n--- Faculty Hiring ---")

    stats = program.faculty_stats

    candidates = []
    for _ in range(3):
        tier = random.choice(FACULTY_TIERS)

        if tier == "S":
            salary = stats.class_s_expense
            quality = 5
        elif tier == "A":
            salary = stats.class_a_expense
            quality = 4
        elif tier == "B":
            salary = stats.class_b_expense
            quality = 3
        elif tier == "C":
            salary = stats.class_c_expense
            quality = 2
        elif tier == "D":
            salary = stats.class_d_expense
            quality = 1

        candidate = {
            "tier": tier,
            "salary": salary,
            "quality": quality
        }
        candidates.append(candidate)

    for i, c in enumerate(candidates, start=1):
        print(f"{i}. Class {c['tier']} Faculty")
        print(f"   Salary: ${c['salary']:,}")
        print(f"   Program Quality +{c['quality']}")

    cancel_option = len(candidates) + 1
    print(f"{cancel_option}. Cancel")

    while True:
        try:
            choice = int(input(f"Choose a candidate (1–{cancel_option}): "))

            if choice == cancel_option:
                print("Hiring canceled.")
                return

            if 1 <= choice <= len(candidates):
                selected = candidates[choice - 1]

                if university.budget < selected["salary"]:
                    print("Not enough budget to hire this faculty.")
                    return

                university.budget -= selected["salary"]

                stats.total += 1

                tier = selected["tier"]
                if tier == "S":
                    stats.class_s += 1
                elif tier == "A":
                    stats.class_a += 1
                elif tier == "B":
                    stats.class_b += 1
                elif tier == "C":
                    stats.class_c += 1
                elif tier == "D":
                    stats.class_d += 1

                print(f"Successfully hired a Class {tier} faculty!")
                print(f"Total faculty in program: {stats.total}")
                print(f"Total faculty expenses: ${stats.total_expenses:,}")

                return

            print(f"Please choose 1–{cancel_option}.")
        except ValueError:
            print("Please enter a valid number.")

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

        elif choice == "4":
            if not uni.colleges:
                print("You must have a college first.")
                continue

            print("\nChoose a college:")
            for i, college in enumerate(uni.colleges, start=1):
                print(f"{i}. {college.name}")

            try:
                c_idx = int(input("Enter choice: ")) - 1
                if c_idx < 0 or c_idx >= len(uni.colleges):
                    raise ValueError
            except ValueError:
                print("Invalid choice.")
                continue

            selected_college = uni.colleges[c_idx]

            if not selected_college.programs:
                print("This college has no programs yet.")
                continue

            print("\nChoose a program:")
            for i, program in enumerate(selected_college.programs, start=1):
                print(f"{i}. {program.name}")

            try:
                p_idx = int(input("Enter choice: ")) - 1
                if p_idx < 0 or p_idx >= len(selected_college.programs):
                    raise ValueError
            except ValueError:
                print("Invalid choice.")
                continue

            selected_program = selected_college.programs[p_idx]

            hire_faculty(selected_program, uni)

        # Exit
        elif choice == "5":
            print("Exiting game. Goodbye!")
            break

        else:
            print("Invalid menu option. Please choose 1–4.")

if __name__ == "__main__":
    main()