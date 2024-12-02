import requests

def student_exists(student_code: str) -> bool:
    url = f'https://users-ms-ta.gadsw.dev/student/get-by-code/?student_code={student_code}'
    response = requests.get(url)
    print(f"student_exists: {response.status_code}")
    print(response.text)
    return response.status_code == 200

def teacher_exists(teacher_code: str) -> bool:
    url = f'https://users-ms-ta.gadsw.dev/user/get-by-code/?user_code={teacher_code}'
    response = requests.get(url)
    print(f"teacher_exists: {response.status_code}")
    return response.status_code == 200


