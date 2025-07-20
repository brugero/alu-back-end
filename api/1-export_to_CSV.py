#!/usr/bin/python3
"""
This script fetches an employee's TODO list data from a REST API
and exports it to a CSV file.
The CSV file is named after the employee's ID (e.g., USER_ID.csv)
and contains records in the format:
"USER_ID","USERNAME","TASK_COMPLETED_STATUS","TASK_TITLE".
"""

import csv
import requests
import sys


def export_employee_todo_to_csv(employee_id):
    """
    Fetches an employee's TODO list and exports it to a CSV file.

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

    username = user_data.get("username")

    # Fetch TODO list data
    todos_url = f"{base_url}/todos?userId={employee_id}"
    todos_response = requests.get(todos_url)
    todos_data = todos_response.json()

    # Define the CSV file name
    csv_file_name = f"{employee_id}.csv"

    # Write data to CSV
    with open(csv_file_name, mode='w', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        for task in todos_data:
            writer.writerow([
                employee_id,
                username,
                task.get("completed"),
                task.get("title")
            ])
    print(f"Data for employee ID {employee_id} exported to {csv_file_name}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 1-export_to_CSV.py <employee_id>")
        sys.exit(1)

    try:
        employee_id = int(sys.argv[1])
        export_employee_todo_to_csv(employee_id)
    except ValueError:
        print("Employee ID must be an integer.")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while connecting to the API: {e}")
        sys.exit(1)
    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")
        sys.exit(1)