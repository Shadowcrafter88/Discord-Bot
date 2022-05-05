import sqlite3

def createDB():
    db = sqlite3.connect("config/databases/reminder.db")
    c = db.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS reminders (
                 id integer, 
                 time text,
                 message text
                 )""")
    db.commit()
    db.close()


def addReminder(id, time, message):
    db = sqlite3.connect("config/databases/reminder.db")
    c = db.cursor()
    try:
        c.execute(f"INSERT INTO reminders VALUES ({id}, \"{time}\", \"{message}\")")

        db.commit()
        db.close()
    except Exception as e:
        print(e)


def removeReminder(id, message):
    db = sqlite3.connect("config/databases/reminder.db")
    c = db.cursor()

    c.execute(f"DELETE FROM reminders WHERE id = {id} AND message LIKE \"{message}\"")

    db.commit()
    db.close()

def getReminders(id):
    db = sqlite3.connect("config/databases/reminder.db")
    c = db.cursor()

    c.execute(f"SELECT * FROM reminders WHERE id = {id}")
    selected = c.fetchall()

    db.commit()
    db.close()

    return selected

def getRemindersAmount(id):
    db = sqlite3.connect("config/databases/reminder.db")
    c = db.cursor()

    c.execute(f"SELECT * FROM reminders WHERE id = {id}")
    selected = c.fetchall()

    db.commit()
    db.close()

    return len(selected)

def remind():
    db = sqlite3.connect("config/databases/reminder.db")
    c = db.cursor()

    c.execute(f"SELECT * FROM reminders WHERE time <= datetime('now', 'localtime')")
    selected = c.fetchall()

    c.execute(f"DELETE FROM reminders WHERE time <= datetime('now', 'localtime')")

    db.commit()
    db.close()

    return selected


