## DBProject


Deployment instructions:

1) Login to nova

2)  Go to delta-tomcat-vm
    ```sh 
    ssh delta-tomcat-vm
    ```

3) Go to your directory with 
    ```sh 
   $ cd specific/scratch/<userName>/django 
    ```
4) Download DBProject
    ```sh 
   $ git clone https://github.com/yahavzar/DBProject.git (or move DBProject from nova with
        $scp -r DBProject delta-tomcat-vm:/specific/scratch/<userName>/django/) 
    $ cd DBProject
    ```    
5) Make the virtual environment
    ```sh 
   $ virtualenv specific/scratch/<userName>/django/DBProject
    ```    
6) Activate the virtual environment
    ```sh 
   $ source specific/scratch/<userName>/django/DBProject/bin/activate.csh
   $ setenv LD_LIBRARY_PATH /usr/local/lib/openssl-1.1.1a/lib
   $ setenv LD_LIBRARY_PATH /usr/local/lib/openssl-1.1.1a/lib:$LD_LIBRARY_PATH
    ```    
7) Install requirements
    ```sh 
    $ pip install --target='/specific/scratch/<userName>/python_package' -r requirements.txt
    $ setenv PYTHONPATH /specific/scratch/<userName>/python_package
    $ cd SRC/APPLICATION_SOURCE_CODE
    ```    
8) Run app.py
    ```sh 
    $ python3 app.py
    ```    
## Notice:  
If you'll be running the app in a local enviorment and not on nova, you'll neeed to go /APPLICATION_SOURCE_CODE/DB/config/mysql_config.json and the host name to 127.0.0.1 and change the port to 3305. Moreover you will have to add to the import prefix 
SRC.APPLICATION_SOURCE_CODE.
This needs to be done for all file within app.py and SRC.APPLICATION_SOURCE_CODE.server
