#!/usr/bin/python2
# -*- coding: utf-8 -*-

"""
TODO:
- Menubar
- Custom startpage (look like duckduckgo, built upon custom page, use small_icon for logo and colors)
- For tab-index: pickle(history) in(task/folder/index.pickle)
- Modularization
- Task view; save/load, etc.
- Read paper (http://www.informationr.net/ir/17-4/paper547.html#.VcnnrXg6mvs)
- Read slides (http://www.slideshare.net/mohanrajrm/a-taskfocused-approach-to-support-sharing-and-interruption-recovery-in-web-browsers)
- Search page for text (http://stackoverflow.com/questions/26912152/search-text-and-scroll-down-with-qwebview)
- Detach tabs, turn into separate windows (http://stackoverflow.com/questions/14872763/how-to-pop-out-a-separate-window-from-a-tabwidget-in-pyside-qt)
- Drag tabs between windows
- URL text align center on focus, left else (https://srinikom.github.io/pyside-docs/PySide/QtGui/QLineEdit.html#PySide.QtGui.PySide.QtGui.QLineEdit.setAlignment)
- Swiping gestures back and forth
- url completion from history (log)
- autocompletion for omnibar google search
- Settings (https://deptinfo-ensip.univ-poitiers.fr/ENS/pyside-docs/PySide/QtWebKit/QWebSettings.html#PySide.QtWebKit.PySide.QtWebKit.QWebSettings.WebAttribute)
- Holding click on back/forward should bring up dropdown-menu (tab history)
- Most Recently Used tab order/switching?
- Unit tests (nose)
"""

import os
import pickle
import signal
import sys
import tempfile
# import just what is needed
from PySide.QtCore import Qt, SLOT, QUrl
from PySide.QtGui import QApplication, QWidget, QMainWindow, QHBoxLayout
from PySide.QtGui import QLineEdit, QPushButton, QVBoxLayout, QKeySequence
from PySide.QtGui import QShortcut, QTabWidget, QMenuBar, QFont, QProgressBar
from PySide.QtGui import QIcon, QStyleFactory, QFrame
from PySide.QtWebKit import QWebView, QWebSettings, QWebInspector

homedir = os.path.expanduser('~')
if getattr(sys, 'frozen', False):
    # we are running in a |PyInstaller| bundle
    os.chdir(homedir)
    basedir = sys._MEIPASS
    sys.stdout = tempfile.TemporaryFile()
    sys.stderr = tempfile.TemporaryFile()
else:
    # we are running in a normal Python environment
    basedir = os.path.dirname(__file__)

bookFile = os.path.join(homedir, "bookmarks.txt")
try:
    b = open(bookFile,"rb")
    bookmarks = pickle.loads(b.read())
    b.close()
except Exception, e:
    #print e
    file = open(bookFile, "w")
    for line in '':
       file.write(line)
    file.close()
    bookmarks = ''

class window(QMainWindow):

    """Main window."""

    def __init__(self, parent=None):
        """Initialize the parent class of this instance."""
        super(window, self).__init__(parent)
        app.aboutToQuit.connect(self.myExitHandler)

        style_sheet = self.styleSheet('style')
        #app.setStyle(QStyleFactory.create('Macintosh'))
        #app.setStyleSheet(style_sheet)

        self.startpage = "https://duckduckgo.com/"
        self.new_tab_behavior = "insert"
        global bookmarks

        global menubar
        menubar = QMenuBar()

        # Initialize a statusbar for the window
        self.statusbar = self.statusBar()
        self.statusbar.setFont(QFont("Helvetica Neue", 11, QFont.Normal));
        self.statusbar.setStyleSheet(style_sheet)
        self.statusbar.setMinimumHeight(15)

        self.pbar = QProgressBar()
        self.pbar.setMaximumWidth(100)
        self.statusbar.addPermanentWidget(self.pbar)

        self.statusbar.hide()

        self.setMinimumSize(504, 235)
        self.setWindowTitle("Raskolnikov")
        self.setWindowIcon(QIcon(""))

        # Create input widgets
        self.bbutton = QPushButton("<")
        self.fbutton = QPushButton(">")
        self.hbutton = QPushButton(u"⌂")
        self.edit = QLineEdit("")
        self.edit.setFont(QFont("Helvetica Neue", 12, QFont.Normal));
        self.edit.setPlaceholderText("Enter URL")
        #self.edit.setMinimumSize(400, 24)
        self.rbutton = QPushButton(u"↻")
        self.dbutton = QPushButton(u"☆")
        self.nbutton = QPushButton(u"+")

        self.edit.setTextMargins(2, 1, 2, 0)

        # create a horizontal layout for the input
        input_layout = QHBoxLayout()
        input_layout.setSpacing(4)
        input_layout.setContentsMargins(0, 8, 0, 0)

        # add the input widgets to the input layout
        input_layout.addWidget(self.bbutton)
        input_layout.addWidget(self.fbutton)
        input_layout.addWidget(self.hbutton)
        input_layout.addWidget(self.edit)
        input_layout.addWidget(self.rbutton)
        input_layout.addWidget(self.dbutton)
        input_layout.addWidget(self.nbutton)

        # create a widget to hold the input layout
        self.input_widget = QFrame()
        self.input_widget.setObjectName("InputWidget")
        self.input_widget.setStyleSheet(style_sheet)

        # set the layout of the widget
        self.input_widget.setLayout(input_layout)
        self.input_widget.setVisible(True)

        # CREATE BOOKMARK-LINE HERE

        # create tabs
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.new_tab()

        tabs_layout = QHBoxLayout()
        tabs_layout.setSpacing(0)
        tabs_layout.setContentsMargins(0, 0, 0, 0)
        tabs_layout.addWidget(self.tabs)

        self.tabs_widget = QFrame()
        self.tabs_widget.setObjectName("TabLine")
        self.tabs_widget.setStyleSheet(style_sheet)
        self.tabs_widget.setLayout(tabs_layout)
        self.tabs_widget.setVisible(True)

        gsettings = self.tabs.currentWidget().settings().globalSettings()
        gsettings.setAttribute(QWebSettings.DeveloperExtrasEnabled, True)
        gsettings.setAttribute(QWebSettings.AcceleratedCompositingEnabled, True)

        self.inspector = QWebInspector(self)
        self.inspector.setPage(self.tabs.currentWidget().page())
        self.inspector.hide()

        # Create a vertical layout and add widgets
        vlayout = QVBoxLayout()
        vlayout.setSpacing(0)
        vlayout.setContentsMargins(0, 0, 0, 0)
        vlayout.addWidget(self.input_widget)
        vlayout.addWidget(self.tabs_widget, 1)
        vlayout.addWidget(self.inspector)

        # create a widget to hold the vertical layout
        wrapper_widget = QWidget()
        wrapper_widget.setLayout(vlayout)
        self.setCentralWidget(wrapper_widget)

        self.bbutton.clicked.connect(self.tabs.currentWidget().back)
        self.fbutton.clicked.connect(self.tabs.currentWidget().forward)
        self.hbutton.clicked.connect(self.goHome)
        self.edit.returnPressed.connect(self.set_url)
        # Add button signal to "go" slot
        self.rbutton.clicked.connect(self.tabs.currentWidget().reload)
        self.dbutton.clicked.connect(self.bookmark)
        self.nbutton.clicked.connect(self.new_tab)
        self.tabs.tabCloseRequested.connect(self.tabs.removeTab)
        self.tabs.currentChanged.connect(self.change_tab)

        widgets = (input_layout.itemAt(i).widget() for i in range(input_layout.count()))
        for widget in widgets:
            if isinstance(widget, QPushButton):
                widget.setFixedSize(33, 21)
                widget.setFont(QFont("Helvetica Neue", 12, QFont.Normal))
                widget.pressed.connect(self.press_button)
                widget.released.connect(self.release_button)

        # make a ctrl+q quit
        sequence = QKeySequence(Qt.CTRL + Qt.Key_Q)
        QShortcut(sequence, self, SLOT("close()"))

        # make an accelerator to toggle fullscreen
        sequence = QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_F)
        QShortcut(sequence, self, self.toggle_fullscreen)

        # make an accelerator to toggle input visibility
        sequence = QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_L)
        QShortcut(sequence, self, self.toggle_input)

        # make an accelerator to focus adress-bar
        sequence = QKeySequence(Qt.CTRL + Qt.Key_L)
        QShortcut(sequence, self, self.focus_adress)

        # make an accelerator to reload page
        sequence = QKeySequence(Qt.CTRL + Qt.Key_R)
        QShortcut(sequence, self, self.tabs.currentWidget().reload)

        # make an accelerator to create new tab
        sequence = QKeySequence(Qt.CTRL + Qt.Key_T)
        QShortcut(sequence, self, self.new_tab)

        # make an accelerator to close tab
        sequence = QKeySequence(Qt.CTRL + Qt.Key_W)
        QShortcut(sequence, self, self.close_tab)

        # make an accelerator to navigate tabs
        sequence = QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_Left)
        QShortcut(sequence, self, self.previous_tab)
        sequence = QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_Right)
        QShortcut(sequence, self, self.next_tab)

        # make an accelerator to toggle inspector
        sequence = QKeySequence(Qt.CTRL + Qt.ALT + Qt.Key_U)
        QShortcut(sequence, self, self.handleShowInspector)

        # update view on page change
        self.tabs.currentWidget().loadStarted.connect(self.load_start)
        self.tabs.currentWidget().loadFinished.connect(self.load_finish)

        self.tabs.currentWidget().loadProgress.connect(self.pbar.setValue)
        self.tabs.currentWidget().page().linkHovered.connect(self.linkHover)

        # finally set the attribute need to rotate
        #try:
        #    self.setAttribute(Qt.WA_Maemo5AutoOrientation, True)
        #except:
        #    print "not maemo"

        self.statusbar.show()

    def press_button(self):
        self.sender().setStyleSheet('background-color: rgba(228, 228, 228)')

    def release_button(self):
        self.sender().setStyleSheet('background-color: rgba(252, 252, 252)')

    def goHome(self):
        self.tabs.currentWidget().setUrl(QUrl(self.startpage))

    def handleShowInspector(self):
        self.inspector.setShown(self.inspector.isHidden())

    def focus_adress(self):
        """Focus adress bar."""
        self.edit.selectAll()
        self.edit.setFocus()

    def toggle_input(self):
        """Toggle toolbar visibility."""
        if self.input_widget.isVisible():
            visible = False
        else:
            visible = True
        self.input_widget.setVisible(visible)

    def toggle_fullscreen(self):
        """Toggle fullscreen."""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def linkHover(self, l):
        self.statusbar.showMessage(l)

    def bookmark(self):
        pass

    def new_tab(self):
        """Open new tab."""
        tab = QWebView()
        tab.load(QUrl(self.startpage))
        self.tabs.setUpdatesEnabled(False)
        if self.new_tab_behavior == "insert":
            self.tabs.insertTab(self.tabs.currentIndex()+1, tab,
                                unicode(tab.title()))
        elif self.new_tab_behavior == "append":
            self.tabs.appendTab(tab, unicode(tab.title()))
        self.tabs.setCurrentWidget(tab)
        self.tabs.setUpdatesEnabled(True)
        tab.titleChanged.connect(self.change_tab)
        tab.urlChanged.connect(self.change_tab)

    def change_tab(self):
        """Change active tab."""
        if self.tabs.count()<=1:
            self.tabs.tabBar().hide();
        else:
            self.tabs.tabBar().show();

        try:
            self.edit.setText(str(self.tabs.currentWidget().url().toEncoded()))
            self.tabs.setTabText(self.tabs.currentIndex(),
                                 unicode(self.tabs.currentWidget().title()))
            self.tabs.currentWidget().setFocus()
        except Exception, e:
            #print e
            self.tabs.tabBar().hide();
            self.new_tab()

    def previous_tab(self):
        """Previous tab."""
        try:
            self.tabs.setCurrentIndex(self.tabs.currentIndex()-1)
            self.change_tab()
        except Exception, e:
            pass
            #print str(e)

    def next_tab(self):
        """Next tab."""
        try:
            self.tabs.setCurrentIndex(self.tabs.currentIndex()+1)
            self.change_tab()
        except Exception, e:
            pass
            #print str(e)

    def close_tab(self):
        """Close tab."""
        self.tabs.removeTab(self.tabs.currentIndex())

    def close(self):
        """Close app."""
        Qapplication.quit()

    def set_url(self):
        """Set url."""
        url = self.edit.text()
        # does the url start with http://?
        if "." not in url:
            url = "http://www.google.com/search?q="+url
        elif not url.startswith("http://"):
            url = "http://" + url
        qurl = QUrl(url)
        self.tabs.currentWidget().load(qurl)
        self.tabs.currentWidget().setFocus()

    def load_start(self):
        """Update view values, called upon started page load."""
        self.rbutton.setText(u"╳")
        self.rbutton.clicked.connect(self.tabs.currentWidget().stop)
        self.pbar.show()

    def load_finish(self):
        """Update view values, called upon finished page load."""
        if (self.tabs.currentWidget().history().canGoBack()):
            self.bbutton.setEnabled(True)
        else:
            self.bbutton.setEnabled(False)
        if (self.tabs.currentWidget().history().canGoForward()):
            self.fbutton.setEnabled(True)
        else:
            self.fbutton.setEnabled(False)

        self.rbutton.setText(u"↻")
        self.rbutton.clicked.connect(self.tabs.currentWidget().reload)
        self.pbar.hide()

    def styleSheet(self, style_sheet):
        """Load stylesheet."""
        try:
            with open(os.path.join(basedir, 'assets', 'style.qss'), 'r') as file:
                return file.read()
        except Exception, e:
            # print e
            return ''

    def myExitHandler(self):
        """Exiting."""
        pass
        #print 'Current:', self.tabs.currentIndex(), unicode(self.tabs.currentWidget().title()), self.tabs.currentWidget().url().toEncoded()
        #for tab in range(self.tabs.count()):
            #print 'Tab:', tab, unicode(self.tabs.widget(tab).title()), self.tabs.widget(tab).url().toEncoded()
                #for item in self.tabs.widget(tab).history().items():
                #    #print item.title(), item.url().toEncoded()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    window = window()
    window.show()
    window.raise_()
    # Run the main Qt loop
    sys.exit(app.exec_())
