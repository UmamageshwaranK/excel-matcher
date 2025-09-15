class AddTask:
    def __init__(self):
        # Load tasks from file at start
        try:
            with open("tasks.txt", "r") as file:
                self.tasks = [eval(line.strip()) for line in file]
        except FileNotFoundError:
            self.tasks = []

    def save_tasks(self):
        # Save all tasks to file
        with open("tasks.txt", "w") as file:
            for task in self.tasks:
                file.write(str(task) + "\n")

    def run(self):
        while True:
            print("\n---To-Do list menu---")
            print("1. Add task")
            print("2. View tasks")
            print("3. Remove task")
            print("4. Exit")

            choice = input("Enter: ")

            if choice == "1":
                user_input = input("Enter the task: ")
                self.tasks.append({"task": user_input, "status": False})
                self.save_tasks()
                print("Task added")

            elif choice == "2":
                if not self.tasks:
                    print("No tasks found")
                else:
                    print("\nYour tasks:")
                    for i, t in enumerate(self.tasks, start=1):
                        status = "done" if t["status"] else "pending"
                        print(f"{i}. {t['task']} - {status}")

            elif choice == "3":
                if not self.tasks:
                    print("No tasks to remove")
                else:
                    for i, t in enumerate(self.tasks, start=1):
                        status = "done" if t["status"] else "pending"
                        print(f"{i}. {t['task']} - {status}")
                    try:
                        get = int(input("Enter the number of task to remove: "))
                        if 1 <= get <= len(self.tasks):
                            removed = self.tasks.pop(get - 1)  # subtract 1 because list is 0-indexed
                            self.save_tasks()
                            print(f"Removed: {removed['task']}")
                        else:
                            print("Invalid number")
                    except ValueError:
                        print("Enter a valid number")

            elif choice == "4":
                print("Thanks for using To-Do list")
                break

            else:
                print("Invalid input")


todo = AddTask()
todo.run()
