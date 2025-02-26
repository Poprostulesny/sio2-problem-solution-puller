How to use:

Requirements:
1. Python libraries:
    -selenium
    -json
    -config
    -base64
2. Microsoft Edge webdrivers https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver?form=MA13LH


Other noteworthy things:
1. If the program gives an error that a given file doesn't exist, then adjusting time limit in 227 line in utils.py might help, as the time that a previous command requires varies with internet speed and computer speed
2. It is possible to use Chrome instead of Edge with tweaks at lines 17 and 26 in main.py
  
  
Quick guide:
1. In file config.py you need to set your login, password, and directories to which you want to download all of the files
2. There is a place where you can add links to other sio2 based websites but only the given one was tested
