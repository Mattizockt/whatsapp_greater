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

    # get message
    festivity_text = []
    for general_result in database_results_general:
        festivity_text.append(c.execute("""select content from festivity where type = ? order by random() limit 1""", (general_result[2],)).fetchall())
        conn.commit()

    if not festivity_text:
        raise ValueError("There is no message text for this query")

    # merge message and person together
    result = []
    for gen, fes in zip(database_results_general, festivity_text):
        result.append((gen[0], gen[1], gen[2], fes))

    return result
if __name__ == "__main__":
    main()

