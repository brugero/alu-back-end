#!/usr/bin/python3
"""
This script fetches an employee's TODO list progress from a REST API
and displays it on the standard output.
It takes an employee ID as a command-line argument.
"""

import requests
import sys


def get_employee_todo_progress(employee_id):
    """
    Fetches and displays an employee's TODO list progress.

    Args:
        employee_id (int): The ID of the employee.
    """
    # Base URL for the API
    base_url = "https://jsonplaceholder.typicode.com"

    # Fetch user data
    user_url = f"{base_url}/users/{employee_id}"
    user_response = requests.get(user_url)
    user_data = user_response.json()

    if not user_data:
        print(f"Employee with ID {employee_id} not found.")
        return

    employee_name = user_data.get("name")

    # Fetch TODO list data
    todos_url = f"{base_url}/todos?userId={employee_id}"
    todos_response = requests.get(todos_url)
    todos_data = todos_response.json()

    total_tasks = len(todos_data)
    completed_tasks = [task for task in todos_data if task.get("completed")]
    number_of_done_tasks = len(completed_tasks)

    # Display progress
    print(f"Employee {employee_name} is done with tasks("
          f"{number_of_done_tasks}/{total_tasks}):")

    # Display completed task titles
    for task in completed_tasks:
        print(f"\t {task.get('title')}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 0-gather_data_from_an_API.py <employee_id>")
        sys.exit(1)

    try:
        employee_id = int(sys.argv[1])
        get_employee_todo_progress(employee_id)
    except ValueError:
        print("Employee ID must be an integer.")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while connecting to the API: {e}")
        sys.exit(1)