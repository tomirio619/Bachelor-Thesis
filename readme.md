* Make sure to compile with the `-shell-escape` flag for PdfLateX.
* Make sure you have the custom font MTPro2 installed (see `custom font`folder )
* Make sure you have installed pygmentize:
	* Assuming Windows OS, install Python 2.7
	* Assuming default install location for Python, add `C:\Python27` and `C:\Python27\Scripts` to Windows path (environment variable).
	* At Command Prompt, run `easy_install Pygments`
	* (Optional) Another way is to install pip (`easy_install pip`) and use pip to install pygments: `pip install pygments` 
	
* On the first run, the custom font will give an error on a specific line, saying that a specific symbol is already declared.
	Go to that specific line, and comment it. This will fix the error.
* Make sure all the MikTex packages are up to date.
	* Search for the program "MikTex Update (Admin)".
	* The first run, you won't be able to select any package to update.
	* Just click "next".
	* After if finishes, rerun the updater. All the packages should be selected when rerun. This will make sure all the packages are updated.
