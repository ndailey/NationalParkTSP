# README

**The Traveling Salesman Problem: National Parks Edition** creates the shortest route (by Euclidean distance) between coordinates inputted by the user. For further documentation and instructions, see **'NationalPark-TSP.ipynb'**. 

To use this script:

1. Set up Concorde using the steps outlined in this doc.
2. Open the 'TSP.py' file in an IDE of your choice (I used [iPython Notebook](https://ipython.org)). 
3. In a separate window, open 'ProjectManual.pdf'.
4. Read through 'ProjectManual.pdf' as you execute the TSP.py script, step-by-step. 
	a. The script should not be executed all at once. Some intermediate steps require you to work in the terminal. 
	b. The headers in ProjectManual.pdf coincide with headers in the TSP.py script for you to follow along.
5. The resulting web map will be located in `/Dailey_FinalProject/Results/TSP_webmap.html`. 

The project requires Python 3.5. Many of the modules and programs used will need to be installed from the terminal. Some modules (such as `numpy` and `pandas`) will require different versions depending on your version of Python. 

## Install Concorde on Mac
Adapted from [David Johnson's](http://davidsjohnson.net/TSPcourse/mac-install-concorde.txt) instructions.

#### Step 1 - Check your C compiler
Make sure your Mac has a working C compiler. Clang is fine. Type "cc" in the terminal to make sure it is installed. 

If not, you will need to install the Xcode command line tools. Instructions can be found [here](http://osxdaily.com/2014/02/12/install-command-line-tools-mac-os-x/).

#### Step 2 - Execute Concorde + QSOPT files
Concorde and QSOPT are already included in the '/Dailey_FinalProject' folder. All you need to do is execute the files in the terminal. 

In the terminal, 'cd' to the '/concorde' directory:
	
	cd /Users/<name>/Desktop/Dailey_FinalProject/concorde

#### Step 3 - Make QSOPT files
In the terminal type: 

	export QSOPTDIR=/Users/<name>/Desktop/Dailey_FinalProject/QSOPT

	export CFLAGS="-g -O3 -arch x86_64"

	./configure --with-qsopt=$QSOPTDIR --host=darwin

	make

#### Step 4 - Run Concorde
To test it, use the TSP instance provided: '/Dailey_FinalProject/sample.tsp' (downloaded from [here](http://www.iwr.uni-heidelberg.de/groups/comopt/software/TSPLIB95/tsp/)).

In the terminal type:
	
	cd /Users/<name>/Desktop/Dailey_FinalProject/concorde/TSP/
	
	./concorde /Users/<name>/Desktop/Dailey_FinalProject/sample.tsp


#### Troubleshooting
If after completing these steps Concorde still does not work, try downloading Concorde and QSOPT directly from the links below.

1. Download Concorde from [here](http://www.math.uwaterloo.ca/tsp/concorde/downloads/codes/src/co031219.tgz)
2. Untar it to the desired location (e.g., '/Desktop/Dailey_FinalProject/'). The directory will be called 'concorde'.
3. Download the Linear Programming solver [here](http://www2.isye.gatech.edu/~wcook/qsopt/beta/index.html).
4. You want the qsopt.a and qsopt.h files. Make sure you use the 64 bit Mac versions of the files. Store those in a directory of your choice. For the purposes of this example, we will call the directory 'QSOPT'.
5. After downloading Concorde and QSOPT, complete Steps 2-4 above.

#### Credits:
http://davidsjohnson.net/TSPcourse/mac-install-concorde.txt

http://wiki.evilmadscientist.com/Obtaining_a_TSP_solver

