#Nammu: Desktop GUI for ORACC


##What is ORACC?
ORACC is the [Open Richly Annotated Cuneiform Corpus](http://oracc.org). 
It provides open-access, standards-based publication platforms, research tools 
and teaching resources for Assyriology and ancient Near Eastern History, 
hosting around 40 academic research projects worldwide. 

ORACC has become established as one of the core online resources in the world 
of ancient Near Eastern studies. It originated in an AHRC-funded research project 
[Prof. Eleanor Robson](https://www.ucl.ac.uk/history/people/academic-staff/eleanor-robson) 
ran at the University of Cambridge several years ago and is now continuing to 
run from University College London in collaboration with University of 
Pennsylvania (Philadelphia).


##What is Nammu?
Nammu is a desktop GUI that enables ORACC content creators to edit, check and 
upload transliterations of Sumerian texts in the form of text files in 
[ASCII Transliteration Format](http://oracc.museum.upenn.edu/doc/help/editinginatf/) 
(ATF). It is being developed as a text editor with extended functionality.

At the time of writing, ORACC content creators use an Emacs plugin for edition,
validation and lemmatisation of ATF files. This plugin can only be installed as 
part of [Emacs](http://oracc.museum.upenn.edu/doc/help/usingemacs/emacssetup/index.html), 
which has a steep learning curve. 

With Nammu, we intend to make a user friendly tool that would replace the use
of the ORACC Emacs plugin. This will help lower the access barriers to the use 
of ORACC, enabling more projects to adopt it.

Nammu is currently being developed by the 
[UCL Research Software Development Group](https://www.ucl.ac.uk/research-it-services/about/research-software-development).

![Nammu](doc/mockups/nammu.png)

## Validation of ATF files

In order to validate ATF files, Nammu uses two approaches:
* Online validation against ORACC server.
* Offline validation using [pyORACC](https://github.com/oracc/pyoracc), the new 
ATF parser developed by UCL RSDT.


#### Validation against the ORACC server
The ORACC server is hosted at University of Pennsylvania (Philadelphia) and 
maintained by [Prof. Steve Tinney](https://www.ling.upenn.edu/people/tinney).
The ORACC server provides with SOAP web services for validation and lemmatisation
of ATF files. Nammu acts as a SOAP client, requesting the server to validate
and lemmatise ATF files, and then presents the server output in the GUI.


#### Validation with pyORACC
Validation against the ORACC server requires the user to have Internet access. 
Since this is not always the case, the UCL RSDG is also developing
an ATF parsing tool to provide with offline initial ATF validation. 
This tool is called pyORACC and you can find more information about it 
[here](https://github.com/oracc/pyoracc).

Nammu uses pyORACC in two different ways:

* Syntax highlighting: This feature allows for users to detect errors while they 
are typing the text. This type of validation helps users check for text 
correctness like spelling errors in keywords, word ordering in each line, etc. 
It won't however highlight errors in the transliterated words, lemmas or translations.
* Offline validation (under development): Users can select to do an offline 
validation using pyORACC when they don't have Internet access. This will return 
error messages coming from pyORACC and presented in the GUI to guide the user 
on how to correct them.


## How to run Nammu

Nammu is being developed in [Jython](http://www.jython.org), an implementation
of the Python language designed to run on the Java platform. 
The installable for Nammu is a JAR file containg Nammu's code as well as all the
necessary Java and Python libraries to run it, like pyORACC, logging, etc.
JAR files can be run in any platform as long as the [Java Virtual Machine](https://en.wikipedia.org/wiki/Java_virtual_machine) 
has been installed. It doesn't require any other extra configuration.

To run Nammu on your computer, you can download the JAR file [here] and just 
double click on it to use it. 

Alternatively, you can also run it from the command line, like this:

`java -jar /path/to/namu.jar`


## Nammu's configuration for advanced users:

#### Nammu's config and logging
The first time Nammu is run, it will create automatically a hidden folder in 
your home directory (`$HOME` in Unix machines and `%USERPROFILE%` in Windows 
machines) called `.nammu`. Alternatively, this folder can be installed elsewhere
by setting a new environment variable called `NAMMU_CONFIG_PATH` that points to 
the desired location where the `.nammu` folder and its contents will be stored.

This folder will contain a log file with debug information output by Nammu and 
a YAML file containing some configuration on how the logging works.

You can see [here](https://github.com/oracc/nammu/blob/development/resources/config/logging.yaml) 
the default logging configuration.


#### Contributors

If you want to contribute to the code, or you want to install and run the code
to customize it instead of just downloading the JAR file, you will first need
to install a few requirements:
* [Maven](https://maven.apache.org), a project management and building
tool for Java. This gathers all the dependencies of the project (e.g. Jython, 
pyORACC, logging, etc.), runs tests, compiles the code in a JAR file, etc.)
* The Java Development Kit (JDK).
* Optionally `git` so you can clone the repo instead of downloading it and 
contribute to it if you like.
 
To obtain the code and run it, you can follow these steps:

1. Clone the repo in your computer:
 `git clone git@github.com:oracc/nammu.git`
2. Download and install the [JDK](http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html).
3. Download and install [Maven](https://maven.apache.org) following instructions.
4. Run the following Maven command to install the project and clean the output 
from previous executions:
 ```
 mvn clean install
 ```
5. This will create Nammu's jar in the `target` folder. Then you can execute it
like this:
 ```
 java -jar  target/original-nammu-0.0.1-SNAPSHOT.jar 
 ```

If you find any problem or need more information, you can create an issue 
[here](https://github.com/oracc/nammu/issues).


## Links of interest

* [ORACC](http://oracc.museum.upenn.edu)'s official website.
* The ORACC [project list](http://oracc.museum.upenn.edu/projectlist.html).
* [ORACC's help](http://oracc.museum.upenn.edu/doc/help/visitingoracc/index.html).
* [ORACC at GitHub](https://github.com/oracc).
* [Slides](http://slides.com/raquelalegre/oracc-7#/) for seminar about ORACC 
and UCL RSDG collaboration at UCL Digital Humanities (27th April 2016)
