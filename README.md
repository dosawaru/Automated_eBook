# Building Automated eBooks using Python and OpenAI

## Getting Started

To run this program, follow the steps below:

### Step 1: Create a Virtual Environment

Make a virtual environment with the following command:

```bash
python3 -m virtualenv env
```

### Step 2: Activate the Virtual Environment

Activate the virtual environment using the appropriate command for your operating system:

For Windows:

```bash
.\env\Scripts\activate
```

For macOS/Linux:

```bash
source env/bin/activate
```

### Step 3: Install Required Packages

Install the necessary Python packages (OpenAI and dotenv) using the following command:

```bash
pip install openai python-dotenv
```

### Step 4: Set Up OpenAI API Key

Create a .env file in the same directory and add your OpenAI API key:

OPENAI_API_KEY=<KEY_FROM_OPENAI_WEBSITE>

### Step 5: Run the Program

Execute the program with the following command:

```bash
python main.py
```

#Note

If you encounter issues activating the virtual environment on Windows, the command below is used to adjust the script execution policy for your currect session

```bash
Set-ExecutionPolicy Unrestricted -Scope Process
```
