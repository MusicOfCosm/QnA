# import sys
# sys.path.append(r"")
from QCM import main
import random
import logging

filename = "A test Q&A"
logging.basicConfig(filename=f"{filename}.log", level=logging.INFO)


question_list = []

question1 = ["What is 9 by the power of 2?", 
            ['18', '2', '81', '4.5'], 
            ['81'], 
            1]

question_list.append(question1)


question2 = ["What is 8 by the power of 2?", 
            ['16', '2', '64', '4', '8x8'], 
            ['64', '8x8'], 
            2]

question_list.append(question2)


random.shuffle(question_list)

if __name__ == "__main__":
    main(question_list)