# run_project.py
import subprocess

def main():
    print("Starting data analysis...")
    subprocess.run(["python", "data_analysis.py"], check=True)
    
    print("Creating visualizations...")
    subprocess.run(["python", "visualizations.py"], check=True)
    
    print("Project run completed!")

if __name__ == "__main__":
    main()

