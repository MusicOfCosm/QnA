# GUI

This is the GUI version of the project.


## QCM_GUI.py

At first, it was like the Terminal based project, with questions, one or multiple answers, and image support.

I later added colors to the corrections, blue for the question, green if everything is correct, orange for having some of the answers, and red for incorrect. I also added ordered answers, with the choice to use numbers or letters. I wanted to have another type of question for chemical formulae, which I have some commented out code from another project. Another thing that I thought of was a drag and drop system to answer with images, put I didn't actually do anything with the idea.

The terrible practice of importing and calling `main()` from another file continued, though this time, if you opened `QCM_GUI.py` directly you had the option to navigate your files to choose a Q&A, which would then use main from it. If you didn't open any files, you just had an example of all the different kinds of questions there are.
This was my first *proper* project, but I didn't have that much experience. At the time, I did not understand Object Oriented Programming, it was just too confusing (it still is). It's a shame too, since this project has the perfect use case for OOP, a question could have been made an object. Instead, I put everything into lists, and *somehow* made it work.