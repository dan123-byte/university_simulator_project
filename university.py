class University:
    def __init__(self, name, year_established, budget):
        self.name = name
        self.year_established = year_established
        self.year = 1
        self.budget = budget

        self.colleges = []

        self.university_points = 0
        self.university_ranking = 0

class College:
    def __init__(self, id, name, year_established, tuition_fee, base_expenses):
        self.id = id
        self.name = name
        self.year_established = year_established
        self.tuition_fee = tuition_fee
        self.base_expenses = base_expenses

        self.programs = []

        self.college_points = 0
        self.college_ranking = 0

class Program:
    def __init__(self,id, name, year_established):
        self.id = id
        self.name = name
        self.year_established = year_established
        self.quality = 1

        self.student_stats = StudentStats()
        self.faculty_stats = FacultyStats()

        self.program_points = 0
        self.program_ranking = 0

class StudentStats:
    def __init__(self):
        self.total = 0
        self.class_s = 0
        self.class_a = 0
        self.class_b = 0
        self.class_c = 0
        self.class_d = 0

class FacultyStats():
    def __init__(self):
        self.total = 0
        self.class_s = 0
        self.class_a = 0
        self.class_b = 0
        self.class_c = 0
        self.class_d = 0

        self.class_s_expense = 0
        self.class_a_expense = 0
        self.class_b_expense = 0
        self.class_c_expense = 0
        self.class_d_expense = 0

    @property
    def total_expenses(self):
        return (
            self.class_s * self.class_s_expense +
            self.class_a * self.class_a_expense +
            self.class_b * self.class_b_expense +
            self.class_c * self.class_c_expense +
            self.class_d * self.class_d_expense
        )