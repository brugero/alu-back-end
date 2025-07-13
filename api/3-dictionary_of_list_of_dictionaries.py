#!/usr/bin/python3
"""
Exports TODO list progress of all employees to JSON format.
"""
import json
import requests
import sys


def export_all_to_json():
    """
    Fetches TODO list progress for all employees and exports it to a single JSON file.
    """
    base_url = "https://jsonplaceholder.typicode.com"

    # Fetch all users
    users_response = requests.get(f"{base_url}/users")
    users_data = users_response.json()

    all_employees_tasks = {}

    for user in users_data:
        user_id = user.get("id")
        username = user.get("username")

        # Fetch TODO list for the current user
        todos_response = requests.get(f"{base_url}/todos",
                                      params={"userId": user_id})
        todos_data = todos_response.json()

        tasks_list = []
        for task in todos_data:
            tasks_list.append({
                "username": username,
                "task": task.get("title"),
                "completed": task.get("completed")
            })
        all_employees_tasks[str(user_id)] = tasks_list

    # Write to JSON file
    json_filename = "todo_all_employees.json"
    with open(json_filename, mode='w', encoding='utf-8') as file:
        json.dump(all_employees_tasks, file, indent=4)

    print(f"Data for all employees exported to {json_filename}")


if __name__ == "__main__":
    try:
        export_all_to_json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        sys.exit(1)