# Instructions to run the first time the VM is created only!
# Rerunning this could break (in particular, you'll need to delete the
# jython directory if it has already been created, and maybe other things...)

# Before running this, you need to download two things into this directory:
# 1. Nammu source (git clone https://github.com/oracc/nammu.git)
# 2. Jython installer (from http://www.jython.org/downloads.html)
# This directory will be available within the VM at /vagrant

# Install Java (1.8) and Jython
sudo apt-get update && sudo apt-get install --assume-yes default-jdk
java -jar /vagrant/jython-installer-2.7.0.jar -s -d /vagrant/jython
export PATH=/vagrant/jython/bin:$PATH  # required for pip
echo "export PATH=/vagrant/jython/bin:$PATH" >> .bashrc

# Install the Python requirements for Nammu
pip install -r /vagrant/nammu/requirements.txt

# Compile the extra classes we need and tell Jython where to find them
mkdir -p /vagrant/nammu/resources/lib
javac -d /vagrant/nammu/resources/lib /vagrant/nammu/src/main/java/uk/ac/ucl/rc/development/oracc/ext/*.java
echo "export JYTHONPATH=/vagrant/nammu/resources/lib" >> .bashrc

# For more instructions on what to do next, see:
# https://github.com/oracc/nammu/wiki/Run-Nammu-from-a-console
