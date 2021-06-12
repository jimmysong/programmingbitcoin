# [Programming Bitcoin](https://learning.oreilly.com/library/view/programming-bitcoin/9781492031482/)

### BY[ JIMMY SONG](https://github.com/jimmysong)

##### [O'Reilly Media, Inc.March 2019](https://learning.oreilly.com/library/publisher/oreilly-media-inc/)

# LICENSE

Repository for the book to be published by O'Reilly.

This book will be licensed under [CC-BY-NC-ND](https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode) once the book is published.


## Setting Up


To get the most out of this book, you’ll want to create an environment where you can run the example code and do the exercises. Here are the steps required to set everything up:

### 1. Install Python 3.5 or higher on your machine:

Windows:		
[https://www.python.org/ftp/python/3.6.2/python-3.6.2-amd64.exe](https://www.python.org/ftp/python/3.6.2/python-3.6.2-amd64.exe)

macOS:		
[https://www.python.org/ftp/python/3.6.2/python-3.6.2-macosx10.6.pkg](https://www.python.org/ftp/python/3.6.2/python-3.6.2-macosx10.6.pkg)

Linux		
##### See your distro docs (many Linux distributions, like Ubuntu, come with Python 3.5+ preinstalled)

### 2. Install pip by downloading this script: [https://bootstrap.pypa.io/get-pip.py](https://bootstrap.pypa.io/get-pip.py).

### 3. Run this script using Python 3:

```sh
python3 get-pip.py
```		

### 4. Install Git. The commands for downloading and installing it are at [https://git-scm.com/downloads](https://git-scm.com/downloads).

### 5. Download the source code for this book:

```sh
git clone https://github.com/jimmysong/programmingbitcoin		
cd programmingbitcoin
```
		
### 6. Install virtualenv:

```sh
pip install virtualenv
```

### 7. Install the requirements:

Linux/macOS

```sh
virtualenv -p python3 .venv		
. .venv/bin/activate
pip install -r requirements.txt
```

Windows

```cmd
virtualenv -p	
PathToYourPythonInstallation\Python.exe .venv	
.venv\Scripts\activate.bat		
pip install -r requirements.txt
```

### 8. Run Jupyter Notebook:

```cmd
jupyter notebook
```

You should have a browser open up automatically, as shown in [Figure P-1](https://raw.githubusercontent.com/jimmysong/programmingbitcoin/master/images/prbc_0001.png).

![](https://raw.githubusercontent.com/jimmysong/programmingbitcoin/master/images/prbc_0001.png)

MORE INFO AT: [https://learning.oreilly.com/library/view/programming-bitcoin/9781492031482/preface01.html#setting_up](https://learning.oreilly.com/library/view/programming-bitcoin/9781492031482/preface01.html#setting_up)
