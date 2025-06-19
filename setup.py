# this setup.py is responsible for creating my ML application as package. So, that anybody can use it.
from setuptools import find_packages,setup
from typing import List

HYPEN_E_DOT='-e .' # to remove -e . from requirements.txt
def get_requirements(file_path:str)->List[str]:
    '''
    this function will return the list of requirements
    '''
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines() # read the file i.e., requirements.txt line by line
        requirements=[req.replace("\n","") for req in requirements] # remove newline character(\n) from each requirement.txt file

        if HYPEN_E_DOT in requirements: # to remove -e . from requirements.txt
            requirements.remove(HYPEN_E_DOT)
    
    return requirements

setup(
name='mlproject',
version='0.0.1',
author='Rudra',
author_email='rudrachouhan0305@gmail.com',
packages=find_packages(),
install_requires=get_requirements('requirements.txt')

)

# -e . in requirements.txt which will automatically to install the packages from the current directory.
'''
### ✅ What does `-e .` mean in `requirements.txt`?

* `-e .` means **"install this project in editable mode"**.
* `.` means **"this folder"** (where your Python code is).

---

### 💡 Why use it?

When you are **writing your own Python project**, and you want to:

* Test it while still making changes
* Avoid reinstalling again and again after each change

You use `-e .`.

---

### 🧪 Example:

Imagine your folder looks like this:

```
my_project/
├── setup.py
├── my_code/
│   └── hello.py
└── requirements.txt
```

Your `requirements.txt` contains:

```
-e .
```

When you run:

```bash
pip install -r requirements.txt
```

It tells Python:

> "Install this folder (`my_project/`) as a package, but keep watching for any changes I make."

So if you edit `hello.py`, the changes will work **immediately** — no need to reinstall.

---

### 📌 You should use `-e .` only if:

* You're building your own Python package or app
* Your folder has a `setup.py` file
'''