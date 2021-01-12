#DBProject


Deployment instructions:
1) Login to nova
2) ssh delta-tomcat-vm
3) cd specific/scratch/<userName>/django
4) git clone https://github.com/yahavzar/DBProject.git (or move DBProject from nova with
scp -r DBProject delta-tomcat-vm:/specific/scratch/<userName>/django/)
5) cd DBProjet
6) virtualenv specific/scratch/<userName>/django/DBProject.
7) source specific/scratch/<userName>/django/DBProject/bin/activate.csh
8) setenv LD_LIBRARY_PATH /usr/local/lib/openssl-1.1.1a/lib
9) setenv LD_LIBRARY_PATH /usr/local/lib/openssl-1.1.1a/lib:$LD_LIBRARY_PATH
10)pip install --target='/specific/scratch/<userName>/python_package' -r requirements.txt
11)setenv PYTHONPATH /specific/scratch/<userName>/python_package
12) cd SRC/APPLICATION_SOURCE_CODE
13) python3 app.py
