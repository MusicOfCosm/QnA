#!/usr/bin/env python3
# import sys
# sys.path.append(r"")
from QCM_GUI import main
import random
import logging
import os

filename = __file__
def remove_end(filename):
    stop = filename.rfind('.')
    while len(filename) != stop:
        filename = filename[:-1]
    return filename
filename = remove_end(filename)

# logging.basicConfig(filename=f"{filename}.log", level=logging.INFO) #uncomment to have your results logged
title = os.path.basename(__file__)
title = remove_end(title)


test_type = 'Mixed' #QCM, QCU, or Mixed?

question_list = []

question1 = ["",     #Question
            [""],    #Choices, if you put only one choice with 'write in (maths/formulae)' as a string, you will have an entry/text field to fill. If 'write in', you can put True to have letter casing matter in the third choice
            [""],    #Answer(s)   Replace the list by a dictionary to get a match question (items must be included in the list of choices)
            1, None, #Worth in points and image(s) - if multiple, use list or tuple
            None,    #Explanation for the answer(s): image(s) here (non compulsory)
            "",      #Explanation text here (non compulsory)
            ""]      #Do you have to select the choices in a particular order? "Numbers", "Letters". Any other non-empty string will make it work without. Put True if answers is a dict and you want it shuffled

question_list.append(question1)


question2 = ["",
            [""],
            [""],
            1, None,
            None,
            "",
            ""]

question_list.append(question2)


question3 = ["",
            [""],
            [""],
            1, None,
            None,
            "",
            ""]

question_list.append(question3)


question4 = ["",
            [""],
            [""],
            1, None,
            None,
            "",
            ""]

question_list.append(question4)


question5 = ["",
            [""],
            [""],
            1, None,
            None,
            "",
            ""]

question_list.append(question5)


question6 = ["",
            [""],
            [""],
            1, None,
            None,
            "",
            ""]
            
question_list.append(question6)


question7 = ["",
            [""],
            [""],
            1, None,
            None,
            "",
            ""]
            
question_list.append(question7)


question8 = ["",
            [""],
            [""],
            1, None,
            None,
            "",
            ""]
            
question_list.append(question8)


question9 = ["",
            [""],
            [""],
            1, None,
            None,
            "",
            ""]
            
question_list.append(question9)


question10 = ["",
             [""],
             [""],
             1, None,
             None,
             "",
             ""]
            
question_list.append(question10)


question11 = ["",
             [""],
             [""],
             1, None,
             None,
             "",
             ""]
            
question_list.append(question11)


question12 = ["",
             [""],
             [""],
             1, None,
             None,
             "",
             ""]
            
question_list.append(question12)


question13 = ["",
             [""],
             [""],
             1, None,
             None,
             "",
             ""]
            
question_list.append(question13)


question14 = ["",
             [""],
             [""],
             1, None,
             None,
             "",
             ""]
            
question_list.append(question14)


question15 = ["",
             [""],
             [""],
             1, None,
             None,
             "",
             ""]
            
question_list.append(question15)


question16 = ["",
             [""],
             [""],
             1, None,
             None,
             "",
             ""]
            
question_list.append(question16)


question17 = ["",
             [""],
             [""],
             1, None,
             None,
             "",
             ""]
            
question_list.append(question17)


question18 = ["",
             [""],
             [""],
             1, None,
             None,
             "",
             ""]
            
question_list.append(question18)


question19 = ["",
             [""],
             [""],
             1, None,
             None,
             "",
             ""]
            
question_list.append(question19)


question20 = ["",
             [""],
             [""],
             1, None,
             None,
             "",
             ""]
            
question_list.append(question20)

#Randomize only the order of the choices
for i in range(len(question_list)):
    if 'write in' not in question_list[i][1][0]:
        random.shuffle(question_list[i][1])

        if test_type == 'QCU' and len(question_list[i][2]) > 1: #Checks if there's only one answers with QCUs
            raise Exception(f'Multiple answers in question {i+1}\n(You have set this as a one answer Q&A)')

        for answer in question_list[i][2]:
            if answer not in question_list[i][1] and not isinstance(question_list[i][2], dict):
                print(f'The error is at question {i+1}')

    if isinstance(question_list[i][2], dict):
        dictio = list(question_list[i][2].items())
        random.shuffle(dictio)
        question_list[i][2] = dict(dictio)

#randomize the order of the questions
random.shuffle(question_list)


if __name__ == "__main__":
    main(test_type, question_list, title)