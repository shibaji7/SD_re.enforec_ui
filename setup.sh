###
#	Author:         Shibaji Chakraborty
#	Organization:   SuperDARN VT
#	Description:    This shell script is used to get the initial setup for the reenforced learning UI.
###
echo 
echo "***********************************************************************************************************************"
conda create -n reenforce python=3.6 anaconda

echo Environment :: Web Environment
echo Framework :: Django
echo Intended Audience :: SuperDARN 
echo License :: MIT License
echo Programming Language :: Python
echo Programming Language :: Python :: 3.6
echo keywords :: django chart highcharts ajax class based view
echo 

conda install django
pip install django-bootstrap3
django-admin startproject reenforce_ui
cd reenforce_ui 
python manage.py startapp ui
cd ..
while read requirement; do conda install --yes $requirement || pip install $requirement; done < requirements.txt
echo "***********************************************************************************************************************"
