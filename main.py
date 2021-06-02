import sqlite3
from datetime import datetime


def main():

    # get necessities to start bot
    information = get_info_to_type()

    # can anything be typed?
    if information is None:
        return print("Nothing to type today.")
    else:
        date, name, type, text = information





def get_info_to_type():

    conn = sqlite3.connect("whatsapp.db")
    c = conn.cursor()

    date = datetime.today().strftime("%d/%m")
    date = "16/01"

    # get name of person and event name
    database_results_general = c.execute("select * from general where dates = ?", (date,)).fetchall()
    conn.commit()

    if not database_results_general:
        return None
    [(_, name, event)] = database_results_general

    # get message
    database_results_festivity = c.execute("select * from festivity where type = ?", (event,)).fetchall()
    conn.commit()

    if not database_results_festivity:
        raise ValueError("There is no message text for this query")
    [(_, message)] = database_results_festivity
    return date, name, event, message

if __name__ == "__main__":
    main()

