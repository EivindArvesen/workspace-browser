# Browser Prototype (Raskolnikov)
### Proof of concept
As this codebase has served its purpose of allowing me to experiment with how the desired functionality (task based web browsing) should look, it is no longer under development.

My current focus is to implement an [application that brings task focused functionality to the OS level](https://github.com/eivind88?tab=repositories), and to document task focused computer interaction in a paper.

I will likely reimplement the features this software illustrates as extensions for the major modern browsers.

---

This repo contains code for a prototype (mostly interface) of an experimental, task based web browser. The purpose of it was to illustrate the concept of task based web browsing, and explore GUI design that would facilitate this.

It is probably not useful for anyone else.

### Code
As this is a *rough prototype*, the code is not very pretty.
The entire program (including GUI) is currently implemented in one 600-line python file.
Other glaring weaknesses include the fact that tabs are not implemented using threads (which leads to all sorts of performance and aesthetic issues), persistent tab history is not properly implemented, sidebar status is not synchronized across tabs, window functionality doesn't exist, etc.

### Use
Even though the browser is usable, it is not recommended for usage as a main web browser, as neither performance nor stability is up to par at this point.
Security has _not_ been focused on as of yet, and as a result **the browser can not be considered secure**.

Furthermore, not all browser plugins are available at present - Flash has some trouble, and Java Applets are not supported at all.

This software depends upon PySide.

Currently only supports OS X.


## License
This software is released under the terms of the 3-clause New BSD License. See the [license](LICENSE.txt) file for details.

[PySide](https://wiki.qt.io/PySide) is released under [LGPL](https://www.gnu.org/copyleft/lesser.html).
Its source code is available on [GitHub](https://github.com/PySide).
