import argparse
import sys
from utilis.storage import Storage
from app.user import User
from app.project import Project
from app.task import Task
from rich.console import Console
from rich.table import Table

console = Console()

def main():
    parser = argparse.ArgumentParser(description="Multi-User Project Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    user_parser = subparsers.add_parser("add-user", help="Create a new user")
    user_parser.add_argument("--name", required=True)
    user_parser.add_argument("--email", required=True)

    project_parser = subparsers.add_parser("add-project", help="Add project to a user")
    project_parser.add_argument("--user", required=True, help="Name of the user")
    project_parser.add_argument("--title", required=True)
    project_parser.add_argument("--desc", default="Project description")
    project_parser.add_argument("--date", default="2026-12-31")

    task_parser = subparsers.add_parser("add-task", help="Add task to a project")
    task_parser.add_argument("--user", required=True)
    task_parser.add_argument("--project", required=True)
    task_parser.add_argument("--title", required=True)

    complete_parser = subparsers.add_parser("complete-task", help="Mark a task as done")
    complete_parser.add_argument("--user", required=True)
    complete_parser.add_argument("--project", required=True)
    complete_parser.add_argument("--task", required=True)

    subparsers.add_parser("list", help="List all users and their projects")

    args = parser.parse_args()

    users = Storage.load_data()

    if args.command == "add-user":
        if any(u.name == args.name for u in users):
            console.print(f"[red]Error: User {args.name} already exists.[/red]")
        else:
            users.append(User(args.name, args.email))
            Storage.save_data(users)
            console.print(f"[green]Successfully added user: {args.name}[/green]")

    elif args.command == "add-project":
        user = next((u for u in users if u.name == args.user), None)
        if not user:
            console.print(f"[red]User '{args.user}' not found.[/red]")
        else:
            user.projects.append(Project(args.title, args.desc, args.date))
            Storage.save_data(users)
            console.print(f"[blue]Project '{args.title}' assigned to {args.user}.[/blue]")

    elif args.command == "add-task":
        user = next((u for u in users if u.name == args.user), None)
        project = next((p for p in user.projects if p.title == args.project), None) if user else None
        
        if project:
            project.tasks.append(Task(args.title, assigned_to=user.name))
            Storage.save_data(users)
            console.print(f"[yellow]Task '{args.title}' added to project '{args.project}'.[/yellow]")
        else:
            console.print("[red]User or Project not found.[/red]")

    elif args.command == "complete-task":
        target_user = next((u for u in users if u.name == args.user), None)
        
        if target_user:
            target_project = next((p for p in target_user.projects if p.title == args.project), None)
            
            if target_project:
                target_task = next((t for t in target_project.tasks if t.title == args.task), None)
                
                if target_task:
                    target_task.mark_done() 
                    Storage.save_data(users)
                    console.print(f"[bold green]Success![/bold green] Task '{args.task}' marked as done.")
                else:
                    console.print(f"[red]Task '{args.task}' not found in project '{args.project}'.[/red]")
            else:
                console.print(f"[red]Project '{args.project}' not found for user '{args.user}'.[/red]")
        else:
            console.print(f"[red]User '{args.user}' not found.[/red]")

    elif args.command == "list":
        table = Table(title="Project Tracker Management System")
        table.add_column("User", style="magenta")
        table.add_column("Projects (Tasks)", style="cyan")
        
        for u in users:
            proj_str = "\n".join([f"- {p.title} ({len(p.tasks)} tasks)" for p in u.projects])
            table.add_row(u.name, proj_str or "No projects")
        console.print(table)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()