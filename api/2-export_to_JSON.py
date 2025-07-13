#!/usr/bin/python3
"""
Exports employee TODO list progress to JSON format.
"""
import json
import requests
import sys


def export_to_json(employee_id):
    """
    Fetches employee TODO list progress and exports it to a JSON file.
    """
    base_url = "https://jsonplaceholder.typicode.com"

    # Fetch user details
    user_response = requests.get(f"{base_url}/users/{employee_id}")
    user_data = user_response.json()
    username = user_data.get("username")

    # Fetch TODO list for the user
    todos_response = requests.get(f"{base_url}/todos",
                                  params={"userId": employee_id})
    todos_data = todos_response.json()

    # Prepare data for JSON export
    tasks_list = []
    for task in todos_data:
        tasks_list.append({
            "task": task.get("title"),
            "completed": task.get("completed"),
            "username": username
        })

    json_output = {str(employee_id): tasks_list}

    # Write to JSON file
    json_filename = f"{employee_id}.json"
    with open(json_filename, mode='w', encoding='utf-8') as file:
        json.dump(json_output, file, indent=4)

    print(f"Data exported to {json_filename}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 2-export_to_JSON.py <employee_id>")
        sys.exit(1)
    try:
        employee_id = int(sys.argv[1])
        export_to_json(employee_id)
    except ValueError:
        print("Employee ID must be an integer.")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        sys.exit(1)