import pickle
import numpy as np
import pyautogui
import cv2
import train, move
import math, time
import asyncio

ANSWERS = ['R', 'G', 'B', 'L', 'D', 'H', 'J']


def get_model():
    model = None
    try:
        model = pickle.load(open('model.pickle', 'rb'))
    except FileNotFoundError:
        print('Model not found, creating a new one...')
        model = train.generate_model()

    return model


def get_orb_images():
    images = []

    image = screenshot()

    for row in range(0, 5):
        for column in range(0, 6):
            width = 76
            hight = 76
            x = (width * column) - column
            y = (hight * row) - row
            dx = x + width-1
            dy = y + hight-1

            orb_image = image[y:dy, x:dx]
            orb_image = cv2.cvtColor(orb_image, cv2.COLOR_BGR2GRAY)
            orb_image = np.array(orb_image)
            mnx, mny = orb_image.shape
            orb_image = orb_image.reshape((mnx*mny))
            images.append(orb_image)

    return images


def generate_board_string():
    board_string = ""
    for image in get_orb_images():
        board_string += ANSWERS[get_model().predict([image])[0]]
    return board_string

def screenshot():
    image = pyautogui.screenshot()
    image = np.array(image)
    x = 734
    y = 520
    h = 377
    w = 452
    image = image[:, :, ::-1].copy()
    image = image[y:y+h, x:x+w]
    return image

def calc_start_position(index):
    column = index % 6
    row = math.floor(index/6)
    print(f"col: {column}")
    print(f"row: {row}")
    return column, row

def add_arrowedLine(hight, image, red, width, x, x2, y, y2):
    overlay = image.copy()
    
    cv2.arrowedLine(overlay, 
                    (int(x + width/2), int(y + hight/2)),
                    (int(x2 + width/2), int(y2 + hight/2)),
                    (0, 0, red), 2
                    )
    alpha = 0.6  # Transparency factor.
    # Following line overlays transparent rectangle over the image
    image = cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)
    return image

def solve_window(board_string, index, moves):
    #debug_window()
    id = index
    
    while True:
        index = id
        frame_array = []
        image = screenshot()
        column, row = calc_start_position(index)
        width = 76
        hight = 76
        x = (width * column) - column
        y = (hight * row) - row
        dx = x + width-1
        dy = y + hight-1

        prediction = board_string[index]
        #print(prediction)
        image = cv2.putText(image, prediction, (int(x + width/2), int(y + hight/2)),
                            cv2.FONT_HERSHEY_PLAIN, 1.2, (0, 0, 0))
        image = cv2.putText(image, prediction, (int(x + width/2-1), int(y + hight/2-1)),
                            cv2.FONT_HERSHEY_PLAIN, 1.2, (row * 40, column * 40, 255))
        image = cv2.rectangle(image, (x, y), (dx, dy), (255, 255, 255), 1)
        red = 255
        count = 0
        for move_to in moves:
            count += 1
            shift = (count)%5
            index, c, r = move_to.calc_position(index)
            x2 = (width * c) - c + shift
            y2 = (hight * r) - r + shift
            image = add_arrowedLine(hight, image, red, width, x, x2, y, y2)
            frame_array.append(image)
            #cv2.imshow("Screenshot", image)
            #cv2.waitKey(100)

            #await asyncio.sleep(1)
            #time.sleep(0.5)
            x = x2
            y = y2
            pass
        fps = 0.5
        size = (452, 377)
        out = cv2.VideoWriter('solve.avi',cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
        for i in range(len(frame_array)):
            # writing to a image array
            out.write(frame_array[i])
        out.release()
        cv2.imwrite('output.jpg', image)
        break
    cv2.imshow("Screenshot", image)
    cv2.waitKey(100)
    cv2.imwrite('output.jpg', image)
    #time.sleep(1000)

def debug_window():
    image = screenshot()

    board_string = generate_board_string()
    for row in range(0, 5):
        for column in range(0, 6):
            width = 76
            hight = 76
            x = (width * column) - column
            y = (hight * row) - row
            dx = x + width-1
            dy = y + hight-1

            prediction = board_string[row * 6 + column]
            #print(prediction)
            image = cv2.putText(image, prediction, (int(x + width/2), int(y + hight/2)),
                                cv2.FONT_HERSHEY_PLAIN, 1.2, (0, 0, 0))
            image = cv2.putText(image, prediction, (int(x + width/2-1), int(y + hight/2-1)),
                                cv2.FONT_HERSHEY_PLAIN, 1.2, (row * 40, column * 40, 255))
            image = cv2.rectangle(image, (x, y), (dx, dy), (255, 255, 255), 1)


    cv2.imshow("Screenshot", image)
    cv2.waitKey(100)
    cv2.imwrite('output_0.jpg', image)


if __name__ == "__main__":
    while True:
        debug_window()
