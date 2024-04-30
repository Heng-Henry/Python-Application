import pyautogui

from time import sleep

pyautogui.FAILSAFE = True


def locate_and_get_coordinate(picture, x1, y1, x2, y2):
    loc = pyautogui.locateAllOnScreen(picture, confidence=0.95, region=(x1, y1, x2, y2))
    temp_list = []
    for box in loc:
        #temp_list.append([box.left, box.top, box.width, box.height])
        temp_list.append(box)

    return temp_list

pyautogui.hotkey('win', 'r')
sleep(0.5)
pyautogui.typewrite("https://www.google.com.tw/")
pyautogui.press('enter')
sleep(2)
pyautogui.moveTo(215, 492, 0.5)
pyautogui.click()
pyautogui.hotkey('ctrl', 'shift', 'n')
pyautogui.moveTo(462, 59, 0.5)
pyautogui.typewrite("https://solvable-sheep-game.streakingman.com/")
pyautogui.press('enter')
pyautogui.hotkey('fn', 'f11')

picture = (None, 'pic1.png', 'pic2.png', 'pic3.png', 'pic4.png', 'pic5.png', 'pic6.png', 'pic7.png', 'pic8.png')

sleep(4.5)

i = 1
fail_count = 0
while True:
    #print(picture[i])
    temp_list = locate_and_get_coordinate(picture[i], 400, 120, 1250, 750)
    temp_list2 = locate_and_get_coordinate(picture[i], 690, 810, 1211, 912)
    #print(len(temp_list))
    #print(len(temp_list2))
    sleep(0.2)
    total_num = len(temp_list) + len(temp_list2)
    #print(len(temp_list))
    if len(temp_list) < 3 and (len(temp_list) + len(temp_list2)) < 3:
        fail_count += 1
        if fail_count == 20:
            pyautogui.moveTo(1015, 963, 0.5)
            pyautogui.click()
            fail_count = 0
        if i == 8:
            i = 1
        else:
            i += 1
        sleep(0.1)
        continue
    elif total_num >= 2 and len(temp_list2) >= 1:
        count = len(temp_list2)
        for box in temp_list:
            if count >= 3:
                break
            pyautogui.moveTo(box.left + box.width / 2, box.top + box.height / 2, 0.5)
            pyautogui.click()

            count += 1
            sleep(0.1)
        if i == 8:
            i = 1
        else:
            i += 1
        continue

    count = 0
    for box in temp_list:
        if count == 3:
            break
        pyautogui.moveTo(box.left+box.width/2, box.top+box.height/2, 0.5)
        pyautogui.click()

        sleep(0.1)
        count += 1
    sleep(0.1)
    if i == 8:
        i = 1
    else:
        i += 1








