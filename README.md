## DBProject


Deployment instructions:

1) Login to nova

2) ssh delta-tomcat-vm

3) ```sh 
   $cd specific/scratch/<userName>/django 
4) ```sh 
   git clone https://github.com/yahavzar/DBProject.git (or move DBProject from nova with
        scp -r DBProject delta-tomcat-vm:/specific/scratch/<userName>/django/)
        
5)  ```sh 
    cd DBProjet

6) ```sh 
   virtualenv specific/scratch/<userName>/django/DBProject.

7) ```sh 
   source specific/scratch/<userName>/django/DBProject/bin/activate.csh

8)```sh 
 setenv LD_LIBRARY_PATH /usr/local/lib/openssl-1.1.1a/lib

9) ```sh 
   setenv LD_LIBRARY_PATH /usr/local/lib/openssl-1.1.1a/lib:$LD_LIBRARY_PATH

10)```sh 
pip install --target='/specific/scratch/<userName>/python_package' -r requirements.txt

11)```sh 
setenv PYTHONPATH /specific/scratch/<userName>/python_package

12) ```sh 
    cd SRC/APPLICATION_SOURCE_CODE

13)```sh 
 python3 app.py
