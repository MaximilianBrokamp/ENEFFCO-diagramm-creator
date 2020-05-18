
#change stdout and error output to lofgile for debugging purposes
#logfile=Logfile.log
#exec > $logfile 2>&1

#pauses the script until the user presses any button
function pause(){
echo -e "\e[39m"
read -s -n 1 -p "Press any key to close the terminal"
}

function installation_failed() {
	echo -e "\e[31mFATAL ERROR: Installation Failed"
	echo -e "\e[31mERROR: $1"
	pause
	exit
}

function installation_succeded() {
	echo -e "\e[32mINSTALLATION SUCCESSFULL: python and all packages are installed"
	echo "You can now Start the program"
	pause
	exit
}
echo "Bash version ${BASH_VERSION}..."

#check for python verion
#if it's not installed or the verion is >3.x the script will return a FATAL ERROR and terminate
python_version=$(python --version)
echo "$python_version"
if [[ $python_version = *"Python 3."* ]]; then
	echo "INFO: correct python version found"
else
	
	message=$'no correct python version found \nmake sure python 3 is installed and set as standard version of python on this computer'
	installation_failed "$message"
fi

#check if pip is installed
#if not the script will retrun a FATAL ERROR and terminate
pip_version=$(python -m pip --version)
echo "$pip_version"
if [[ $pip_version = *"pip"*"(python 3."* ]]; then
	echo "INFO: correct pip version found"
else
	
	message=$'no correct pip version found \n make sure pip is installed and the it is the correct version for the installed python version'
	installation_failed "$message"
fi

#check if the necessary packages are already installed
selenium=false
pynput=false
installed_packages=$(pip list)
for i in "${installed_packages[@]}"
do
	if [[ $i = *"selenium"* ]]; then
		echo "INFO: slenenium package already installed"
		selenium=true
	fi
	if [[ $i = *"pynput"* ]]; then
		echo "INFO: pynput package already installed"
		pynput=true
	fi
done

#if the selenium package wasn't found in the package list the script will install it
#Is the installation was successfull it will output these and continue
#When the insatllation failes it will return an error and call the installation_failed function
if  ! $selenium; then
	echo "INFO: selenium package NOT found \n will be installed now"
	pynput_install=$(python -m pip install selenium)
	if [[ $pynput_install = *"ERROR"* ]]; then
			message=$'could not install selenium \n, try again or install the package manually';
			installation_failed "$message";
	else
		echo "Successfully Installed selenium";
	fi
fi

#if the pynput package wasn't found in the package list the script will install it
#Is the installation was successfull it will output these and continue
#When the insatllation failes it will return an error and call the installation_failed function
if ! $pynput; then
	echo $'INFO: pynput package NOT found, will be installed now'
	pynput_install=$(python -m pip install pynput)
	if [[ $pynput_install = *"ERROR"* ]]; then
		echo "$pynput_install"
		message=$'could not install pynput, \ntry again or install the package manually';
		installation_failed "$message";
	else
		echo "Successfully Installed pynput";
	fi
fi
 
#check if all necessary files exit
#currently not working

#cd code
#return_value=$(python -c "import check_all_files; return_value=check_all_files.check_all_files(); exit(return_value)")
#cd ..

#echo "${return_value}"
#if [[ $return_value = *"True"* ]]; then
#	echo "INFO: all necessary files are available";
#else
#	message=$'could not find all files'
#	installation_failed "$message";
#fi

installation_succeded



















