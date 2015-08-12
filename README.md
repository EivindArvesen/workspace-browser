# Raskolnikov
<!---
Build icons, etc.
-->

![Screenshot](res/small_icon.png)

Raskolnikov is an experimental, task based web browser.

You can think of this as automatically saving a project or workspace (currently open windows and their tabs).

The browser is named after Raksolnikov (of Dostoevsky's Crime and Punishment), since its use is built around schismatization.
It is based on webkit (via the PySide Qt-binding), and programmed in Python.

###Proof of concept
This application is still in a very early, experimental stage,
and neither performance nor stability is up to par at this point.

####Use case
Let us say you are doing research for your thesis, jumping between dozens of open tabs.

When you are done for the day you'd like to look for a new apartment.

* You open the web browsers task-list by clicking the task button in the toolbar,
* open another task by clicking a task title from the list.

This implicitly saves and closes the window(s) and tabs assosiated with the previous task, and opens the saved window(s) and tabs associated with the opened task.

####Justification vis-à-vis alternatives
#####Bookmarks
While most modern browsers are able to bookmark numerous tabs at once (e.g. as a folder), and later reopen them all at once (i.e. the entire folder), this approach of saving "workspaces" requires users to manually add and remove links from saved folders, or alternatively remove the folder and save all tabs again.
#####Leave everything open
Modern browsers generally have the ability to "remember" (reopen) windows and tabs from the previous session on launch.
This approach can result in clutter, many open windows, and potentially performance issues.
#####Task-based approach
Saves a collection of tabs (and windows), reducing both visual clutter and CPU load. Use of this approach also discourages multitasking - cognitive context switching is generally accepted to impede performance - and facilitates the widely used strategy of organizing related tasks in groups.

## Installation
Binaries can be found
### Automatic environment setup
If you don't have Python installed, already have the [Anaconda Python distribution](https://store.continuum.io/cshop/anaconda/) installed or don't have any preference regarding Python distribution, the included `setup.sh` can set up a development environment for you.
Running
```
bash dev/setup.sh
```
will check if the default Anaconda Python path exists, and download and install the latest [miniconda distribution](http://conda.pydata.org/miniconda.html) if it doesn't.
The script then creates a [conda](http://conda.pydata.org/docs/) environment from `requirements.txt`.

To start using the environment, activate it with `source activate browser-dev`.
When you're done, you can deactivate it with `source deactivate browser-dev`.

### Manual environment setup
If you'd like to set up the development manually, the included `requirements.txt` can be used with virtualenv.

With virtualenv, this should go something like
```
pip install -r requirements.txt
```
once you have created and activated an environment.

If you'd like to build the application yourself, you also need to install PyInstaller manually:
```
pip install git+https://github.com/pyinstaller/pyinstaller.git@develop
```

### Contributions
Feedback is very much appreciated.
If you run into a bug or would like to see a new feature, please open a new issue.
Contributions in the form of code (e.g. implementing new features, bug-fixes) are also appreciated.
Just fork the repo, check out a new branch with an informative name, commit your changes and send a pull request.
In the case of any new dependencies, running
```
bash dev/export-env.sh
```
will automatically export your environment and update the requirements-/environment-files (provided you are using a conda env).

## License
This software is released under the terms of the 3-clause New BSD License. See the [license](LICENSE.txt) file for details.

[PySide](https://wiki.qt.io/PySide) is released under [LGPL](https://www.gnu.org/copyleft/lesser.html).
It's source code is available on [GitHub](https://github.com/PySide).

The application icon is built upon [Spectacle Flat Icons](https://dribbble.com/shots/2075892-Spectacle-Flat-Icons) and [The Axe](https://dribbble.com/shots/1702501-The-Axe).
