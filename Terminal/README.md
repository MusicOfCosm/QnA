# Terminal

This is the first iteration of this project.

`QCM prototype_example.py` was more of a testing grounds. `A test Q&A.py` shows how a typical Q&A would be organized. With the path to `QCM.py` visible thanks to `sys.path.append()`, you could store your Q&A files wherever you wanted. Since I had learned about logging, I used its library to log the results of attemps.
What I didn't realize was how awful what I did is: importing and using `main()` from another file?! Only after using C did I realize how terrible of a thing to do this is.