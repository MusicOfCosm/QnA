#!/usr/bin/env python3
import random
import logging
from datetime import datetime
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk

from sys import platform
if platform.startswith('win'): #if the program is being run on windows, the tkinter blurriness is removed
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1) #Don't know how it works, but it makes the text on windows not blurry, which is nice

#investigate tkinter.dnd — Drag and drop support
def example():
    global filename
    filename = "A test Q&A_GUI"
    #logging.basicConfig(filename=f"{filename}.log", level=logging.INFO)

    global test_type
    test_type = 'Mixed'

    global question_list
    question_list = []

    question3 = ["This is a example Q&A", 
                ['You may quit, the results are not logged', r"Rosace.ico"], 
                ['You may quit, the results are not logged'], 
                1, None, None, 'This quesion is literally worthless']

    question_list.append(question3)


    question1 = ["What is 9 by the power of 2?", 
                ['18', '2', '81', '4.5'], 
                ['81'], 
                1, r"Rosace.ico"]

    question_list.append(question1)


    question2 = ["What is 8 by the power of 2?", 
                ['16', '2', '64', '4', '8x8'], 
                ['64', '8x8'], 
                2, r"Rosace.ico"]

    question_list.append(question2)


    question4 = ["Order testing", 
                ['Step 1', 'Step 2', 'Step 3', 'Step 4'], 
                ['Step 1', 'Step 2', 'Step 3', 'Step 4'], 
                1, None,
                None,
                '',
                'numbers']

    question_list.append(question4)


    question5 = ["Order testing 2", 
                ['Step A', 'Step B', 'Step C', 'Step D'], 
                ['Step A', 'Step B', 'Step C', 'Step D'], 
                1, None,
                None,
                '',
                'letters']

    question_list.append(question5)


    question7 = ["Match testing", 
                ['1st choice', '2nd choice', '3rd choice', '4th choice', 'image'], 
                {'The first is': '1st choice', 'The second is': '2nd choice', 'The third is': '3rd choice', 'The fourth is': '4th choice', r"Rosace.ico": 'image'}, 
                1, None,
                None,
                '',
                '']

    question_list.append(question7)


    question6 = ["Entry testing", 
                ['write in'],#, 'This is a one word answer, and a test'], 
                ['answer'], 
                1, None,
                None,
                '',
                '']

    question_list.append(question6)

    for i in range(len(question_list)):
        if 'write in' not in question_list[i][1][0]:
            random.shuffle(question_list[i][1])
        
        if isinstance(question_list[i][2], dict):
            dictio = list(question_list[i][2].items())
            random.shuffle(dictio)
            question_list[i][2] = dict(dictio)

    # random.shuffle(question_list)

def main(test_type, question_list, title):
    root = Tk()
    root.attributes("-topmost", True) #So that you don't see the windows in the back
    def setup(title): #Just to gain some space
        root.title(title)
        root.iconbitmap(r'Rosace.ico')
        root.state('zoom') #basically fullscreen but with the buttons on top, 'zoomed' does the same

        global canvas
        global scroll
        global content

        canvas = Canvas(root)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        scroll = ttk.Scrollbar(root, orient=VERTICAL, command=canvas.yview)
        scroll.pack(side=RIGHT, fill=Y)

        canvas.config(yscrollcommand=scroll.set) #configure and config do the same thing
        canvas.bind('<Configure>', lambda event: canvas.config(scrollregion=canvas.bbox('all'))) #e: event, bbox: bounding box
        if platform.startswith('win'):
            canvas.bind_all('<MouseWheel>', lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))
        else: canvas.bind_all('<MouseWheel>', lambda event: canvas.yview_scroll(int(-1*(event.delta/1)), "units"))

        def reset_scrollregion(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        content = Frame(canvas)
        content.bind("<Configure>", reset_scrollregion)
        canvas.create_window((0,0), window=content, anchor='nw')
    setup(title)

    points_var = []
    end_answers = []
    p_end_answers = []
    for _ in range(len(question_list)):
        points_var.append(DoubleVar())
        end_answers.append('')
        p_end_answers.append('')


    progress = ttk.Progressbar(content, maximum=len(question_list), length=750)
    progress.pack()


    img_global_list = [] #a place to store images to memory so they don't get overwritten

    def Study(content, scroll, test_type, question, choices, answers, points, image, w_expl=None, img_expl=None, order=''):

        try: n = question_list.index([question, choices, answers, points, image]) #The list is there to have a consistent number
        except:
            try: n = question_list.index([question, choices, answers, points, image, w_expl])
            except:
                try: n = question_list.index([question, choices, answers, points, image, w_expl, img_expl])
                except : n = question_list.index([question, choices, answers, points, image, w_expl, img_expl, order])

        if not isinstance(answers, dict):
            for i in answers:
                if i not in choices and 'write in' not in choices:
                    print(question, '\n', i)
                    raise UnboundLocalError(f'One, or multiple answers are not in the list of choices! You probably have to change your program.\nIt\'s question {n+1}')

        if ',' in str(answers):               #If there's multiple answers, a correct answer gives you the worth 
            point_value = points/len(answers) #of the question, divided by the number of correct answers there are
        else: point_value = points            #Otherwise, the correct answer just gives you the amount of points the question is worth

        if test_type == 'Mixed':
            if len(answers) > 1:
                q_type = 'QCM'
            else: q_type = 'QCU'

        else: q_type = test_type

        Q_widget = Label(None, text=f'Question {n+1}', font=('Verdana', 10, 'bold'), fg='blue')
        Q_Frame = LabelFrame(content, labelwidget=Q_widget, labelanchor=N, borderwidth=5, relief=GROOVE) #relief doesn't work with ttk (though it should)
        Q_Frame.pack(pady=20, ipady=3)

        Label(Q_Frame, text=question, font=('Verdana', 10), wraplength=1888/1.5, justify=LEFT).grid()
        if points <= 1: ttk.Label(Q_Frame, text=f'(This question is worth {points} point)', font=('Verdana', 8)).grid()
        else: Label(Q_Frame, text=f'(This question is worth {points} points)', font=('Verdana', 8)).grid()
        
        if isinstance(image, list) or isinstance(image, tuple):
            image_list = image
            for image in image_list:
                if isinstance(image, str) and image != '':
                    global img #If this isn't done, the image gets garbage collected, and a blank space is displayed where the image should be
                    img = ImageTk.PhotoImage(Image.open(image))
                    render = Label(Q_Frame, image=img)
                    render.grid()
                    img_global_list.append(img)
        else:
            if isinstance(image, str) and image != '':
                img = ImageTk.PhotoImage(Image.open(image))
                render = Label(Q_Frame, image=img)
                render.grid()
                img_global_list.append(img) #Stores the image so that it doesn't disappear

        Label(Q_Frame).grid() #Space

        choice_frame = Frame(Q_Frame)
        choice_frame.grid()

        def ordered(p_end_answers):
            if order != '' and order != False:
                for k in range(len(choices)):
                    try: globals()[f'answer{n}-{k}'].pack_forget()
                    except: pass
                order_frame.config(height=1) #resets height

                for k, answer_label in enumerate(p_end_answers[n]):
                    globals()[f'answer{n}-{k}'] = Label(order_frame, font=(0), height=0, wraplength=1888/1.5, justify=LEFT, anchor=W)
                    globals()[f'answer{n}-{k}'].pack()#pack(padx=(1888-width.get())/2, fill=BOTH, expand=True)

                    if answer_label.endswith(('.png', '.jpeg', '.jpg', '.jfif', '.ico')):
                        global img
                        img = ImageTk.PhotoImage(Image.open(answer_label))
                        img_global_list.append(img)
                        answer_label = img

                    if 'pyimage' in globals()[f'answer{n}-{k}']['image']:
                        globals()[f'answer{n}-{k}'].config(text='', image='', font=(0))

                    if order.lower() == 'numbers':
                        if isinstance(answer_label, ImageTk.PhotoImage):
                            globals()[f'answer{n}-{k}'].config(text=f'{k+1} - ', image=answer_label, compound='right', wraplength=1888/1.5, justify=LEFT, font=(12)) #compound puts the image in a direction from the text
                        else:
                            globals()[f'answer{n}-{k}'].config(text=f'{k+1} - {answer_label}', wraplength=1888/1.5, justify=LEFT, font=(13))

                    elif order.lower() == 'letters':
                        if isinstance(answer_label, ImageTk.PhotoImage):
                            globals()[f'answer{n}-{k}'].config(text=f'{chr(k+65)} - ', image=answer_label, compound='right', wraplength=1888/1.5, justify=LEFT, font=(12))
                        else:
                            globals()[f'answer{n}-{k}'].config(text=f'{chr(k+65)} - {answer_label}', wraplength=1888/1.5, justify=LEFT, font=(13))

                    else:
                        if isinstance(answer_label, ImageTk.PhotoImage):
                            globals()[f'answer{n}-{k}'].config(text='- ', image=answer_label, compound='right', wraplength=1888/1.5, justify=LEFT, font=(12))
                        else:
                            globals()[f'answer{n}-{k}'].config(text=f'- {answer_label}', wraplength=1888/1.5, justify=LEFT, font=(12))


        def getvalue(var, index, answer_list=None): #Fucker won't shut up about answer_list since I added match questions
            if isinstance(answers, dict):
                answer_list = [var.get() for var in var_list] #Combobox work differently than check/radiobuttons
                end_answers[n] = dict(zip(keys, answer_list))

                nb_good_answers = 0.0
                for index in range(len(answer_list)):
                    if answer_list[index] == list(answers.values())[index]:
                        nb_good_answers += point_value
                points_var[n].set(nb_good_answers)

                if end_answers[n] == answers:
                    points_var[n].set(points)


            elif q_type == 'QCM':
                answer_list.append(var.get())
                if 'Off' in answer_list:
                    answer_list.remove('Off')
                    answer_list.remove(choices[index])

                end_answers[n] = answer_list
                    
                if order: #Empty strings '' (default value) are considered False
                    p_end_answers[n] = answer_list
                    ordered(p_end_answers)


                if set(answer_list).issubset(answers): # x.issubset(y) returns True if all elements in set x are in set y regardless of len(x)
                    for i in answer_list:
                        if i in answers:
                            points_var[n].set(len(answer_list) * point_value)

                else: points_var[n].set(0.0)


            else: #if QCU
                if 'write in' in choices[0].lower() and len(choices) < 3 or 'write in' in choices[0].lower() and len(choices) == 3 and choices[2] != True: #if the casing of write in matters
                    var.set(var.get().lower())
                    answers[0] = answers[0].lower()

                if var.get() in answers: points_var[n].set(points)
                else: points_var[n].set(0.0)

                end_answers[n] = var.get()

                if 'write in' in choices[0].lower() and var.get() == '': #To reset var to the greyed out message if needs be
                    var.set(grey_msg)
                    color.set('grey')
                    write_in.configure(textvariable=var, fg=color.get())


        iteration = 0
        width = DoubleVar()

        if 'write in' in choices[0].lower():
            q_type = 'QCU' #In case test_type is set to QCM

            if len(choices) > 1 and choices[1] != '':
                grey_msg = choices[1]  
            else: grey_msg = 'Write in'
            var = StringVar(Q_Frame, grey_msg)
            color = StringVar(Q_Frame, 'grey')

            write_in = Entry(Q_Frame, textvariable=var, fg=color.get(), justify=CENTER, width=30)#, cursor='question_ar')
            write_in.grid()


            def focus_out(event):
                Q_Frame.focus_set()
                if var.get() =='':
                    var.set(grey_msg)
                    color.set('grey')
                    write_in.configure(textvariable=var, fg=color.get())


            def writing(event):
                if color.get() == 'grey' and var.get() == grey_msg:
                    var.set('')
                    color.set('black')
                    write_in.configure(textvariable=var, fg=color.get()) #If it's not there, the grey doesn't set in


            Q_Frame.bind('<1>', focus_out)
            write_in.bind('<1>', writing)
            write_in.bind('<Key>', writing) #KeyPress also works
            write_in.bind('<KeyRelease>', lambda e, var=var, index=0: getvalue(var, index)) #an event parameter is generated with bind, event=None

            '''
            if 'formulae' in choices[0].lower():
                import pubchempy as pcp
                from rdkit import Chem
                from rdkit.Chem import Draw
                import webbser

                def formulae(smiles, zoom):
                    try: 
                        template = Chem.MolFromSmiles(smiles.get())
                        
                        image = Draw.MolToImage(template, (zoom.get(), zoom.get()))
                        image.save('temp_image.png')
                        image = 'temp_image.png'

                        global img
                        img = ImageTk.PhotoImage(Image.open(image))
                        render.config(image=img)
                        img_global_list.append(img)
                    except: pass

                zoom = IntVar(root, 500)

                write_in.bind('<KeyRelease>', lambda event, var=var, zoom=zoom: formulae(var, zoom))

                import webbser
                link = Label(root, text="SMILES", fg='blue', cursor='hand2')
                link.pack()
                link.bind('<Button-1>', lambda event: webbser.open_new_tab('https://en.wikipedia.org/wiki/Simplified_molecular-input_line-entry_system'))

                render = Label(root, image='')
                render.pack()

                def zooming(yes):
                    if yes:
                        zoom.set(zoom.get() + 100)
                    else: 
                        zoom.set(zoom.get() - 100)

                    formulae(var, zoom)

                Z_in = ttk.Button(root, text='Zoom in', command=lambda: zooming(True))
                Z_in.pack()
                Z_out = ttk.Button(root, text='Zoom out', command=lambda: zooming(False))
                Z_out.pack()
            '''

            Label(Q_Frame).grid()


        elif isinstance(answers, dict):
            def create_combox(i):
                if keys[i].endswith(('.png', '.jpeg', '.jpg', '.jfif', '.ico')):
                    global img
                    img = ImageTk.PhotoImage(Image.open(keys[i]))
                    img_global_list.append(img)
                    is_image = True
                else: is_image = False

                if small and not is_image: #Next to each other
                    ttk.Label(choice_frame, text=keys[i] + ' ').grid(row=i, column=0, sticky=E, pady=5)

                    globals()[f'choice{i}'] = ttk.Combobox(choice_frame, textvariable=var_list[i], values=('', *choices))
                    globals()[f'choice{i}'].grid(row=i, column=1, sticky=W, padx=(0, 10), pady=5)

                else: #Piled
                    if is_image:
                        ttk.Label(choice_frame, image=img, wraplength=1888/2, justify=LEFT).grid(row=2*i, sticky=S)
                    else: ttk.Label(choice_frame, text=keys[i], wraplength=1888/2, justify=LEFT).grid(row=2*i, sticky=S)

                    globals()[f'choice{i}'] = ttk.Combobox(choice_frame, textvariable=var_list[i], values=('', *choices))
                    globals()[f'choice{i}'].grid(row=2*i+1, sticky=N, pady=(5, 30))
                
                globals()[f'choice{i}'].state(['readonly'])

                #https://stackoverflow.com/questions/44268882/remove-ttk-combobox-mousewheel-binding
                def empty_scroll_command(event):
                    return "break"
                globals()[f'choice{i}'].bind("<MouseWheel>", empty_scroll_command)

                def rebind_box(event):
                    return "TCombobox"

                globals()[f'choice{i}'].bind('<1>', lambda e: [canvas.unbind_all('<MouseWheel>'),
                                                              globals()[f'choice{i}'].bind("<MouseWheel>", rebind_box)])

                def rebind(_):
                    canvas.bind_all('<MouseWheel>', lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))
                choice_frame.bind('<FocusIn>', rebind)

                globals()[f'choice{i}'].bind('<<ComboboxSelected>>', lambda e, var=var_list[i], index=i: 
                                                                    [getvalue(var, index, answer_list),
                                                                    choice_frame.focus_set(), #To not get highlighted text
                                                                    rebind]) #Rebinding content scroll


            answer_list = []
            keys = list(answers.keys())
            small = True
            for key in keys:
                if len(key) < 100 and small == True and not key.endswith(('.png', '.jpeg', '.jpg', '.jfif', '.ico')):
                    pass
                else : small = False

            var_list = []
            for i in range(len(answers)):
                var_list.append(StringVar())
                create_combox(i)


        elif q_type == 'QCM':
            def create_cb(i):
                if choices[i].endswith(('.png', '.jpeg', '.jpg', '.jfif', '.ico')):
                    global img
                    img = ImageTk.PhotoImage(Image.open(choices[i]))
                    img_global_list.append(img)
                    globals()[f'choice{i}'] = ttk.Checkbutton(choice_frame, command=lambda: getvalue(var[i], i, answer_list), image=img, variable=var[i], onvalue=choices[i], offvalue='Off') #var.set(choices[i] or 'Off')
                    globals()[f'choice{i}'].grid(sticky=W)

                else:
                    globals()[f'choice{i}'] = ttk.Checkbutton(choice_frame, command=lambda: getvalue(var[i], i, answer_list), text=choices[i], variable=var[i], onvalue=choices[i], offvalue='Off')
                    globals()[f'choice{i}'].grid(sticky=W)

            answer_list = []
            var = []
            for i in range(len(choices)):
                var.append(StringVar()) #A list of StringVar() is made which will all have their own Checkbutton
                create_cb(i) #Has to pass through a function to work >:(


            if order != '' and order != False: #If anything is written in order, it will be an 'order' question (even if it's a string of random characters)
                def clear():
                    answer_list.clear()
                    [globals()[f'choice{i}'].state(['!selected']) for i in range(len(var))]
                    points_var[n].set(0.0)
                    end_answers[n] = ''

                order_frame = Frame(Q_Frame)
                order_frame.grid()

                ttk.Button(Q_Frame, text='clear', command=clear).grid(pady=15)#pack(padx=(1888-width.get())/2)


        elif q_type == 'QCU':
            def create_rb(i):
                if choices[i].endswith(('.png', '.jpeg', '.jpg', '.jfif', '.ico')):
                    global img
                    img = ImageTk.PhotoImage(Image.open(choices[i]))
                    img_global_list.append(img)
                    globals()[f'q_choice{i}'] = ttk.Radiobutton(choice_frame, command=lambda: getvalue(var, i, ), image=img, variable=var, value=choices[i])
                    globals()[f'q_choice{i}'].grid(sticky=W)

                else:
                    globals()[f'q_choice{i}'] = ttk.Radiobutton(choice_frame, command=lambda: getvalue(var, i, ), text=choices[i], variable=var, value=choices[i])
                    globals()[f'q_choice{i}'].grid(sticky=W)

            var = StringVar() #All Radiobuttons will be tied together
            for i in range(len(choices)):
                create_rb(i) #Has to pass through a function to work >:(

            def clear():
                var.set('')
                [globals()[f'q_choice{i}'].state(['!selected']) for i in range(len(choices))]
                points_var[n].set(0.0)
                end_answers[n] = ''

            ttk.Button(Q_Frame, text='clear', command=clear).grid(pady=15)#pack(padx=(1888-width.get())/2)

        else: raise ValueError('Your code does not indicate a test type (QCM, QCU, Mixed...).')

        progress['value'] = n+1

        if n+1 != len(question_list): Label(content, pady=20, text=175*'_').pack()

        return points

    ttk.Label(content, text='Answering incorrectly to a question will yield you 0 point.', font=('Verdana', 12, 'bold')).pack()

    max_score = 0
    for args in question_list:
        question_worth = Study(content, scroll, test_type, *args)
        max_score += question_worth

    progress.destroy()
    root.after_idle(root.attributes, '-topmost', False)
    
    def Finish():
        Done['state'] = DISABLED

        score = 0
        for i in range(len(question_list)):
            score += points_var[i].get()

        global total_score
        total_score = round(score/max_score*20, 2) #Mean of all questions out of 20, with 2 decimal places

        root.destroy() #Closes the window

    Done = ttk.Button(content, text='End', command=Finish)
    Done.pack()
    ttk.Label(content, width=190).pack()

    root.mainloop()

    try: 
        if logging: logging.info(f'\n On {datetime.now().strftime("%B %d, %Y at %H:%M:%S")}, you got a score of {total_score}/20\n')
    except: 
        import sys
        sys.exit()


    root = Tk()
    setup(title+' - Correction')

    progress = ttk.Progressbar(content, maximum=len(question_list), length=750)
    progress.pack(pady=20)
    

    img_global_list = []

    Label(content, text=f'You got a total score of {total_score}/20!', font=('Verdana', 12, 'bold', 'underline'), fg='red').pack()
    ttk.Label(content, width=190).pack()

    for i in range(len(question_list)):
        if 'write in' in question_list[i][1][0] or len(question_list[i][2]) == 1: q_type = 'QCU'
        else: q_type = 'QCM'

        correct = False #For later, to activate the correction or not


        Q_widget = Label(None, text=f'Question {i+1}', font=('Verdana', 10, 'bold'), fg='blue')
        Q_Frame = LabelFrame(content, labelwidget=Q_widget, labelanchor=N, borderwidth=5, relief=GROOVE) #relief doesn't work with ttk (though it should)
        Q_Frame.pack(pady=20, ipady=3)

        Label(Q_Frame, text=question_list[i][0], font=('Verdana', 11), wraplength=1888/1.5, justify=LEFT, fg='blue').grid()

        if isinstance(question_list[i][4], list) or isinstance(question_list[i][4], tuple):
            for image in question_list[i][4]:
                if isinstance(image, str) and image != '':
                    img = ImageTk.PhotoImage(Image.open(image))
                    render = Label(Q_Frame, image=img)
                    render.grid()
                    img_global_list.append(img)
        
        else:
            image = question_list[i][4]
            if isinstance(image, str) and image != '':
                img = ImageTk.PhotoImage(Image.open(image))
                render = Label(Q_Frame, image=img)
                render.grid()
                img_global_list.append(img)


        if q_type == 'QCM': Label(Q_Frame, text='Your answer(s):', font=('Verdana', 10, 'underline')).grid()
        else: Label(Q_Frame, text='Your answer:', font=('Verdana', 10, 'underline')).grid()


        if not isinstance(end_answers[i], list):
            buffer = []
            buffer.append(end_answers[i])
            end_answers[i] = buffer

        true_end_answers = [] #a deep copy is an independent copy (a shallow copy would have the same id)
        for item in end_answers:
            try: # this is for objects that raise errors when slicing (such as int or dict)
                true_end_answers.append(item[:])
            except:
                true_end_answers.append('')


        for k in range(len(end_answers[i])):
            if str(end_answers[i][k]).endswith(('.png', '.jpeg', '.jpg', '.jfif', '.ico')):
                img = ImageTk.PhotoImage(Image.open(end_answers[i][k]))
                end_answers[i][k] = img


        answer_frame = Frame(Q_Frame)
        answer_frame.grid()

        for k in range(len(end_answers[i])):
            color = StringVar(answer_frame, 'green')


            if isinstance(end_answers[i][k], dict):
                if end_answers[i][k] == question_list[i][2]:
                    correct = True

                for index in range(len(end_answers[i][k].values())):
                    given_values = tuple(end_answers[i][k].values())
                    real_values = tuple(question_list[i][2].values())
                    
                    if given_values[index] == real_values[index]:
                        color.set('green')
                    else: color.set('red')

                    keys = tuple(question_list[i][2].keys())
                    if bool(given_values[index]): #If it's not a empty string
                        if keys[index].endswith(('.png', '.jpeg', '.jpg', '.jfif', '.ico')):
                            img = ImageTk.PhotoImage(Image.open(keys[index]))
                            img_global_list.append(img)
                            Label(answer_frame, image=img, text=given_values[index], compound='top', font=('Verdana', 10), fg='blue', wraplength=1888/1.5, justify=LEFT).grid(sticky=W, pady=(5, 30))
                            
                        else: Label(answer_frame, text=(keys[index] + ' - ' + given_values[index]), font=('Verdana', 10), fg=color.get(), wraplength=1888/1.5, justify=LEFT).grid(sticky=W)


            elif q_type == 'QCU': #If QCU or write in
                if len(true_end_answers[i]) > len(question_list[i][2]) or true_end_answers[i][k] != question_list[i][2][0]:
                    color.set('red')
                else: correct = True

                if isinstance(end_answers[i][k], ImageTk.PhotoImage):
                    Label(answer_frame, image=end_answers[i][k], font=('Verdana', 10), bg=color.get(), wraplength=1888/1.5, justify=LEFT).grid()
                elif end_answers[i][k] != '':
                    Label(answer_frame, text=end_answers[i][k], font=('Verdana', 10), fg=color.get(), wraplength=1888/1.5, justify=LEFT).grid()


            elif len(question_list[i]) == 8 and question_list[i][7] != '' and question_list[i][7] != False and end_answers[i][k] != '': #If order
                if true_end_answers[i] != question_list[i][2]: #If incorrect
                    color.set('red')
                else: correct = True

                if question_list[i][7].lower() == 'numbers':
                    if isinstance(end_answers[i][k], ImageTk.PhotoImage):
                        Label(answer_frame, text=f'{k+1} - ', image=end_answers[i][k], compound='right', font=('Verdana', 10), fg=color.get(), wraplength=1888/1.5, justify=LEFT).grid()
                    else:
                        Label(answer_frame, text=f'{k+1} - {end_answers[i][k]}', font=('Verdana', 10), fg=color.get(), wraplength=1888/1.5, justify=LEFT).grid(sticky=W)

                elif question_list[i][7].lower() == 'letters':
                    if isinstance(end_answers[i][k], ImageTk.PhotoImage):
                        Label(answer_frame, text=f'{chr(k+65)} - ', image=end_answers[i][k], compound='right', font=('Verdana', 10), fg=color.get(), wraplength=1888/1.5, justify=LEFT).grid()
                    else:
                        Label(answer_frame, text=f'{chr(k+65)} - {end_answers[i][k]}', font=('Verdana', 10), fg=color.get(), wraplength=1888/1.5, justify=LEFT).grid(sticky=W)

                else:
                    if isinstance(end_answers[i][k], ImageTk.PhotoImage):
                        Label(answer_frame, text='- ', image=end_answers[i][k], compound='right', font=('Verdana', 10), fg=color.get(), wraplength=1888/1.5, justify=LEFT).grid()
                    else:
                        Label(answer_frame, text=f'- {end_answers[i][k]}', font=('Verdana', 10), fg=color.get(), wraplength=1888/1.5, justify=LEFT).grid(sticky=W)


            elif sorted(true_end_answers[i]) == sorted(question_list[i][2]): #QCM
                if isinstance(end_answers[i][k], ImageTk.PhotoImage):
                    Label(answer_frame, image=end_answers[i][k], font=('Verdana', 10), bg='green', wraplength=1888/1.5, justify=LEFT).grid()
                else:
                    Label(answer_frame, text=f'- {end_answers[i][k]}', font=('Verdana', 10), fg='green', wraplength=1888/1.5, justify=LEFT).grid(sticky=W)
                correct = True

            elif set(true_end_answers[i]).issubset(question_list[i][2]): #If you got some of the answers in a QCM
                if isinstance(end_answers[i][k], ImageTk.PhotoImage):
                    Label(answer_frame, image=end_answers[i][k], font=('Verdana', 10), bg='orange', wraplength=1888/1.5, justify=LEFT).grid()
                else:
                    Label(answer_frame, text=f'- {end_answers[i][k]}', font=('Verdana', 10), fg='orange', wraplength=1888/1.5, justify=LEFT).grid(sticky=W)

            else:
                if isinstance(end_answers[i][k], ImageTk.PhotoImage):
                    Label(answer_frame, image=end_answers[i][k], font=('Verdana', 10), bg='red', wraplength=1888/1.5, justify=LEFT).grid()
                elif end_answers[i][k] != '':
                    Label(answer_frame, text=f'- {end_answers[i][k]}', font=('Verdana', 10), fg='red', wraplength=1888/1.5, justify=LEFT).grid(sticky=W)
        
        
        Label(Q_Frame).grid() #Space


        if not correct: #If not True:
            if len(question_list[i][2]) == 1: #If the question has only one answer
                if question_list[i][2][0].endswith(('.png', '.jpeg', '.jpg', '.jfif', '.ico')):
                    img = ImageTk.PhotoImage(Image.open(question_list[i][2][0]))
                    question_list[i][2][0] = img

                Label(Q_Frame, text='Correct answer:', font=('Verdana', 10, 'underline')).grid()
                if isinstance(question_list[i][2][0], ImageTk.PhotoImage):
                    Label(Q_Frame, image=question_list[i][2][0], font=('Verdana', 10), bg='blue', wraplength=1888/1.5, justify=LEFT).grid()
                else:
                    Label(Q_Frame, text=question_list[i][2][0], font=('Verdana', 10), fg='blue', wraplength=1888/1.5, justify=LEFT).grid()
                

            else: #If the question has multiple answers
                Label(Q_Frame, text='Correct answers:', font=('Verdana', 10, 'underline')).grid()

                correction_frame = Frame(Q_Frame)
                correction_frame.grid()

                if isinstance(question_list[i][2], dict):
                    if question_list[i][7] == True:
                        for keys, values in sorted(question_list[i][2].items()):
                            if keys.endswith(('.png', '.jpeg', '.jpg', '.jfif', '.ico')):
                                img = ImageTk.PhotoImage(Image.open(keys))
                                img_global_list.append(img)
                                Label(correction_frame, image=img, text=values, compound='top', font=('Verdana', 10), fg='blue', wraplength=1888/1.5, justify=LEFT).grid(sticky=W, pady=(5, 30))
                            
                            else: Label(correction_frame, text=(keys + ' - ' + values), font=('Verdana', 10), fg='blue', wraplength=1888/1.5, justify=LEFT).grid(sticky=W, pady=(5, 30))
                    else: 
                        for keys, values in question_list[i][2].items():
                            if keys.endswith(('.png', '.jpeg', '.jpg', '.jfif', '.ico')):
                                img = ImageTk.PhotoImage(Image.open(keys))
                                img_global_list.append(img)
                                Label(correction_frame, image=img, text=values, compound='top', font=('Verdana', 10), fg='blue', wraplength=1888/1.5, justify=LEFT).grid(sticky=W, pady=(5, 30))
                            
                            else: Label(correction_frame, text=(keys + ' - ' + values), font=('Verdana', 10), fg='blue', wraplength=1888/1.5, justify=LEFT).grid(sticky=W, pady=(5, 30))

                else:
                    for k, answer in enumerate(question_list[i][2]):
                        if question_list[i][2][k].endswith(('.png', '.jpeg', '.jpg', '.jfif', '.ico')):
                            img = ImageTk.PhotoImage(Image.open(question_list[i][2][k]))
                            question_list[i][2][k] = img

                        if len(question_list[i]) == 8 and question_list[i][7] != False and question_list[i][7].lower() == 'numbers':
                            if isinstance(question_list[i][2][k], ImageTk.PhotoImage):
                                Label(correction_frame, text=f'{k+1} - ', image=question_list[i][2][k], compound='right', font=('Verdana', 10), fg='blue', wraplength=1888/1.5, justify=LEFT).grid()
                            else:
                                Label(correction_frame, text=f'{k+1} - {question_list[i][2][k]}', font=('Verdana', 10), fg='blue', wraplength=1888/1.5, justify=LEFT).grid(sticky=W)#pack(padx=(1888-width[1][i].get())/2, expand=True, fill=BOTH)
                            
                        elif len(question_list[i]) == 8 and question_list[i][7] != False and question_list[i][7].lower() == 'letters':
                            if isinstance(question_list[i][2][k], ImageTk.PhotoImage):
                                Label(correction_frame, text=f'{chr(k+65)} - ', image=question_list[i][2][k], compound='right', font=('Verdana', 10), fg='blue', wraplength=1888/1.5, justify=LEFT).grid()
                            else:
                                Label(correction_frame, text=f'{chr(k+65)} - {question_list[i][2][k]}', font=('Verdana', 10), fg='blue', wraplength=1888/1.5, justify=LEFT).grid(sticky=W)#pack(padx=(1888-width[1][i].get())/2, expand=True, fill=BOTH)
                        
                        else:
                            if isinstance(question_list[i][2][k], ImageTk.PhotoImage):
                                Label(correction_frame, image=question_list[i][2][k], font=('Verdana', 10), bg='blue', wraplength=1888/1.5, justify=LEFT).grid()
                            else:
                                Label(correction_frame, text=f'- {question_list[i][2][k]}', font=('Verdana', 10), fg='blue', wraplength=1888/1.5, justify=LEFT).grid(sticky=W)#pack(padx=(1888-width[1][i].get())/2, expand=True, fill=BOTH)
        
        else: Label(Q_Frame, text="You have answered correctly.", font=('Verdana', 10), fg='blue').grid()
        

        if len(question_list[i]) >= 6 and question_list[i][5] != None or len(question_list[i]) >= 7 and question_list[i][6] != '': #If there's an explanation
            Label(Q_Frame).grid()
            Label(Q_Frame, text='Explanation:', font=('Verdana', 10, 'underline')).grid()
            Explanation = Frame(Q_Frame)
            Explanation.grid()

            if isinstance(question_list[i][5], list) or isinstance(question_list[i][5], tuple):
                for image in question_list[i][5]:
                    if isinstance(image, str) and image != '':
                        img = ImageTk.PhotoImage(Image.open(image))
                        render = Label(Explanation, image=img)
                        render.grid()
                        img_global_list.append(img)
            
            else:
                image = question_list[i][5]
                if isinstance(image, str) and image != '':
                    img = ImageTk.PhotoImage(Image.open(image))
                    exp_render = Label(Explanation, image=img)
                    exp_render.grid()
                    img_global_list.append(img)

            if len(question_list[i]) >= 7 and question_list[i][6] != '':
                exp_text = Label(Explanation, text=question_list[i][6], font=('Verdana', 10), wraplength=1888/1.5, justify=LEFT)
                exp_text.grid()


        if i+1 != len(question_list): Label(content, pady=20, text=175*'_').pack()

        progress['value'] = i+1

    progress.destroy()
    ttk.Button(content, text='Close', command=lambda: root.destroy()).pack()
    ttk.Label(content, width=190).pack()

    root.mainloop()

    try:
        import os
        os.remove('temp_image.png')
    except: pass

if __name__ == '__main__':
    root = Tk()
    root.overrideredirect(True)
    root.attributes('-alpha', 0)
    file = filedialog.askopenfilename(initialdir=r"",
                                      title='Select the Q&A you wish to use to study',
                                      filetypes=[('Python files', '.py')])
    root.destroy()
    from subprocess import call
    if file == '':
        example()
        main(test_type, question_list, filename)
    
    else:
        call(["python", file])
