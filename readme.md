# MS Analysis
This is the source code of my bachelor thesis which I wrote to obtain my Computer Science Bachelor Degree.
It could be useful for others to get a better idea of what a convenient structure would be when writing a big paper in LaTeX.  
Some people might wonder why on earth you would use LaTeX to typeset documents.
[This](http://www.andy-roberts.net/writing/latex/benefits) blog post should give you more insight in the advantages of using LaTeX.

## Notes
Some notes on using/compiling the source code:
* Make sure to compile with the `-shell-escape` flag for PdfLateX.
* Make sure you have the custom font MTPro2 installed
	* Create a new folder (e.g. `C:\Latex Fonts`)
	* Download MTPro2 from the [this](http://www.pctex.com/mtpro2.html) website (file will be called `mtp2lite.zip.tpm`). The file is also included in the `custom font` directory.
	* Put the file in the created folder (`C:\Latex Fonts`), change the extension to `.zip` and extract
	* Open MiKTeX Settings (Admin)
	* Go to the 'Roots' tab
	* Select 'Add'
	* Select the following dir: `C:\Latex Fonts\mtp2lite\texmf`
	* Select 'Apply'
	* Go to the 'General' tab and click 'refresh FNDB'
	* (Optional), create a new .tex file, and add the following imports:
```tex
\pdfmapfile{=mtpro2.map}	
\usepackage[lite, subscriptcorrection]{mtpro2}
```
* Make sure you have installed pygmentize:
	* Assuming Windows OS, install Python 2.7
	* Assuming default install location for Python, add `C:\Python27` and `C:\Python27\Scripts` to Windows path (environment variable).
	* At Command Prompt, run `easy_install Pygments`
	* (Optional) Another way is to install pip (`easy_install pip`) and use pip to install pygments: `pip install pygments` 
	
* On the first run, the custom font will give an error on a specific line, saying that a specific symbol is already declared:
```
Command `\hbar' already defined. ...thSymbol{\hbar} {\mathord}{symbols}{"84}`
```
Go to that specific line, and comment it. This will fix the error.
* Make sure all the MikTex packages are up to date:
	* Search for the program "MikTex Update (Admin)".
	* Just use all the default settings. Note that on the first run, you won't be able to select any package for updating.
	* After the updater finishes, rerun the updater. All the packages should be selected for updating.
