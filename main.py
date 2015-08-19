#!/usr/bin/python2
# -*- coding: utf-8 -*-

import os
import cPickle as pickle
import signal
import sys
import tempfile
# import just what is needed
from PySide.QtCore import Qt, SLOT, QUrl, QSettings
from PySide.QtGui import QApplication, QWidget, QMainWindow, QHBoxLayout
from PySide.QtGui import QLineEdit, QPushButton, QVBoxLayout, QKeySequence
from PySide.QtGui import QShortcut, QTabWidget, QMenuBar, QFont, QProgressBar
from PySide.QtGui import QIcon, QFrame, QDesktopServices
from PySide.QtGui import QSizePolicy, QTreeView, QStandardItemModel
from PySide.QtGui import QStandardItem, QToolButton, QAction
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

tabFile = os.path.join(homedir, "saved_tabs.p")
try:
    b = open(tabFile, "rb")
    saved_tabs = pickle.loads(b.read())
    b.close()
except Exception, e:
    # print e
    file = open(tabFile, "w")
    for line in '':
        file.write(line)
    file.close()
    saved_tabs = ''

bookFile = os.path.join(homedir, "bookmarks.p")
try:
    c = open(bookFile, "rb")
    bookmarks = pickle.loads(c.read())
    c.close()
except Exception, e:
    print e
    file = open(bookFile, "w")
    for line in '':
        file.write(line)
    file.close()
    bookmarks = []

class window(QMainWindow):

    """Main window."""

    def __init__(self, parent=None):
        """Initialize the parent class of this instance."""
        super(window, self).__init__(parent)
        app.aboutToQuit.connect(self.myExitHandler)

        self.style_sheet = self.styleSheet('style')
        # app.setStyle(QStyleFactory.create('Macintosh'))
        #app.setStyleSheet(self.style_sheet)
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0,0,0,0)

        app.setOrganizationName("Eivind Arvesen")
        app.setOrganizationDomain("https://github.com/eivind88/raskolnikov")
        app.setApplicationName("Raskolnikov")
        app.setApplicationVersion("0.0.1")
        settings = QSettings()

        self.data_location = QDesktopServices.DataLocation
        self.temp_location = QDesktopServices.TempLocation
        self.cache_location = QDesktopServices.CacheLocation

        self.startpage = "https://duckduckgo.com/"
        self.new_tab_behavior = "insert"

        global bookmarks

        global saved_tabs
        print "Currently saved_tabs:\n", saved_tabs

        global menubar
        menubar = QMenuBar()

        # Initialize a statusbar for the window
        self.statusbar = self.statusBar()
        self.statusbar.setFont(QFont("Helvetica Neue", 11, QFont.Normal))
        self.statusbar.setStyleSheet(self.style_sheet)
        self.statusbar.setMinimumHeight(15)

        self.pbar = QProgressBar()
        self.pbar.setMaximumWidth(100)
        self.statusbar.addPermanentWidget(self.pbar)

        self.statusbar.hide()

        self.setMinimumSize(504, 235)
        # self.setWindowModified(True)
        # app.alert(self, 0)
        self.setWindowTitle("Raskolnikov")
        # toolbar = self.addToolBar('Toolbar')
        # toolbar.addAction(exitAction)
        # self.setUnifiedTitleAndToolBarOnMac(True)
        self.setWindowIcon(QIcon(""))

        # Create input widgets
        self.bbutton = QPushButton(u"<")
        self.fbutton = QPushButton(u">")
        self.hbutton = QPushButton(u"⌂")
        self.edit = QLineEdit("")
        self.edit.setFont(QFont("Helvetica Neue", 12, QFont.Normal))
        self.edit.setPlaceholderText("Enter URL")
        # self.edit.setMinimumSize(400, 24)
        self.rbutton = QPushButton(u"↻")
        self.dbutton = QPushButton(u"☆")
        self.tbutton = QPushButton(u"⁐")
        # ↆ ⇧ √ ⌘ ⏎ ⏏ ⚠ ✓ ✕ ✖ ✗ ✘ ::: ❤ ☮ ☢ ☠ ✔ ☑ ♥ ✉ ☣ ☤ ✘ ☒ ♡ ツ ☼ ☁ ❅ ✎
        self.nbutton = QPushButton(u"+")
        self.nbutton.setObjectName("NewTab")
        self.nbutton.setMinimumSize(35, 30)
        self.nbutton.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)

        self.edit.setTextMargins(2, 1, 2, 0)

        # create a horizontal layout for the input
        input_layout = QHBoxLayout()
        input_layout.setSpacing(4)
        input_layout.setContentsMargins(0, 0, 0, 0)

        # add the input widgets to the input layout
        input_layout.addWidget(self.bbutton)
        input_layout.addWidget(self.fbutton)
        input_layout.addWidget(self.hbutton)
        input_layout.addWidget(self.edit)
        input_layout.addWidget(self.rbutton)
        input_layout.addWidget(self.dbutton)
        input_layout.addWidget(self.tbutton)

        # create a widget to hold the input layout
        self.input_widget = QFrame()
        self.input_widget.setObjectName("InputWidget")
        self.input_widget.setStyleSheet(self.style_sheet)

        # set the layout of the widget
        self.input_widget.setLayout(input_layout)
        self.input_widget.setVisible(True)

        # CREATE BOOKMARK-LINE HERE
        self.bookmarks_layout = QHBoxLayout()
        self.bookmarks_layout.setSpacing(0)
        self.bookmarks_layout.setContentsMargins(0, 0, 0, 0)

        for i in bookmarks:
            link = QToolButton()
            link.setDefaultAction(QAction(unicode(i), link))
            link.setObjectName(unicode(i))
            link.setFont(QFont("Helvetica Neue", 11, QFont.Normal))
            link.clicked.connect(self.handleBookmarks)

            self.bookmarks_layout.addWidget(link)

        self.bookmarks_widget = QFrame()
        self.bookmarks_widget.setObjectName("BookmarkWidget")
        self.bookmarks_widget.setStyleSheet(self.style_sheet)
        self.bookmarks_widget.setLayout(self.bookmarks_layout)

        if not bookmarks:
            self.bookmarks_widget.hide()

        # Task list
        self.tasklist = QStandardItemModel()
        #parentItem = self.tasklist.invisibleRootItem()
        #self.tasklist.header().hide()
        self.tasklist.setHorizontalHeaderItem(0, QStandardItem('Tasks'))
        parentItem = QStandardItem("Parent")
        self.tasklist.appendRow(parentItem)
        for i in range(4):
            item = QStandardItem("Item %d" % i)
            parentItem.appendRow(item)
            #parentItem = item

        #self.list.activated[str].connect(self.handleBookmarks)
        #self.list.view().setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)

        # create tabs
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(False)
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.tabBar().hide()
        self.tabs.setFont(QFont("Helvetica Neue", 11, QFont.Normal))
        self.tabs.setCornerWidget(self.nbutton)
        self.tabs.cornerWidget().setObjectName("CornerWidget")
        self.tabs.cornerWidget().setMinimumSize(10, 24)
        self.tabs.cornerWidget().setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)

        if saved_tabs:
            for tab in saved_tabs['tabs']:
                tasklist = QTreeView()
                tasklist.hide()
                tasklist.setObjectName('taskList')
                tasklist.setMinimumWidth(100)
                tasklist.setMaximumWidth(250)

                new_tab = QWebView()
                new_tab.setObjectName('webView')

                inspector = QWebInspector(self)
                inspector.setObjectName('webInspector')
                inspector.hide()

                page_layout = QVBoxLayout()
                page_layout.setSpacing(0)
                page_layout.setContentsMargins(0, 0, 0, 0)
                page_layout.addWidget(new_tab)
                page_layout.addWidget(inspector)
                page_widget = QFrame()
                page_widget.setObjectName('pageWidget')
                page_widget.setLayout(page_layout)

                complete_tab_layout = QHBoxLayout()
                complete_tab_layout.setSpacing(0)
                complete_tab_layout.setContentsMargins(0, 0, 0, 0)
                complete_tab_layout.addWidget(tasklist)
                complete_tab_layout.addWidget(page_widget)
                complete_tab_widget = QFrame()
                complete_tab_widget.setLayout(complete_tab_layout)

                #for page in tab['history']:
                #    new_tab.load(QUrl(page['url']))
                #print tab['current_history']
                #for item in new_tab.history().items():
                #    print item
                #new_tab.history().goToItem(new_tab.history().itemAt(tab['current_history']))
                new_tab.load(QUrl(tab['history'][tab['current_history']]['url']))
                tab['current_history']
                self.tabs.setUpdatesEnabled(False)
                if self.new_tab_behavior == "insert":
                    self.tabs.insertTab(self.tabs.currentIndex()+1, complete_tab_widget,
                                        unicode(new_tab.title()))
                elif self.new_tab_behavior == "append":
                    self.tabs.appendTab(complete_tab_widget, unicode(new_tab.title()))
                self.tabs.setUpdatesEnabled(True)
                new_tab.titleChanged.connect(self.change_tab)
                new_tab.urlChanged.connect(self.change_tab)
                new_tab.loadStarted.connect(self.load_start)
                new_tab.loadFinished.connect(self.load_finish)
                new_tab.loadProgress.connect(self.pbar.setValue)
                new_tab.page().linkHovered.connect(self.linkHover)
                inspector.setPage(new_tab.page())

            for index, tab in enumerate(saved_tabs['tabs']):
                self.tabs.setTabText(index, tab['history'][tab['current_history']]['title'])

            self.tabs.setCurrentIndex(saved_tabs['current_tab'])
        else:
            self.new_tab()

        tabs_layout = QVBoxLayout()
        tabs_layout.setSpacing(0)
        tabs_layout.setContentsMargins(0, 0, 0, 0)
        tabs_layout.addWidget(self.tabs)

        self.tabs_widget = QFrame()
        self.tabs_widget.setObjectName("TabLine")
        self.tabs_widget.setStyleSheet(self.style_sheet)
        self.tabs_widget.setLayout(tabs_layout)
        self.tabs_widget.setVisible(True)

        # Webkit settings
        gsettings = self.tabs.currentWidget().findChild(QFrame, unicode('pageWidget')).findChild(QWebView, unicode('webView')).settings().globalSettings()
        # Basic settings
        gsettings.setAttribute(QWebSettings.AutoLoadImages, True)
        gsettings.setAttribute(QWebSettings.JavascriptEnabled, True)
        gsettings.setAttribute(QWebSettings.JavascriptCanOpenWindows, False)
        gsettings.setAttribute(QWebSettings.JavascriptCanAccessClipboard, False)
        gsettings.setAttribute(QWebSettings.PluginsEnabled, False) # Flash isn't stable at present
        gsettings.setAttribute(QWebSettings.JavaEnabled, False) # Java applet's aren't supported by PySide
        gsettings.setAttribute(QWebSettings.DeveloperExtrasEnabled, True)
        gsettings.setAttribute(QWebSettings.AcceleratedCompositingEnabled,
            True)
        # Performace settings
        gsettings.setAttribute(QWebSettings.DnsPrefetchEnabled, True)
        gsettings.setAttribute(QWebSettings.AcceleratedCompositingEnabled, True)
        gsettings.setAttribute(QWebSettings.DnsPrefetchEnabled, True)
        # Other settings
        gsettings.setAttribute(QWebSettings.PrivateBrowsingEnabled, False)

        # Create a vertical layout and add widgets
        vlayout = QVBoxLayout()
        vlayout.setSpacing(0)
        vlayout.setContentsMargins(0, 0, 0, 0)
        # toolbar.addWidget(self.input_widget)
        vlayout.addWidget(self.input_widget)
        vlayout.addWidget(self.bookmarks_widget)
        vlayout.addWidget(self.tabs_widget)

        # create a widget to hold the vertical layout
        wrapper_widget = QWidget()
        wrapper_widget.setLayout(vlayout)
        self.setCentralWidget(wrapper_widget)

        self.bbutton.clicked.connect(self.tabs.currentWidget().findChild(QFrame, unicode('pageWidget')).findChild(QWebView, unicode('webView')).back)
        self.fbutton.clicked.connect(self.tabs.currentWidget().findChild(QFrame, unicode('pageWidget')).findChild(QWebView, unicode('webView')).forward)
        self.hbutton.clicked.connect(self.goHome)
        self.edit.returnPressed.connect(self.set_url)
        # Add button signal to "go" slot
        self.rbutton.clicked.connect(self.tabs.currentWidget().findChild(QFrame, unicode('pageWidget')).findChild(QWebView, unicode('webView')).reload)
        self.dbutton.clicked.connect(self.bookmark)
        self.tbutton.clicked.connect(self.toggleTaskBar)
        self.nbutton.clicked.connect(self.new_tab)
        self.tabs.tabCloseRequested.connect(self.tabs.removeTab)
        self.tabs.currentChanged.connect(self.change_tab)

        widgets = (input_layout.itemAt(i).widget() for i in range(
            input_layout.count()))
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
        sequence = QKeySequence(Qt.CTRL + Qt.ALT + Qt.Key_L)
        QShortcut(sequence, self, self.toggle_input)

        # make an accelerator to focus adress-bar
        sequence = QKeySequence(Qt.CTRL + Qt.Key_L)
        QShortcut(sequence, self, self.focus_adress)

        # make an accelerator to reload page
        sequence = QKeySequence(Qt.CTRL + Qt.Key_R)
        QShortcut(sequence, self, self.tabs.currentWidget().findChild(QFrame, unicode('pageWidget')).findChild(QWebView, unicode('webView')).reload)

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

        # make an accelerator to toggle bookmark
        sequence = QKeySequence(Qt.CTRL + Qt.Key_D)
        QShortcut(sequence, self, self.bookmark)

        # make an accelerator to toggle task/project-list
        sequence = QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_L)
        QShortcut(sequence, self, self.toggleTaskBar)

        # finally set the attribute need to rotate
        # try:
        #     self.setAttribute(Qt.WA_Maemo5AutoOrientation, True)
        # except:
        #     print "not maemo"

        self.statusbar.show()

    def press_button(self):
        """On button press. Connected."""
        self.sender().setStyleSheet('background-color: rgba(228, 228, 228)')

    def release_button(self):
        """On button release. Connected."""
        self.sender().setStyleSheet('background-color: rgba(252, 252, 252)')

    def goHome(self):
        """Go to startpage."""
        self.tabs.currentWidget().findChild(QFrame, unicode('pageWidget')).findChild(QWebView, unicode('webView')).setUrl(QUrl(self.startpage))

    def handleShowInspector(self):
        """Toggle web inspector."""
        self.tabs.currentWidget().findChild(QFrame, unicode('pageWidget')).findChild(QWebInspector, unicode('webInspector')).setShown(self.tabs.currentWidget().findChild(QFrame, unicode('pageWidget')).findChild(QWebInspector, unicode('webInspector')).isHidden())

    def toggleTaskBar(self):
        """Toggle task bar."""
        if self.tabs.currentWidget().findChild(QTreeView, unicode('taskList')).isHidden():
            self.tabs.currentWidget().findChild(QTreeView, unicode('taskList')).setModel(self.tasklist)
        self.tabs.currentWidget().findChild(QTreeView, unicode('taskList')).setShown(self.tabs.currentWidget().findChild(QTreeView, unicode('taskList')).isHidden())
        #self.tasklist.setShown(self.tasklist.isHidden())

    def focus_adress(self):
        """Focus adress bar."""
        self.edit.selectAll()
        self.edit.setFocus()

    def toggle_input(self):
        """Toggle input visibility."""
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
        self.change_tab()

    def linkHover(self, l):
        """Show link adress in status bar on mouse hover."""
        self.statusbar.showMessage(l)

    def new_tab(self):
        """Open new tab."""
        tasklist = QTreeView()
        tasklist.hide()
        tasklist.setObjectName('taskList')
        tasklist.setMinimumWidth(100)
        tasklist.setMaximumWidth(250)

        new_tab = QWebView()
        new_tab.setObjectName('webView')

        inspector = QWebInspector(self)
        inspector.setObjectName('webInspector')
        inspector.hide()

        page_layout = QVBoxLayout()
        page_layout.setSpacing(0)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.addWidget(new_tab)
        page_layout.addWidget(inspector)
        page_widget = QFrame()
        page_widget.setObjectName('pageWidget')
        page_widget.setLayout(page_layout)

        complete_tab_layout = QHBoxLayout()
        complete_tab_layout.setSpacing(0)
        complete_tab_layout.setContentsMargins(0, 0, 0, 0)
        complete_tab_layout.addWidget(tasklist)
        complete_tab_layout.addWidget(page_widget)
        complete_tab_widget = QFrame()
        complete_tab_widget.setLayout(complete_tab_layout)

        new_tab.load(QUrl(self.startpage))
        self.tabs.setUpdatesEnabled(False)
        if self.new_tab_behavior == "insert":
            self.tabs.insertTab(self.tabs.currentIndex()+1, complete_tab_widget,
                                    unicode(new_tab.title()))
        elif self.new_tab_behavior == "append":
            self.tabs.appendTab(complete_tab_widget, unicode(new_tab.title()))
        self.tabs.setCurrentWidget(complete_tab_widget)
        self.tabs.setTabText(self.tabs.currentIndex(),
                             unicode(self.tabs.currentWidget().findChild(QFrame, unicode('pageWidget')).findChild(QWebView, unicode('webView')).title()))
        self.tabs.setUpdatesEnabled(True)
        # tab.page().mainFrame().setScrollBarPolicy(Qt.Horizontal, Qt.ScrollBarAlwaysOff)
        # tab.page().mainFrame().setScrollBarPolicy(Qt.Vertical, Qt.ScrollBarAlwaysOff)
        new_tab.titleChanged.connect(self.change_tab)
        new_tab.urlChanged.connect(self.change_tab)
        new_tab.loadStarted.connect(self.load_start)
        new_tab.loadFinished.connect(self.load_finish)
        new_tab.loadProgress.connect(self.pbar.setValue)
        new_tab.page().linkHovered.connect(self.linkHover)
        inspector.setPage(new_tab.page())

    def change_tab(self):
        """Change active tab."""
        if self.tabs.count() <= 1:
            self.tabs.tabBar().hide()
        else:
            self.tabs.tabBar().show()

        try:
            self.edit.setText(str(self.tabs.currentWidget().findChild(QFrame, unicode('pageWidget')).findChild(QWebView, unicode('webView')).url().toEncoded()))
            self.tabs.setTabText(self.tabs.currentIndex(),
                                 unicode(self.tabs.currentWidget().findChild(QFrame, unicode('pageWidget')).findChild(QWebView, unicode('webView')).title()))
            self.tabs.currentWidget().findChild(QFrame, unicode('pageWidget')).findChild(QWebView, unicode('webView')).setFocus()
        except Exception:
            self.tabs.tabBar().hide()
            self.new_tab()

        #print (self.tabs.widget(self.tabs.currentIndex()).size().width()-10), self.tabs.count()
        self.tabs_widget.setStyleSheet(self.style_sheet +
                                       "QTabBar::tab { width:" + str(
                                        (self.tabs.widget(
                                            self.tabs.currentIndex()
                                            ).size().width()-26-self.tabs.count()*2)/self.tabs.count()
                                        ) + "px; }")

    def previous_tab(self):
        """Previous tab."""
        try:
            if self.tabs.currentIndex() > 0:
                self.tabs.setCurrentIndex(self.tabs.currentIndex()-1)
            else:
                self.tabs.setCurrentIndex(self.tabs.count()-1)

            self.change_tab()
        except Exception:
            pass

    def next_tab(self):
        """Next tab."""
        try:
            if self.tabs.currentIndex() < self.tabs.count()-1:
                self.tabs.setCurrentIndex(self.tabs.currentIndex()+1)
            else:
                self.tabs.setCurrentIndex(0)

            self.change_tab()
        except Exception: #, e
            pass

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
        self.tabs.currentWidget().findChild(QFrame, unicode('pageWidget')).findChild(QWebView, unicode('webView')).load(qurl)
        self.tabs.currentWidget().findChild(QFrame, unicode('pageWidget')).findChild(QWebView, unicode('webView')).setFocus()

    def load_start(self):
        """Update view values, called upon started page load."""
        self.rbutton.setText(u"╳")
        self.rbutton.clicked.connect(self.tabs.currentWidget().findChild(QFrame, unicode('pageWidget')).findChild(QWebView, unicode('webView')).stop)
        self.pbar.show()

    def load_finish(self):
        """Update view values, called upon finished page load."""
        if (self.tabs.currentWidget().findChild(QFrame, unicode('pageWidget')).findChild(QWebView, unicode('webView')).history().canGoBack()):
            self.bbutton.setEnabled(True)
        else:
            self.bbutton.setEnabled(False)
        if (self.tabs.currentWidget().findChild(QFrame, unicode('pageWidget')).findChild(QWebView, unicode('webView')).history().canGoForward()):
            self.fbutton.setEnabled(True)
        else:
            self.fbutton.setEnabled(False)

        self.rbutton.setText(u"↻")
        self.rbutton.clicked.connect(self.tabs.currentWidget().findChild(QFrame, unicode('pageWidget')).findChild(QWebView, unicode('webView')).reload)
        self.pbar.hide()

        global bookmarks
        if unicode(self.tabs.currentWidget().findChild(QFrame, unicode('pageWidget')).findChild(QWebView, unicode('webView')).url().toEncoded()) in bookmarks:
            self.dbutton.setText(u"★")
        else:
            self.dbutton.setText(u"☆")

        if not self.tabs.currentWidget().findChild(QFrame, unicode('pageWidget')).findChild(QWebInspector, unicode('webInspector')).isHidden():
            self.tabs.currentWidget().findChild(QFrame, unicode('pageWidget')).findChild(QWebInspector, unicode('webInspector')).hide()
            self.tabs.currentWidget().findChild(QFrame, unicode('pageWidget')).findChild(QWebInspector, unicode('webInspector')).show()

    def bookmark(self):
        """Toggle bookmark."""
        global bookmarks
        if not self.tabs.currentWidget().findChild(QFrame, unicode('pageWidget')).findChild(QWebView, unicode('webView')).url().toEncoded() in bookmarks:
            bookmarks.append(self.tabs.currentWidget().findChild(QFrame, unicode('pageWidget')).findChild(QWebView, unicode('webView')).url().toEncoded())
            pickle.dump(bookmarks, open(bookFile, "wb"))
            link = QToolButton()
            link.setDefaultAction(QAction(unicode(unicode(self.tabs.currentWidget().findChild(QFrame, unicode('pageWidget')).findChild(QWebView, unicode('webView')).url().toEncoded())), link))
            link.setObjectName(unicode(self.tabs.currentWidget().findChild(QFrame, unicode('pageWidget')).findChild(QWebView, unicode('webView')).url().toEncoded()))
            link.setFont(QFont("Helvetica Neue", 11, QFont.Normal))
            link.clicked.connect(self.handleBookmarks)
            self.bookmarks_layout.addWidget(link)

            if self.bookmarks_widget.isHidden():
                self.bookmarks_widget.show()

            self.dbutton.setText(u"★")

        else:
            bookmarks.remove(self.tabs.currentWidget().findChild(QFrame, unicode('pageWidget')).findChild(QWebView, unicode('webView')).url().toEncoded())
            pickle.dump(bookmarks, open(bookFile, "wb"))
            link = self.bookmarks_widget.findChild(QToolButton, unicode(self.tabs.currentWidget().findChild(QFrame, unicode('pageWidget')).findChild(QWebView, unicode('webView')).url().toEncoded()))
            self.bookmarks_layout.removeWidget(link)
            link.deleteLater()
            link = None

            if not bookmarks:
                self.bookmarks_widget.hide()

            self.dbutton.setText(u"☆")

    def handleBookmarks(self):

        self.gotoLink(self.sender().objectName())
        #self.gotoLink(unicode())

    def gotoLink(self, url):

        self.tabs.currentWidget().findChild(QFrame, unicode('pageWidget')).findChild(QWebView, unicode('webView')).load(QUrl(url))

    def styleSheet(self, style_sheet):
        """Load stylesheet."""
        try:
            with open(os.path.join
                      (basedir, 'assets', 'style.qss'), 'r') as file:
                return file.read()
        except Exception:
            # print e
            return ''

    def resizeEvent(self, evt=None):
        """Called on window resize."""
        self.change_tab()

    def myExitHandler(self):
        """Exiting."""
        pass
        global tabFile

    # {current_tab: 1, tabs:[0: {current_history:3, history:[{title, url}]]}
        pb = {'current_tab': self.tabs.currentIndex()}
        pb['tabs'] = list()
        for tab in range(self.tabs.count()):
            pb['tabs'].append(dict(current_history=self.tabs.widget(
                tab).findChild(QFrame, unicode('pageWidget')).findChild(QWebView, unicode('webView')).history().currentItemIndex(), history=list(dict(
                    title=item.title(), url=item.url()
                    ) for item in self.tabs.widget(tab).findChild(QFrame, unicode('pageWidget')).findChild(QWebView, unicode('webView')).history().items())))

        # print pb
        pickle.dump(pb, open(tabFile, "wb"))


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
