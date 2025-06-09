from django.http import JsonResponse

# Dummy dictionary: roll number as key, name as value
student_data = {
    "1": "Ankit",
    "2": "Aadhesh",
    "3": "Charlie",
}

def get_student(request, roll_number):
    name = student_data.get(roll_number)
    if name:
        return JsonResponse({"roll": roll_number, "name": name})
    else:
        return JsonResponse({"error": "Student not found"}, status=404)
