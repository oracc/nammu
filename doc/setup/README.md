# Setting up a new development environment

This directory has information on how to set up an environment to contribute to
the development of Nammu. This is illustrated by setting up a virtual machine
(VM), as this is a simple way of ensuring a clean environment, but similar
steps (as described in the `provision.sh` script) can also be followed in
different setups.

## Instructions
1. Install Vagrant (https://www.vagrantup.com/intro/getting-started/install.html)
and VirtualBox.
1. Get a copy of the Nammu source (`git clone https://github.com/oracc/nammu.git`)
(you probably already have this!).
1. Download the Jython installer (http://www.jython.org/downloads.html).
1. Put the `Vagrantfile` and the `provision.sh` script at the same location where
the Nammu source and the Jython installer are.
1. Run `vagrant up`. This will create a new VM and install all requirements.
1. Run `vagrant ssh` to connect to a terminal in the VM.
1. You can now delete the Jython installer if you want.

For further details of how to run Nammu from this setup, see
https://github.com/oracc/nammu/wiki/Run-Nammu-from-a-console.

## Details
A few more details about the process, should you need them...
### Preparing the VM
The provided `Vagrantfile` has a simple description of an Ubuntu VM and how to
create it. In addition to the default settings, we also ask to enable X forwarding.
This is necessary so that you can see Nammu when you run it from inside the VM.

Everything in the directory where the `Vagrantfile` is located will be shared
with the VM. By default, it is available under `/vagrant` from inside the VM,
and it will be kept synchronised between the VM and the host machine. This is
why the instructions above ask you to put all files in the same location. This
also means that any changes you make in the Nammu source (in that same directory)
will be reflected inside the VM, so you can launch Nammu with your changed code.

### Provisioning (setup)
After the bare VM is created, a series of instructions will be run to set it up.
These are contained in the `provision.sh` shell script, and have two main steps:

- Installing the necessary dependencies (Java, Jython, various Python packages)
- Creating and moving the relevant resources to where Jython can find them, and
setting up the path appropriately

If not using a VM, you can adjust these instructions to your own environment.
