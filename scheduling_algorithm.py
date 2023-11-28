from pulp import *

#кол-во классов, кол-во преподавателей, кол-во учебных дней, кол-во уроков в день
grade_num, teach_num, study_days_num, class_num_per_day = map(int, input().split()) 

#путь до файла с предпочтениями
teachers_file = "teachers.txt"
preferences_file = "prefrences.txt"
lessons_count_file = "lessons_count.txt"


# Считываем список преподавателей
with open(teachers_file, 'r') as file:
    teachers = [line.strip() for line in file]

# Считываем предпочтения преподавателей
preferences = []
with open(preferences_file, 'r') as file:
    for line in file:
        preference = line.strip().split(',')
        preferences.append((preference[0], int(preference[1]), int(preference[2]), int(preference[3])))

# Считываем количество уроков в неделю для каждого преподавателя
lessons_count = {}
with open(lessons_count_file, 'r') as file:
    for line in file:
        teacher, count = line.strip().split(',')
        lessons_count[teacher] = int(count)

# Создаем экземпляр задачи оптимизации
prob = LpProblem("School_Schedule_Problem", LpMaximize)

# Создаем переменные решений для каждого урока в расписании
schedule = LpVariable.dicts("schedule",
                            ((teacher, day, classroom, timeslot) for teacher in teachers
                             for day in range(1, study_days_num + 1)  # Дни недели 
                             for classroom in range(1, grade_num + 1)  # Классы 
                             for timeslot in range(1, 7 + 1)),  # Уроки 
                            cat='Binary')

# Добавляем целевую функцию
prob += lpSum(schedule[teacher, day, classroom, timeslot] for (teacher, day, classroom, timeslot) in schedule)

# Добавляем ограничения на количество уроков для каждого преподавателя
for teacher, total_lessons in lessons_count.items():
    prob += lpSum(schedule[teacher, day, classroom, timeslot] for (teacher, day, classroom, timeslot) in schedule) == total_lessons

# Решаем задачу оптимизации
prob.solve()

# Выводим полученное расписание
for v in prob.variables():
    if v.varValue > 0:
        print(v.name, "=", v.varValue)





