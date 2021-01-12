## DBProject


Deployment instructions:

1) Login to nova

2) ssh delta-tomcat-vm

3) move to your directory with 
    ```sh 
   $cd specific/scratch/<userName>/django 
    ```
4) Download DBProject
    ```sh 
   $git clone https://github.com/yahavzar/DBProject.git (or move DBProject from nova with
        $scp -r DBProject delta-tomcat-vm:/specific/scratch/<userName>/django/) 
    $cd DBProjet
    ```    
5) Make the virtual environment
    ```sh 
   $virtualenv specific/scratch/<userName>/django/DBProject.
    ```    
6) Activate the virtual environment
    ```sh 
   $source specific/scratch/<userName>/django/DBProject/bin/activate.csh
   $setenv LD_LIBRARY_PATH /usr/local/lib/openssl-1.1.1a/lib
   $setenv LD_LIBRARY_PATH /usr/local/lib/openssl-1.1.1a/lib:$LD_LIBRARY_PATH
    ```    
7) Install requirements
    ```sh 
    $pip install --target='/specific/scratch/<userName>/python_package' -r requirements.txt
    $setenv PYTHONPATH /specific/scratch/<userName>/python_package
    ```    
8) 
    ```sh 
    $cd SRC/APPLICATION_SOURCE_CODE
    ```    
9) Run app.py
    ```sh 
    $python3 app.py
    ```    