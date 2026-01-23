from university import University, College, Program, StudentStats, FacultyStats
import random
import json

colleges = [
    College(1, "Engineering", 1990, 50000, 20000),
    College(2, "Business", 1985, 45000, 18000),
    College(3, "Arts", 1970, 30000, 15000),
]

FACULTY_TIERS = ["S", "A", "B", "C", "D"]

def run_semester(university):
    print(f"\n--- Running Semester {university.year} ---\n")
    university.year += 1

    university.university_points = 0

    for college in university.colleges:
        print(f"Processing College: {college.name}")

        university.budget -= college.base_expenses
        print(f"  Deducted base expenses: ${college.base_expenses:,}")

        college.college_points = 0

        for program in college.programs:
            admit_students_roll(program, university)

            f = program.faculty_stats
            quality_increase = f.class_s * 3 + f.class_a * 2 + f.class_b * 1
            program.quality += quality_increase
            program.quality = min(program.quality, 100)
            print(f"  Program '{program.name}' quality increased by {quality_increase}, now {program.quality}")

            student_points = (
                program.student_stats.class_s * 10 +
                program.student_stats.class_a * 6 +
                program.student_stats.class_b * 4 +
                program.student_stats.class_c * 2 +
                program.student_stats.class_d * 1
            )

            faculty_points = (
                f.class_s * 10 +
                f.class_a * 7 +
                f.class_b * 5 +
                f.class_c * 3 +
                f.class_d * 1
            )

            program.program_points = student_points + faculty_points
            print(f"    Program points earned this semester: {program.program_points}")

            college.college_points += program.program_points

            s_leave = int(program.student_stats.class_s * 0.1)
            a_leave = int(program.student_stats.class_a * 0.05)
            d_leave = int(program.student_stats.class_d * 0.2)
            total_leaving = s_leave + a_leave + d_leave

            program.student_stats.total -= total_leaving
            program.student_stats.class_s -= s_leave
            program.student_stats.class_a -= a_leave
            program.student_stats.class_d -= d_leave

            print(f"  {total_leaving} students graduated/dropped from '{program.name}'")

            faculty_expense = f.total_expenses
            university.budget -= faculty_expense
            print(f"  Paid faculty salaries: ${faculty_expense:,}")

        university.university_points += college.college_points
        print(f"College '{college.name}' earned {college.college_points} points this semester.")

    print(f"\nSemester {university.year} completed.")
    print(f"University points: {university.university_points}")
    print(f"University budget: ${university.budget:,}\n")

def main_menu():
    print("\n--- MAIN MENU ---")
    print("1. Pick a College to Establish")
    print("2. Create a Program for a College")
    print("3. View University Status")
    print("4. Hire Faculty for a Program")
    print("5. Run Semester")
    print("6. Exit")
    print("7. Save Game")
    print("8. Load Game")
    choice = input("Select an option (1–8): ").strip()
    return choice

def view_status(uni):
    print("\n--- CURRENT STATUS ---")
    print(f"University: {uni.name}, Budget: ${uni.budget:,}, Year: {uni.year}")
    print(f"University Points: {uni.university_points}, University Ranking: {uni.university_ranking}\n")

    if not uni.colleges:
        print("No colleges added yet.")
    else:
        for college in uni.colleges:
            print(f"\nCollege: {college.name}, Tuition: ${college.tuition_fee:,}")
            print(f"College Points: {college.college_points}, College Ranking: {college.college_ranking}")

            if hasattr(college, "programs") and college.programs:
                for program in college.programs:
                    print(f"  - Program: {program.name}, Quality: {program.quality}, "
                          f"Points: {program.program_points}, "
                          f"Students: {program.student_stats.total}/{program.capacity} ({program.size})")

                    f = program.faculty_stats
                    print(f"    Faculty: Total={f.total}, "
                          f"S={f.class_s}, A={f.class_a}, B={f.class_b}, "
                          f"C={f.class_c}, D={f.class_d}, "
                          f"Expenses=${f.total_expenses:,}")

                    s = program.student_stats
                    print(f"    Students: Total={s.total}, "
                          f"S={s.class_s}, A={s.class_a}, B={s.class_b}, "
                          f"C={s.class_c}, D={s.class_d}")
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

def admit_students_roll(program, university):
    remaining_capacity = program.capacity - program.student_stats.total
    if remaining_capacity <= 0:
        print(f"{program.name} is already full!")
        return

    base_demand = random.randint(int(0.5 * program.capacity), int(1.5 * program.capacity))

    admitted = min(int(base_demand * (0.5 + program.quality / 10)), remaining_capacity)
    admitted = max(10, admitted)

    program.student_stats.total += admitted

    s_pct = min(0.05 + program.quality / 100, 0.1)
    a_pct = 0.2 + program.quality / 50
    b_pct = 0.25
    c_pct = 0.2

    s_count = int(admitted * s_pct)
    a_count = int(admitted * a_pct)
    b_count = int(admitted * b_pct)
    c_count = int(admitted * c_pct)
    d_count = admitted - (s_count + a_count + b_count + c_count)

    program.student_stats.class_s += s_count
    program.student_stats.class_a += a_count
    program.student_stats.class_b += b_count
    program.student_stats.class_c += c_count
    program.student_stats.class_d += d_count

    college_tuition = None
    for college in university.colleges:
        if program in college.programs:
            college_tuition = college.tuition_fee
            break

    if college_tuition is None:
        college_tuition = 10000
    university.budget += admitted * college_tuition

    print(f"{admitted} students admitted to {program.name} ({program.size})")

def save_game(university, filename="savegame.json"):
    data = {
        "name": university.name,
        "year_established": university.year_established,
        "year": university.year,
        "budget": university.budget,
        "university_points": university.university_points,
        "university_ranking": university.university_ranking,
        "colleges": []
    }

    for college in university.colleges:
        college_data = {
            "id": college.id,
            "name": college.name,
            "year_established": college.year_established,
            "tuition_fee": college.tuition_fee,
            "base_expenses": college.base_expenses,
            "college_points": college.college_points,
            "college_ranking": college.college_ranking,
            "programs": []
        }

        for program in college.programs:
            program_data = {
                "id": program.id,
                "name": program.name,
                "year_established": program.year_established,
                "capacity": program.capacity,
                "size": program.size,
                "quality": program.quality,
                "program_points": program.program_points,
                "program_ranking": program.program_ranking,
                "student_stats": vars(program.student_stats),
                "faculty_stats": vars(program.faculty_stats)
            }
            college_data["programs"].append(program_data)

        data["colleges"].append(college_data)

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Game saved to '{filename}'!")

def load_game(filename="savegame.json"):
    try:
        with open(filename, "r") as f:
            data = json.load(f)

        uni = University(data["name"], data["year_established"], data["budget"])
        uni.year = data.get("year", 1)
        uni.university_points = data.get("university_points", 0)
        uni.university_ranking = data.get("university_ranking", 0)

        for college_data in data.get("colleges", []):
            college = College(
                college_data["id"],
                college_data["name"],
                college_data["year_established"],
                college_data["tuition_fee"],
                college_data["base_expenses"]
            )
            college.college_points = college_data.get("college_points", 0)
            college.college_ranking = college_data.get("college_ranking", 0)

            for program_data in college_data.get("programs", []):
                program = Program(
                    program_data["id"],
                    program_data["name"],
                    program_data["year_established"],
                    program_data["capacity"]
                )
                program.size = program_data["size"]
                program.quality = program_data["quality"]
                program.program_points = program_data["program_points"]
                program.program_ranking = program_data.get("program_ranking", 0)

                s_stats = StudentStats()
                f_stats = FacultyStats()

                for key, value in program_data["student_stats"].items():
                    setattr(s_stats, key, value)

                for key, value in program_data["faculty_stats"].items():
                    setattr(f_stats, key, value)

                program.student_stats = s_stats
                program.faculty_stats = f_stats

                college.programs.append(program)

            uni.colleges.append(college)

        print(f"Game loaded from '{filename}'!")
        return uni

    except FileNotFoundError:
        print(f"No save file found at '{filename}'. Starting a new game.")
        return None

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

        # Run Semester
        elif choice == "5":
            if not uni.colleges:
                print("You must have a college first.")
                continue

            run_semester(uni)

        # Exit
        elif choice == "6":
            print("Exiting game. Goodbye!")
            break

        elif choice == "7":
            save_game(uni)

        elif choice == "8":
            loaded_uni = load_game()
            if loaded_uni:
                uni = loaded_uni
        else:
            print("Invalid menu option. Please choose 1–8.")

if __name__ == "__main__":
    main()