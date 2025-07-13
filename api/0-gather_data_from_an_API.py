#!/usr/bin/python3
"""
A Python script that, using a REST API, for a given employee ID,
returns information about his/her TODO list progress.

The script accepts an integer as a parameter, which is the employee ID.
It displays the employee TODO list progress in the exact format:
First line: Employee EMPLOYEE_NAME is done with tasks(NUMBER_OF_DONE_TASKS/TOTAL_NUMBER_OF_TASKS):
Second and N next lines display the title of completed tasks:    TASK_TITLE
"""

import requests
import sys


def get_employee_todo_progress(employee_id):
    """
    Fetches and displays the TODO list progress for a given employee ID.

    Args:
        employee_id (int): The ID of the employee.
    """
    # Base URL for the API
    base_url = "https://jsonplaceholder.typicode.com"

    # Fetch user information
    user_url = f"{base_url}/users/{employee_id}"
    user_response = requests.get(user_url)
    user_data = user_response.json()

    # Get employee name using .get() for safe access
    employee_name = user_data.get("name")

    # Fetch TODO list for the employee
    todos_url = f"{base_url}/todos?userId={employee_id}"
    todos_response = requests.get(todos_url)
    todos_data = todos_response.json()

    # Initialize counters and list for completed tasks
    total_tasks = 0
    done_tasks = 0
    completed_task_titles = []

    # Process TODO data
    for task in todos_data:
        total_tasks += 1
        # Check if task is completed using .get()
        if task.get("completed"):
            done_tasks += 1
            # Get task title using .get()
            completed_task_titles.append(task.get("title"))

    # Display the progress
    print(f"Employee {employee_name} is done with tasks({done_tasks}/{total_tasks}):")
    for title in completed_task_titles:
        print(f"\t {title}")


if __name__ == "__main__":
    try:
        # Get employee ID from console input
        employee_id_input = input("Enter the employee ID: ")
        employee_id = int(employee_id_input)
        get_employee_todo_progress(employee_id)
    except ValueError:
        print("Error: Employee ID must be an integer.")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)