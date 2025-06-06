# lolcode-python-py

## OVERVIEW
<p align="justify">
This is a LOLCODE interpreter built using Python and Tkinter (for the GUI). It is based on the specifications from http://www.lolcode.org/. While the features may not exactly match the original, this project aims to closely mimic its behavior. The author’s purpose in building this project is to create a simple programming language from scratch and to understand the phases of lexer, parser, and interpreter.
</p>

### Author’s Note:
<p align="justify">
Originally, this was a group project (team of two) at the author’s university. Although the team submitted a satisfactory version, the author decided to revive this project to improve it by fixing bugs and adding new features. While it started as a group project, it is worth noting that the code retrieved from the original repository includes only the work done by the author. As a result, this has become author's solo project.
</p>

## Prerequisites
- [Python 3](https://www.python.org/downloads/)
- [tkinter](https://docs.python.org/3/library/tkinter.html)

## How to Run
1. Clone the repository to your local machine:  
   `git clone https://github.com/krispypatata/lolcode-interpreter-py.git`

2. Open a terminal in the project’s root directory.

3. Run the program by typing:  
   `python3 lolcode.py`

4. Alternatively, if you have `make` installed, simply run:  
   `make`

5. To test the program without the GUI:  
   - Open `lolcode.py` in your code editor.  
   - In the `__main__` section, comment out the GUI-related statements and uncomment the call to `test_run_lolcode()`.  
   - You can modify the `test_run_lolcode` function as needed for testing.  
   - Alternatively, you can also use the `handle_run_lolcode()` function.

