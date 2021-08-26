# CSE 163 Project - Christopher Ku

In order to run my project you would firstly need to navigate to
the main directory. In it you can see a file called `main.py`. Click on
the file to access it. Assuming you are using VS Code on Windows you can
go on and click the Run in Terminal button on the top right corner of the
IDE (Green Arrowhead). As soon as you click on it you would need to wait for
some time for the program to run. When it finishes running you could navigate
to the figures file in the directory and view all of the plots made by my program.
If you are interested in seeing the tests I wrote for my program you could navigate
to the `data_test.py` folder and run it to see it pass all of the tests. You may
need to install the Plotly library via Anaconda to see the interactive plots that
my program makes when you run `main.py`.

Additional things to note:
* You will realize in main that some of the lines are long and fails flake8 that 
is because they are titles for my plots and some of them may be long.
* Lastly, I couldn't write a test for the first method in main because whenever I 
use assert_equals a ValueError comes up, but when I run it normally in main the code 
runs fine. I am unsure of this bug.
