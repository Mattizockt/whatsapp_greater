import sqlite3
from datetime import datetime
from time import sleep
import pyautogui


def main():

    # get necessities to start bot
    information = get_info_to_type()

    # can anything be typed?
    if information is None:
        return print("Nothing to type today.")

    # open whatsapp and initialize
    searchbar = open_whatsapp()


    for element in information:

        date, name, event, text = element

        # prepare search field
        pyautogui.click(x=searchbar[0], y=searchbar[1])
        pyautogui.hotkey("ctrl", "a")
        pyautogui.press("backspace")
        pyautogui.write(name)
        sleep(2)
        pyautogui.click(x=146, y=241)
        sleep(2)

        # todo weiter fehleroptimierung (schnelligkeit, übergang zwischen mehreren zielen)

        # if this person does exist
        message_bar = pyautogui.locateOnScreen("pictures\message_bar.jpg", confidence=0.9)
        if message_bar is None:
            raise ValueError("The name of the person does not exist")

        # start writing the text
        pyautogui.click(x=message_bar[0], y=message_bar[1])
        pyautogui.write(text.format(name))
        pyautogui.press("enter")

        pyautogui.FAILSAFE = False
        pyautogui.click(x=1919, y=0)
        pyautogui.FAILSAFE = True

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
        result.append((gen[0], gen[1], gen[2], fes[0][0]))

    return result


def open_whatsapp():
    
    pyautogui.press("win")
    sleep(0.5)
    pyautogui.write("whatsapp")
    pyautogui.press("enter")

    # wait till whatsapp is loaded
    while True:
        if pyautogui.locateOnScreen("pictures\whatsapp_start_pic.jpg", confidence=0.9):
            print("success")
            break
        else:
            print("failure")

    # enter in searchbar the name
    searchbar = pyautogui.center(pyautogui.locateOnScreen("pictures\searchbar_whatsapp.jpg", confidence=0.9))
    return searchbar
if __name__ == "__main__":
    main()

