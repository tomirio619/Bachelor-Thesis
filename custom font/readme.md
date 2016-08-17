* Create a new folder (e.g. `C:\Latex Fonts`)
* Download MTPro2 from the [this](http://www.pctex.com/mtpro2.html) website (file will be called mtp2lite.zip.tpm)
* Put the file in the created folder (`C:\Latex Fonts`), change the extension to `.zip` and extract
* Open MiKTeX Settings (Admin)
* Go to the 'Roots' tab
* Select 'Add'
* Select the following dir: `C:\Latex Fonts\texmf`
* Select 'Apply'
* Go to the 'General' tab and click 'refresh FNDB'
* (Optional), create a new .tex file, and add the following imports:
```tex
\pdfmapfile{=mtpro2.map}	
\usepackage[lite, subscriptcorrection]{mtpro2}
```

