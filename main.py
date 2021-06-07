import sqlite3
from datetime import datetime
from time import sleep
import pyautogui


def main():
    # get necessities to start bot
    information = get_database_information()

    # can anything be typed?
    if information is None:
        return print("Nothing to type today.")

    # open whatsapp and initialize
    searchbar = open_whatsapp()

    # writes text into whatsap
    write_in_whatsapp(information, searchbar)


def get_database_information():
    conn = sqlite3.connect("whatsapp.db")
    c = conn.cursor()

    date = datetime.today().strftime("%d/%m")

    # get name of person and event name
    database_results_general = c.execute("select * from general where dates = ?", (date,)).fetchall()
    conn.commit()

    if not database_results_general:
        return None

    # what to do if one event is meant for everybody (with "all" as name)
    all_statements = []
    for result in database_results_general:
        all_statements.append(make_holiday_for_all(result, c))  # [(),(),()]
    database_results_general = [x for x in database_results_general if x[1] != "all"]

    # modify all statements and append contents to database general_results
    all_statements = [x for x in all_statements if x is not None]
    [database_results_general.extend(x) for x in all_statements]

    # get message that needs to be typed
    festivity_text = []
    for general_result in database_results_general:
        festivity_text.append(c.execute("""select content from festivity where type = ? order by random() limit 1""",
                                        (general_result[2],)).fetchall())
        conn.commit()

    if not festivity_text:
        raise ValueError("There is no message text for this query")

    # merge message and person together
    result = []
    for gen, fes in zip(database_results_general, festivity_text):
        result.append((gen[0], gen[1], gen[2], fes[0][0]))

    return result


# returns array of new statements
def make_holiday_for_all(result, c):
    all_names = []
    if result[1] == "all":
        all_names.append(c.execute("select persons from general where persons != 'all'").fetchall())

        final_product = []
        for name in all_names[0]:
            final_product.append((result[0], name[0], result[2]))

        return final_product  # [(), (), ()]


# opens whatsapp
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


# writes the text messages into whatsapp
def write_in_whatsapp(information, searchbar):
    for element in information:

        date, name, event, text = element

        # prepare search field
        pyautogui.click(x=searchbar[0], y=searchbar[1])
        pyautogui.hotkey("ctrl", "a")
        pyautogui.press("backspace")
        pyautogui.write(name)

        # if there is fitting chat, groupchat
        while True:
            if pyautogui.locateOnScreen("pictures\chats_logo.jpg", confidence=0.8) or pyautogui.locateOnScreen(
                    "pictures\groups_logo.jpg", confidence=0.8):
                break
            elif pyautogui.locateOnScreen("pictures\\no_group_chats_found.jpg", confidence=0.8):
                print("this chat does not exist")
                return 0
        pyautogui.click(x=146, y=241)

        # wait until entering the message bar is possible
        message_bar = None
        while True:
            message_bar = pyautogui.locateOnScreen("pictures\message_bar.jpg", confidence=0.9)
            if message_bar:
                break

        # start writing the text
        pyautogui.click(x=message_bar[0], y=message_bar[1])
        pyautogui.write(text.format(name))
        pyautogui.press("enter")
        pyautogui.press("enter")

    pyautogui.FAILSAFE = False
    pyautogui.click(x=1919, y=0)
    pyautogui.FAILSAFE = True


if __name__ == "__main__":
    main()
