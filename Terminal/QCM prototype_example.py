# import sys
# sys.path.append(r'') #Allows the program to know where to import the QCM module from 
from QCM import main
import random
import logging
import tkinter
from tkinter import filedialog

root = tkinter.Tk()
root.withdraw()

logging.basicConfig(filename='Base_log.log', level=logging.INFO)

img = filedialog.askopenfilename(filetypes=(('png.files', '*.png'),
                                            ('jpeg.files', '*.jpeg'),
                                            ('jpeg.files', '*.jpg'),
                                            ('tiff.files', '*.tiff'),
                                            ('gif.files', '*.gif'),
                                            ('bmp.files', '*.bmp')) )

question_list = []

question1 = ['What is 9 by the power of 2?', ['18', '2', '81', '4.5'], ['81'], 1, img]
question2 = ['What is 8 by the power of 2?', ['16', '2', '64', '4', '8x8'], ['64', '8x8'], 2]
question_list.append(question1)
question_list.append(question2)

random.shuffle(question_list)

if __name__ == '__main__':
    main(question_list)


'''
Want:
    The rules explained at the begginning                         - Done
    Have the means of the questions out of 20                     - Done
    Have all the answers and your scores at the end               - Done
    Have your total score stored in another file along with time  - Done
'''
