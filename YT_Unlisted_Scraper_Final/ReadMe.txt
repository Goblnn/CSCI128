This code will not run properly on Linux or ios (potentially, ios is unconfirmed) due to the 
msvcrt import not existing for those softwares. I know for a fact it does not work on Linux
as the Gradescope grader runs on Linux and cannot use the module when grading this 
project, however it works perfectly well on my Windows computer.

The msvcrt import functions as a keyboard interrupt, stopping the program when the user
hits "q" when focused on the terminal, or switching the amount of output information
each loop when the user hits "o." If you are using a Linux or ios computer, you can
replace lines 150-156 in main.py with the following code to stop the program automatically
after 10 seconds of runtime, effectively removing the point of error:

if(time.time() - loop_start_time > 10):
    break

You will also need to remove the import statement in line 1 to remove all errors. This
code will run in the exact same way, it will just end at a set time instead of running
until the user tells it to stop. 