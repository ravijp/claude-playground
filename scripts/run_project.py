import sys
import subprocess

def run_project(project_name):
    """Run a specific project"""
    project_path = f"projects/{project_name}"
    
    if not os.path.exists(project_path):
        print(f"❌ Project '{project_name}' not found")
        return
    
    print(f"\n🚀 Running {project_name}...\n")
    
    main_file = os.path.join(project_path, "main.py")
    if not os.path.exists(main_file):
        main_file = os.path.join(project_path, "agent.py")
    
    subprocess.run([sys.executable, main_file])

if __name__ == "__main__":
    import os
    
    if len(sys.argv) < 2:
        print("Usage: python run_project.py <project-name>")
        print("\nAvailable projects:")
        for item in os.listdir("projects"):
            if os.path.isdir(os.path.join("projects", item)):
                print(f"  - {item}")
    else:
        run_project(sys.argv[1])
