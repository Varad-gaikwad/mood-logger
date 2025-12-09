import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector
import os

if not os.path.exists("C:\\Users\\Milgard\\Documents\\STUDY\\IP\\MoodMate\\moods.csv"):
    
     moods=pd.DataFrame(columns=["Date","Mood","Hours_studied"])
     moods.to_csv("C:\\Users\\Milgard\\Documents\\STUDY\\IP\\MoodMate\\moods.csv",index=False)

if not os.path.exists("C:\\Users\\Milgard\\Documents\\STUDY\\IP\\MoodMate\\tasks.csv"):
    tasks=pd.DataFrame(columns=["Task","Status","Date"])
    tasks.to_csv("C:\\Users\\Milgard\\Documents\\STUDY\\IP\\MoodMate\\tasks.csv",index=False)

db = mysql.connector.connect(
host="localhost",
user="root",          
password="varad",  
database="moodmate")
cursor = db.cursor()

def log_mood():
    date = input("Enter date (YYYY-MM-DD): ")
    mood = input("How are you feeling today? ")
    hours = int(input("How many hours did you study today? "))
    df = pd.read_csv("moods.csv")
    row = {"Date": date, "Mood": mood, "Hours_studied": hours}
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df.to_csv("moods.csv", index=False)
    query = "INSERT INTO moods (Date, Mood, Hours_studied) VALUES (%s, %s, %s)"
    cursor.execute(query, (date, mood, hours))
    db.commit()

    print("Mood logged successfully!")
    
def add_task():
    task = input("Enter task name: ")
    date = input("Enter date (YYYY-MM-DD): ")
    df = pd.read_csv("tasks.csv")
    row = {"Task": task, "Status": "Pending", "Date": date}
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df.to_csv("tasks.csv", index=False)
    query = "INSERT INTO tasks (Task, Status, Date) VALUES (%s, %s, %s)"
    cursor.execute(query, (task, "Pending", date))
    db.commit()

    print("Task added!")
    
def complete_task():
    task = input("Enter the task you completed: ")
    df = pd.read_csv("tasks.csv")

    if task in df["Task"].values:
        df.loc[df["Task"] == task, "Status"] = "Done"
        df.to_csv("tasks.csv", index=False)

        query = "UPDATE tasks SET Status='Done' WHERE Task=%s"
        cursor.execute(query, (task,))
        db.commit()

        print("Task marked as done!")
    else:
        print("Task not found!")

def analyze_mood():
    df = pd.read_csv("moods.csv")
    if df.empty:
        print("No data yet!")
        return

    unique_moods = df["Mood"].unique()
    avg_hours = {}

    for mood in unique_moods:
     mood_rows = df[df["Mood"] == mood]
     avg_hours[mood] = mood_rows["Hours_studied"].mean()

    avg = pd.Series(avg_hours)
    print("Average Study Hours per Mood:", avg)

    avg.plot(kind="bar", color="skyblue")
    plt.title("Average Study Hours per Mood")
    plt.xlabel("Mood")
    plt.ylabel("Hours Studied")
    plt.show()
    
def view_tasks():
    df = pd.read_csv("tasks.csv")
    print("Your Tasks:")
    print(df)
    print()
    
def mood_suggestion():
    mood = input("Enter your current mood: ")
    suggestions = {
        "Happy": "Perfect time to revise something new ",
        "Sad": "Take a small break",
        "Tired": "Short 15-min nap",
        "Motivated": "Push your limits today! ",
        "Angry": "Listen to some music!"}
    print(suggestions.get(mood))
    
def productivity_analysis():
    moods_df = pd.read_csv("moods.csv")
    tasks_df = pd.read_csv("tasks.csv")

    if moods_df.empty:
        print("No data yet!")
        return

    unique_dates = moods_df["Date"].unique()
    daily_productivity = {}

    for date in unique_dates:
        # Hours studied on this date
        hours = moods_df[moods_df["Date"] == date]["Hours_studied"].sum()
        # Number of tasks done on this date
        tasks_done = tasks_df[(tasks_df["Date"] == date) & (tasks_df["Status"] == "Done")].shape[0]
        daily_productivity[date] = {"Hours_Studied": hours, "Tasks_Done": tasks_done}

    prod_df = pd.DataFrame.from_dict(daily_productivity, orient="index")
    print("Daily Productivity Summary:")
    print(prod_df)

    prod_df.plot(kind="bar", color=["skyblue", "orange"])
    plt.title("Daily Hours Studied and Tasks Completed")
    plt.xlabel("Date")
    plt.ylabel("Hours / Tasks Done")
    plt.show()


while True:
    print("""
--- MoodLogger Menu ---
1. Log Mood & Study Hours
2. Add Task
3. Complete Task
4. View Tasks
5. Analyze Mood Patterns
6. Get Mood-Based Suggestion
7. Daily Productivity""")
    ch = input("Enter your choice (1-7): ")

    if ch == "1":
        log_mood()
    elif ch == "2":
        add_task()
    elif ch == "3":
        complete_task()
    elif ch == "4":
        view_tasks()
    elif ch == "5":
        analyze_mood()
    elif ch == "6":
        mood_suggestion()
    elif ch == "7":
        productivity_analysis()
    else:
        print("Invalid choice.")