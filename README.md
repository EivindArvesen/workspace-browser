# Raskolnikov
<!--
Build icons, etc.
For instance:
[![travis][travis-image]][travis-url]
[![cc-gpa][cc-gpa-image]][cc-gpa-url]
[![cc-coverage][cc-coverage-image]][cc-coverage-url]
[travis-image]: https://travis-ci.org/ekonstantinidis/gitify.svg?branch=master
[travis-url]: https://travis-ci.org/ekonstantinidis/gitify
[cc-gpa-image]: https://codeclimate.com/github/ekonstantinidis/gitify/badges/gpa.svg
[cc-gpa-url]: https://codeclimate.com/github/ekonstantinidis/gitify
[cc-coverage-image]: https://codeclimate.com/github/ekonstantinidis/gitify/badges/coverage.svg
[cc-coverage-url]: https://codeclimate.com/github/ekonstantinidis/gitify/coverage
-->

![Screenshot](res/small_icon.png)

Raskolnikov is an experimental, task based web browser.

This can be thought of as automatically saving a project or workspace (i.e. currently open windows and their tabs).

The browser is named after Raksolnikov (of Dostoevsky's Crime and Punishment), since its use is built around schismatization.
It is based on webkit (via the PySide Qt-binding), and programmed in Python.

###Proof of concept
The purpose of this application prototype is to illustrate the concept of task based browsing.
While it certainly is usable in its current state, it is not recommended for usage as a main web browser.
Should there be marked interest in the features this software provides, it will likely be reimplemented as extensions for the major modern browsers.

This application is still in a very early, experimental stage,
and neither performance nor stability is up to par at this point.

Security has _not_ been focused on as of yet, and as a result **the browser can not be considered secure**.

Furthermore, not all browser plugins are available at present - Flash has some trouble, and Java Applets are not supported at all.

####Use case
Let us say you are doing research for your thesis, jumping between dozens of open tabs.

When you are done for the day you'd like to look for a new apartment.

* You open the web browser's task-list by clicking the task button in the toolbar, and
* open another task by clicking a task title from the list.

This implicitly saves and closes the window(s) and tabs assosiated with the previous task, and opens the saved window(s) and tabs associated with the clicked task.

####Justification vis-à-vis alternatives
#####Bookmarks
While most modern browsers are able to bookmark numerous tabs at once (e.g. as a folder), and later reopen them all at once (i.e. the entire folder), this approach of saving "workspaces" requires users to manually add and remove links from saved folders, or alternatively remove the folder and save all tabs again.
#####Leave everything open
Modern browsers generally have the ability to "remember" (reopen) windows and tabs from the previous session on launch.
This approach can result in clutter, many open windows, and potentially performance issues.
#####Task-based approach
Saves a collection of tabs (and windows), reducing visual clutter as well as CPU load and RAM usage. Use of this approach also discourages multitasking - cognitive context switching is generally accepted to impede performance - and facilitates the widely used strategy of organizing related tasks in groups.

## Installation
Binaries can be downloaded from the [releases](https://github.com/eivind88/raskolnikov/releases) page.

As Raskolnikov is under rapid development, these may be outdated, and infrequently updated.

Alternatively, you can install Raskolnikov in one of the following ways:

### Automatic environment setup
If you don't have Python installed, already have the [Anaconda Python distribution](https://store.continuum.io/cshop/anaconda/) installed or don't have any preference regarding Python distribution, the included `setup.sh` can set up a development environment for you.
Running

```shell
bash dev/setup.sh
```

will check if the default Anaconda Python path exists, and download and install the latest [miniconda distribution](http://conda.pydata.org/miniconda.html) if it doesn't.
The script then creates a [conda](http://conda.pydata.org/docs/) environment from `requirements.txt`.

To start using the environment, activate it with `source activate raskolnikov-dev`.
When you're done, you can deactivate it with `source deactivate raskolnikov-dev`.

The automatic environment setup script should work for modern 64-bit versions of OS X, Linux and Windows (Cygwin).

### Manual environment setup
If you'd like to set up the development manually, the included `requirements.txt` can be used with virtualenv.

With virtualenv, this should go something like

```shell
pip install -r requirements.txt
```

once you have created and activated an environment.

If you'd like to build the application yourself, you also need to install PyInstaller manually:

```shell
pip install git+https://github.com/pyinstaller/pyinstaller.git@develop
```

### Distribution
To prepare the application for distribution after setting up the development environment, run:

```shell
bash dev/build.sh
```

This script runs PyInstaller on the included ```main.spec```,
and outputs a packaged application in a newly created folder ```dist```.

Currently supports only OS X.

<!--
UPDATE THIS AFTER NOSETESTS ARE WRITTEN!
### Tests
There are 3 types of tests: `jest`, `jscs` and `jsxhint`.
To run the tests:

```shell
npm test
```

-->

## Contributions
Feedback is very much appreciated.

If you run into a bug or would like to see a new feature, please open a new issue.

Contributions in the form of code (e.g. implementing new features, bug-fixes) are also appreciated.
Just fork the repo, check out a new branch with an informative name, commit your changes and send a pull request.

In the case of any new dependencies, running

```shell
bash dev/export-env.sh
```

will automatically export your environment and update the ```requirements.txt``` (provided you are using a conda env).

## License
This software is released under the terms of the 3-clause New BSD License. See the [license](LICENSE.txt) file for details.

[PySide](https://wiki.qt.io/PySide) is released under [LGPL](https://www.gnu.org/copyleft/lesser.html).
Its source code is available on [GitHub](https://github.com/PySide).

The application icon is built upon [Spectacle Flat Icons](https://dribbble.com/shots/2075892-Spectacle-Flat-Icons) and [The Axe](https://dribbble.com/shots/1702501-The-Axe).
