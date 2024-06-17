import tkinter
from tkinter import filedialog
import os

root = tkinter.Tk()
root.withdraw()

filename = input('What is going to be the name of this Q&A file? (Do NOT put a file extension, or a special character!)\n')

try:
    f = open(f'{filename}.py', 'x', encoding='utf-8')

    f.write('import sys\n')
    f.write(r'sys.path.append(r"C:\Users\macky\OneDrive\Documents\Coding\Python\QCM")') #An r (raw) string considers \ as characters
    f.write('\nfrom QCM import main\n')
    f.write('import random\n')
    f.write('import logging\n\n')

    f.write(f'filename = \'{filename}\'\n')

    log_q = False
    while not log_q: #Does the user want to log their results?
        log = input('\nWould you like your results to be logged? (y/n) ')
        if log.lower() == 'y' or log.lower() == 'yes':
            f.write('logging.basicConfig(filename=f"{filename}.log", level=logging.INFO)\n\n\n')
            logging = True
            log_q = True
        
        elif log.lower() == 'n' or log.lower() == 'no':
            logging = False #This will affect main()
            log_q = True

        else:
            print('Not a valid response!', end='\n\n')
            log_q = False

    test = False
    while not test:
        type_q = input('\nWill the questions all have a single answer? ')
        if type_q.lower() == 'y' or type_q.lower() == 'yes':
            f.write('test_type = "QCU"\n\n')
            test = True
        
        elif type_q.lower() == 'n' or type_q.lower() == 'no':
            f.write('test_type = "QCM"\n\n')
            test = True

        else:
            print('Not a valid response!', end='\n\n')
            test = False

    f.write('question_list = []\n\n')

    def question():
        q = False
        while not q:
            a = input('What is the question?\n')

            s = False
            while not s:
                sure = input('\nConfirm question: (y/n) ')
                if sure.lower() == 'y' or sure.lower() == 'yes':
                    q = True
                    s = True
                    return a
                
                elif sure.lower() == 'n' or sure.lower() == 'no':
                    q = False
                    s = True

                else:
                    print('Not a valid response!', end='\n\n')
                    s = False


    def choices():
        q = False
        while not q:
            a = input('\nWhat are the choices for this questions? They must be written like this: "a", "b", "c" or this \'a\', \'b\', \'c\' (Don\'t forget to separate the choices with commas!)\n')

            s = False
            while not s:
                sure = input('Confirm choices: (y/n) ')
                if sure.lower() == 'y' or sure.lower() == 'yes':
                    q = True
                    s = True
                    return a
                
                elif sure.lower() == 'n' or sure.lower() == 'no':
                    q = False
                    s = True

                else:
                    print('Not a valid response!', end='\n\n')
                    s = False

    def answers():
        q = False
        while not q:
            a = input('\nWhat are the answers? Same deal as before, you must type your answers between quotes and separate them using commas. The answers must be included in the list of choices.\n')

            s = False
            while not s:
                sure = input('Confirm answers: (y/n) ')
                if sure.lower() == 'y' or sure.lower() == 'yes':
                    q = True
                    s = True
                    return a
                
                elif sure.lower() == 'n' or sure.lower() == 'no':
                    q = False
                    s = True

                else:
                    print('Not a valid response!', end='\n\n')
                    s = False

    def worth():
        q = False
        while not q:
            a = int(input('\nHow many points is the question worth? You must type a number. '))

            s = False
            while not s:
                sure = input('Confirm worth: (y/n) ')
                if sure.lower() == 'y' or sure.lower() == 'yes':
                    q = True
                    s = True
                    return a
                
                elif sure.lower() == 'n' or sure.lower() == 'no':
                    q = False
                    s = True

                else:
                    print('Not a valid response!', end='\n\n')
                    s = False

    for n in range(int(input('\n\nHow many questions do you plan on having? Your must type a number. '))):
        print(f'\n\nQuestion {n+1}:')
        f.write('question{} = ["{}", \n            [{}], \n            [{}], \n            {}'.format(n+1,
                                                                                                question(),
                                                                                                choices(),
                                                                                                answers(),
                                                                                                worth()) )
        
        img_q = False
        while not img_q: #Does the user want to integrate an image?
            imaging = input('\nWould you like the question to have an image? (y/n) ')
            if imaging.lower() == 'y' or imaging.lower() == 'yes':
                img = filedialog.askopenfilename(filetypes=(('png.files', '*.png'),
                                                            ('JPG.files', '*.JPG'),
                                                            ('jpeg.files', '*.jpeg'),
                                                            ('tif.files', '*.tif'),
                                                            ('gif.files', '*.gif'),
                                                            ('bmp.files', '*.bmp')) )
                f.write(f', \n            r"{img}"]\n\n')
                img_q = True
            
            elif imaging.lower() == 'n' or imaging.lower() == 'no':
                f.write(', None]\n\n')
                img_q = True

            else:
                print('Not a valid response!', end='\n\n')
                img_q = False
        
        f.write(f'question_list.append(question{n+1})\n\n\n')

    f.write('random.shuffle(question_list)\n\n')
    f.write('if __name__ == "__main__":\n')
    f.write('    main(question_list)')

    print('\n\nYou have finished making your Q&A! Hopefully, you didn\'t mess it up, and the new file that you made will run properly. But you never know!\nAsk me if you have any questions, or problems!\n')
    os.system("pause")

except Exception as e:
    print(f'Uh oh! You got an error!\n{e}')
    os.remove(f'{os.getcwd()}\\{filename}.py')
    os.system("pause")

finally:
    f.close()