class Student:
    instance_list = []
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}
        self.__class__.instance_list.append(self)

    def add_courses(self, course_name):
        self.finished_courses.append(course_name)

    def rate_lecture(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and \
                course in lecturer.courses_attached and course in self.courses_in_progress:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        res = f'''
        Имя: {self.name}
        Фамилия: {self.surname}
        Средняя оценка за домашние задания: {average_grade(self)}
        Курсы в процессе изучения: {', '.join(self.courses_in_progress)}
        Завершенные курсы:
        {', '.join(self.finished_courses) if self.finished_courses else 'no completed courses'}
        '''
        return res

    def __lt__(self, other):
        if not isinstance(other, Student) and not self.grades and not other.grades:
            return 'nothing to compare'
        return average_grade(self) < average_grade(other)

    def __le__(self, other):
        if not isinstance(other, Student) and not self.grades and not other.grades:
            return 'nothing to compare'
        return average_grade(self) <= average_grade(other)

    def __eq__(self, other):
        if not isinstance(other, Student) and not self.grades and not other.grades:
            return 'nothing to compare'
        return average_grade(self) == average_grade(other)


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    instance_list = []
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}
        self.__class__.instance_list.append(self)

    def __str__(self):
        res = f'''
        Имя: {self.name}
        Фамилия: {self.surname}
        Средняя оценка за лекции: {average_grade(self)}
        '''
        return res

    def __lt__(self, other):
        if not isinstance(other, Lecturer) and not self.grades and not other.grades:
            return 'nothing to compare'
        return average_grade(self) < average_grade(other)

    def __le__(self, other):
        if not isinstance(other, Lecturer) and not self.grades and not other.grades:
            return 'nothing to compare'
        return average_grade(self) <= average_grade(other)

    def __eq__(self, other):
        if not isinstance(other, Lecturer) and not self.grades and not other.grades:
            return 'nothing to compare'
        return average_grade(self) == average_grade(other)


class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and \
                course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        res = f'''
        Имя: {self.name}
        Фамилия: {self.surname}
        '''
        return res


def average_grade(self):
    if self.grades:
        return sum([sum(i) for i in self.grades.values()]) / sum([len(i) for i in self.grades.values()])
    else:
        return 'grades not found'

def average_grade_students(students_list, course):
    result = 0
    count = 0
    for s in students_list:
        if course in s.courses_in_progress and course in s.grades:
            result += sum(s.grades[course]) / len(s.grades[course])
            count += 1
    if count:
        return f'Средняя оценка студентов за курс: {course} - {result / count}'
    else:
        return 'nothing to compare'

def average_grade_lecturers(lecturers_list, course):
    result = 0
    count = 0
    for s in lecturers_list:
        if course in s.courses_attached and course in s.grades:
            result += sum(s.grades[course]) / len(s.grades[course])
            count += 1
    if count:
        return f'Средняя оценка лекторов за курс: {course} - {result / count}'
    else:
        return 'nothing to compare'


# объявление списков, экземпляров и присвоение им данных
student1 = Student('Сын', 'Дворов', 'муж')  # студент1
student1.courses_in_progress += ['Python']
student1.courses_in_progress += ['Java']
student1.finished_courses += ['Git']
student1.finished_courses += ['Основы языка программирования Python']

student2 = Student('Света', 'Горелова', 'жен')  # студент2
student2.courses_in_progress += ['Python']
student2.courses_in_progress += ['Java']

reviewer1 = Reviewer('Камаз', 'Арбузов')  # ревьюер1
reviewer1.courses_attached += ['Python']
reviewer1.courses_attached += ['Java']

reviewer2 = Reviewer('Кот', 'Царапов')  # ревьюер2
reviewer2.courses_attached += ['Python']
reviewer2.courses_attached += ['Java']

lector1 = Lecturer('Ремонт', 'Фасадов')  # лектор1
lector1.courses_attached += ['Python']
lector1.courses_attached += ['Java']

lector2 = Lecturer('Десант', 'Парашютов')  # лектор2
lector2.courses_attached += ['Python']
lector2.courses_attached += ['Java']

# этап выставления оценок
reviewer1.rate_hw(student1, 'Python', 9)
reviewer1.rate_hw(student1, 'Python', 8)
reviewer2.rate_hw(student1, 'Python', 9)
reviewer2.rate_hw(student1, 'Python', 5)

reviewer1.rate_hw(student2, 'Python', 7)
reviewer1.rate_hw(student2, 'Python', 4)
reviewer2.rate_hw(student2, 'Python', 8)
reviewer2.rate_hw(student2, 'Python', 5)

reviewer1.rate_hw(student1, 'Java', 8)
reviewer1.rate_hw(student1, 'Java', 7)
reviewer2.rate_hw(student1, 'Java', 9)
reviewer2.rate_hw(student1, 'Java', 8)

reviewer1.rate_hw(student2, 'Java', 7)
reviewer1.rate_hw(student2, 'Java', 4)
reviewer2.rate_hw(student2, 'Java', 9)
reviewer2.rate_hw(student2, 'Java', 9)

student1.rate_lecture(lector1, 'Python', 9)
student1.rate_lecture(lector1, 'Python', 9)
student2.rate_lecture(lector1, 'Python', 7)
student2.rate_lecture(lector1, 'Python', 8)

student1.rate_lecture(lector1, 'Java', 9)
student1.rate_lecture(lector1, 'Java', 6)
student2.rate_lecture(lector1, 'Java', 7)
student2.rate_lecture(lector1, 'Java', 8)

# Дальнейший код для использования всех вариантов выдачи оценок
# комментим 8 строк кода ниже, чтобы увидеть отсутствие оценок у экземпляра результатом при выводе
# чтобы сравнения прошли корректно, нужно раскомментить оценки второго лектора
student1.rate_lecture(lector2, 'Python', 6)
student1.rate_lecture(lector2, 'Python', 7)
student2.rate_lecture(lector2, 'Python', 9)
student2.rate_lecture(lector2, 'Python', 8)

student1.rate_lecture(lector2, 'Java', 4)
student1.rate_lecture(lector2, 'Java', 9)
student2.rate_lecture(lector2, 'Java', 5)
student2.rate_lecture(lector2, 'Java', 9)

print(student1)
print(student2)
print(lector1)
print(lector2)

print(average_grade_students(Student.instance_list, 'Python'))
print(average_grade_lecturers(Lecturer.instance_list, 'Java'))

print(student1 < student2)
print(student1 > student2)
print(student1 <= student2)
print(lector1 < lector2)
print(lector1 > lector2)
print(lector1 >= lector2)
print(student1 == student2)
print(lector1 != lector2)