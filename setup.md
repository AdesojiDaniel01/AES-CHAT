Setup Guide
1. Install Python

    Make sure Python 3.10+ is installed.

    Windows: Download from python.org
    Mac/Linux: usually comes with Python 3

    Run the following command to check if you have it: 

    python3 --version

2. Create a virtual environment

    From inside the project folder:

    python3 -m venv venv

    * Note, the second venv can be whatever you want to name your virtual environment. 
    

This creates a folder called venv/ that holds Python and the libraries that are imported..

3. Activate the virtual environment

    Linux / Mac:

    source venv/bin/activate


    Windows (PowerShell):

    venv\Scripts\Activate.ps1


    ** basically, cd into that Scripts (or bin folder) and then do the activate command. 
    You can also ./venv_folder_name/Scripts/activate from an outer folder to do the same thing.

After activating, your terminal prompt will show (venv) at the start. This indicates the virtual environment is active.
All pip installs should be run with the environment activated first.


4. Install project requirements
pip install -r requirements.txt


This pulls in all needed Python packages for the project.
Towards the end of our project, we'll need to update the requirements.txt file with whatever
import files we endup using.

5. Deactivate when done
    deactivate

6. Git ignore virtual environments

    Everyone will have their own venv name. Add it to .gitignore so it never gets committed.

    Open .gitignore and add your venv folder under this section:

    # Add your venv file names here to avoid committing them.
    venv/
    .AESCHATVenv/


    If you name yours something else (like .bobenv/), add that name to the list.

7. Running the project

    With your venv active:

    python -m app.server


    and in another terminal:

    python -m app.client