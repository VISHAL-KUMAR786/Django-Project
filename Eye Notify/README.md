
# Eye Notify

This python app will help to Notify, when you have to relax you after a paritcular time interval.




## Authors

- [@Vishal-kumar786](https://github.com/VISHAL-KUMAR786)


## Appendix

use this command if you have change something in eye.py , According to you need . Then you have to delete all other file except eye.py.

Right click on that particular folder where eye.py is located type this command to build extecutable file 

👉🏻 pyinstaller -F -w eye.py --hidden-import plyer.platforms.win.notification  

you have to ensure that window Antimalware Service Executable is not deleting the exe file when it is run.

If you are facing problem that after running it is automatically get deleted , for this 

use 2 image give in folder as refrence for solution
## 🚀 About Me
I'm a full stack developer ...
## Installation

Install my-project with python version 3.10
```bash
    run eye.exe file on dist folder
```

In case you have change eye.py, then you have to recompile 
```bash
pyinstaller -F -w eye.py --hidden-import plyer.platforms.win.notification
```
    