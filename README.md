# Nammu: Desktop GUI for ORACC

To run Nammu on your computer, you can download it from
[here](https://github.com/oracc/nammu/releases/download/1.2.1/nammu-1.2.1.jar)
and just double click on it to open it.

## What is ORACC?
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


## What is Nammu?
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

<img src="./doc/mockups/nammu_1.2.png" align="center" width="90%">


## Validation and lemmatisation of ATF files

In order to validate ATF files, Nammu uses two approaches:
* Online validation against ORACC server, configurable on the settings menu.
* Offline validation using [pyORACC](https://github.com/oracc/pyoracc), the new
ATF parser developed by UCL RSDT.

Lemmatisation can only be done online with the ORACC server.


#### Validation and lemmatisation against the ORACC server
The ORACC server is hosted at University of Pennsylvania (Philadelphia) and
maintained by [Prof. Steve Tinney](https://www.ling.upenn.edu/people/tinney).
The ORACC server provides SOAP web services for validation and lemmatisation
of ATF files. Nammu acts as a SOAP client, requesting the server to validate
and lemmatise ATF files, and then presents the server output in the GUI.


#### Validation with pyORACC
Validation against the ORACC server requires the user to have Internet access.
Since this is not always the case, the UCL RSDG is also developing
an ATF parsing tool to provide offline initial ATF validation.
This tool is called pyORACC and you can find more information about it
[here](https://github.com/oracc/pyoracc).

Nammu uses pyORACC in two different ways:

* __Syntax highlighting__: This feature allows for users to detect errors while they
are typing the text. This type of validation helps users check for text
correctness like spelling errors in keywords, word ordering in each line, etc.
It won't however highlight errors in the transliterated words, lemmas or translations.
* __Offline validation__ (under development): Users can select to do an offline
validation using pyORACC when they don't have Internet access. This will return
error messages coming from pyORACC and presented in the GUI to guide the user
on how to correct them.

#### Right to left translation support

<img src="./doc/mockups/nammu_arabic.png" align="center" width="90%">

As part of the [Nahrein project](http://www.ucl.ac.uk/nahrein), Nammu has been extended to support Arabic, Farsi and Kurdish translation languages. This is enabled through the creation of an Arabic Translation pane, which opens automatically on valid ATF files which contain an Arabic, Kurdish or Farsi translation line, such as:

```
@translation parallel ar project
```

If editing a new file which does not yet have a translation, this mode can be activated using the `Window` menu, which contains an option `Toggle Arabic Translation Editor` which will enable or disable the translation pane.

This feature is still a work in progress so please open an [issue](https://github.com/oracc/nammu/issues/new) and let us know if you have any problems.

## How to run Nammu

To run Nammu on your computer, you can download it from
[here](https://github.com/oracc/nammu/releases/download/1.2.1/nammu-1.2.1.jar)
and just double click on it to open it and use it.

If you find any problem trying to open it, have a look in the [Troubleshooting](#known-problems-and-troubleshooting) section.

## Default keystrokes

There's a set of default keystrokes for all actions that can be done with Nammu:

| Action | Keystroke |
|--|--|
|New File| Ctrl/Cmd + N|
|Open File| Ctrl/Cmd + O|
|Close File| Ctrl/Cmd + W|
|Save As | Ctrl/Cmd + E|
|Save File| Ctrl/Cmd + S|
|Validate| Ctrl/Cmd + D|
|Lemmatise|Ctrl/Cmd + L|
|Undo| Ctrl/Cmd + Z|
|Redo| Ctrl/Cmd + Y|
|Find| Ctrl/Cmd + F|
|Find next| Ctrl/Cmd + G |
|Replace all | Ctrl/Cmd + A|
|Replace one | Ctrl/Cmd + R|
|Show Help| Ctrl/Cmd + H|
|Split Editor Horizontally| Ctrl/Cmd + .|
|Split Editor Vertically| Ctrl/Cmd + ;|
|Syntax Highlight Switch| Ctrl/Cmd + T|


These are in your settings file and will be editable from the settings menu on a later release.


## Getting help
If you run into trouble, or have any questions or suggestions, you can get in
touch with Nammu's developers by creating a new issue in this repository and
telling us about your problem [here](https://github.com/oracc/nammu/issues/new).

Please follow the guidelines to help us better understand and reproduce your
problem.

## Known problems and troubleshooting
If you try to open Nammu and it doesn't work, it might be that you don't have
Java installed. You can check if you do by opening a terminal and typing:

`java`

If that command is not recognised, then you'll need to download and install
the Java Runtime Environment (JRE). You can find the appropriate JRE
installable file for your operating system
[here](http://www.oracle.com/technetwork/java/javase/downloads/jre8-downloads-2133155.html).

If you keep having trouble, you can also run it from the command line, like this:

`java -jar /path/to/nammu-1.2.1.jar`

Where `/path/to/` reflects your local path to where the `nammu-1.2.1.jar` file has been downloaded. This will output a clearer log message about what the problem is.

### Known problems:
* Nammu doesn't validate or lemmatise properly when filenames include a space.

A full list of issues can be found [here](https://github.com/oracc/nammu/issues).

If you have any other suggestions, new features you'd like us to work on, or
any other comment, please let us know by creating a new issue [here](https://github.com/oracc/nammu/issues/new).


## Nammu's configuration for advanced users:

#### Nammu's config and logging
The first time Nammu is run, it will create automatically a hidden folder in
your home directory (`$HOME` in Unix machines and `%USERPROFILE%` in Windows
machines) called `.nammu`. Alternatively, this folder can be installed elsewhere
by setting a new environment variable called `NAMMU_CONFIG_PATH` that points to
the desired location where the `.nammu` folder and its contents will be stored.

This folder will contain a log file with debug information output by Nammu and
a [YAML file](https://github.com/oracc/nammu/blob/master/resources/config/logging.yaml)
containing some configuration on how the logging works.

You can see [here](https://github.com/oracc/nammu/blob/development/resources/config/logging.yaml)
the default logging configuration.

There is also [a configuration file](https://github.com/oracc/nammu/blob/master/resources/config/settings.yaml)
for shortcuts, preferred working directory, preferred list of ORACC projects,
etc. This will be fully editable from Nammu, but for now only working directory
and lemmatisation server can be edited from the settings window.


#### Notes on Nammu's software development

Nammu is being developed in [Jython](http://www.jython.org), an
implementation of the Python language designed to run on the Java platform.
The installable for Nammu is a JAR file containing Nammu's code as well as all
the necessary Java and Python libraries to run it, like pyORACC, logging, etc.

JAR files can be run in any platform as long as the
[Java Virtual Machine](https://en.wikipedia.org/wiki/Java_virtual_machine)
has been installed. It doesn't require any other extra configuration.

### Requirements

Nammu is developed and tested on Java 8. The new release of Nammu (1.2.1) now supports Java versions 9 and 10. If you encounter problems running Nammu on these versions, please let us know by filing an issue.

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
    ```
    git clone git@github.com:oracc/nammu.git
    ```    
1. Install requirements:
    ```bash
    cd nammu
    pip install -r requirements.txt
    ```
1. Run tests from nammu's root folder. These check the Oracc's server
functionality needed by Nammu for validation and lemmatisation, as well as use
cases related to Nammu's Arabic translation mode. More tests will be added
before the next release.
    ```bash
    py.test ./python/nammu
    ````
1. Download and install the [JDK](http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html).
1. Download and install [Maven](https://maven.apache.org) following instructions.
1. Run the following Maven command to install the project and clean the output
from previous executions, skipping tests which can be run separately from the
build as indicated in step 3:
    ```bash
    mvn clean install -DskipTests
    ```
1. This will create Nammu's jar in the `target` folder. Then you can execute it
like this:
    ```bash
    java -jar  target/nammu-1.2.1.jar
    ```
1. You can also run Nammu in development mode from the console. See instructions:
https://github.com/oracc/nammu/wiki/Running-Nammu-from-a-console

If you find any problem, need more information or would like to contribute, you
can create an issue [here](https://github.com/oracc/nammu/issues).


## License

Nammu is free software and has been licensed under the GNU General Public
License. You can read the full license text
[here](https://www.gnu.org/licenses/gpl-3.0.en.html).

If you want to reuse Nammu's code and have any concerns about the implications
of this license, please get in touch with us at `rc-softdev` (at) `ucl.ac.uk`.


## Links of interest

* [Blog post about Nammu](http://oracc.blogspot.co.uk/2016/07/editing-atf-with-nammu.html)
by Prof. Eleanor Robson.
* [ORACC](http://oracc.museum.upenn.edu)'s official website.
* The ORACC [project list](http://oracc.museum.upenn.edu/projectlist.html).
* [ORACC's help](http://oracc.museum.upenn.edu/doc/help/visitingoracc/index.html).
* [ORACC at GitHub](https://github.com/oracc).
* [Slides](http://slides.com/raquelalegre/oracc-7#/) for seminar about ORACC
and UCL RSDG collaboration at UCL Digital Humanities (27th April 2016)
