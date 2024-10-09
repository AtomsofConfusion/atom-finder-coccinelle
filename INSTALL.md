### Installation Guide
1. Make sure coccinelle is installed on the system. For more information, please refer to this link
https://github.com/coccinelle/coccinelle/blob/master/install.txt

2. Run the following command to build the command line tool.
    > export PYTHONPATH=$PYTHONPATH:$(pwd) 
    > pip install .

3. To verify the build is successful, try calling it.
    > atom-finder-coccinelle