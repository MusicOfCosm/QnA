import random
import time
import logging
from datetime import datetime
import os
from PIL import Image            #Those three modules
import matplotlib.pyplot as plt  #allow the manipulation
import matplotlib.image as mpimg #of images

class Question:
    def __init__(self, question, choices, answers, points, image=None):
        
        for i in answers:
            if i not in choices:
                raise UnboundLocalError('One or multiple answers are not in the list of choices!')

        self.question = question
        self.answers = answers
        self.points = points
        self.total_points = 0
        self.image = image

        random.shuffle(choices) #The elements in choices are now shuffled 
        keys = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        self.choices = dict(zip(keys, choices)) #creates a dict with 'keys' as keys and 'choices' as values
        
        if ',' in str(self.answers):                    #If there's multiple answers, a correct answer gives you the worth 
            self.point_value = points/len(self.answers) #of the question, divided by the number of correct answers there are
        else: self.point_value = points                 #Otherwise, the correct answer just gives you the amount of points the question is worth


    def testing(self):
        print(f'This question is worth {self.points} point(s).\n{self.question}', end='\n\n')

        for i, j in self.choices.items(): #dict.items() method returns a view object that displays a list of a given dictionary's (key, value) tuple pair.
            print(f'{i}: {j}')
        print() #just an empty line in the console

        if isinstance(self.image, str) and self.image != '':
            img = mpimg.imread(self.image)
            plt.imshow(img)
            ax = plt.gca()
            ax.axes.xaxis.set_visible(False)
            ax.axes.yaxis.set_visible(False)
            plt.show(block=False)

        answer_list = []
        have_answered = False
        while not have_answered:
            try:
                self.answer = self.choices[str(input('Your answer: ').upper())]

                answer_list.append(self.answer)

                if len(answer_list) != len(set(answer_list)): #A set cannot have duplicates
                    print(f'The answer - {self.answer} - has been removed.')
                    answer_list.remove(self.answer) #If the same answer is there twice,
                    answer_list.remove(self.answer) #they both get deleted 
                    have_answered = False

                Done = False
                while not Done:
                    print(f'Your current answers : {answer_list}')
                    done = str(input('Are you done answering this question? (y/n) '))
                    print() #empty line again
                    if done.lower() == 'n' or done.lower() == 'no':
                        Done = True

                    elif done.lower() == 'y' or done.lower() == 'yes':
                        have_answered = True
                        Done = True

                    else:
                        print('Not a valid response!', end='\n\n')
                        Done = False
                    
            except Exception: 
                print('You have to input one of the letters on the left.')
                have_answered = False #This reset the have_answered while loop, and allows to answer again

        if isinstance(self.image, str) and self.image != '':
            plt.close('all')

        n = len(answer_list) - len(self.answers)
        if n > 0:
            print(f'You have {n} incorrect response(s)!') #If there's an incorrect answer, nothing is added to self.total_points (it's = 0)

        elif not set(answer_list).issubset(self.answers): # x.issubset(y) returns True if all elements in set x are in set y
            n = 0
            m = 0
            for i in answer_list:
                if i in self.answers:
                    n += 1
                
                else:
                    m += 1
            
            if n == 0:
                print(f'You have {m} incorrect answer(s)!')

            else:
                print(f'You have {n} correct answer(s) and {m} incorrect one(s)!')

        else:
            n = 0
            m = len(self.answers)
            for i in answer_list:
                if i in self.answers:
                    self.total_points += self.point_value
                    n += 1
            print(f'You have {n} correct answer(s) out of {m}!')

        print(f'Points gained for this question: {self.total_points}')
        time.sleep(1.5)
        print(end='\n\n')

        return self.points, self.total_points


def main(question_list):
    print('You can only select one answer at a time.\nIf you wish to remove an answer you deem incorrect, simply select it again. \nAnswering incorrectly to a question will yield you 0 points. \nLetter casing does not matter.', end='\n\n\n')

    score = 0
    max_score = 0
    for i in question_list:
        question_worth, points_gained = Question(*i).testing()
        score += points_gained
        max_score += question_worth
    
    total_score = round(score/max_score*20, 2) #Mean of all questions out of 20, with 2 decimal places
    print(f'You got a total score of {total_score}/20!')
    if logging: logging.info(f'\n On {datetime.now().strftime("%B %d, %Y at %H:%M:%S")}, you got a score of {total_score}/20\n')

    correction = input('Would you like to see the correction? (if so, type y or yes, else press enter) ')
    if correction.lower() == 'y' or correction.lower() == 'yes':
        for i in range(len(question_list)):
            print(f'\nQuestion {i+1}: {question_list[i][0]}\n{question_list[i][2]}')
    
    print() #empty line
    os.system('pause') #This will pause the program (here it's at the end) until you press any key