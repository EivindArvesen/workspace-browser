#-*- mode: python -*-
import os, sys, shutil

root = os.path.dirname(os.path.realpath('__file__'))
version = "0.0.1"
appname = "Raskolnikov"

a = Analysis(
 [
 #os.path.join(HOMEPATH,'support/_mountzlib.py'),
 #os.path.join(CONFIGDIR,'support/useUnicode.py'),
 'raskolnikov/main.py'
 ],
 pathex=[root],
 hiddenimports=['PySide.QtNetwork'],
 hookspath=None,
 runtime_hooks=None,
 excludes=None)

extrafiles = [(os.path.join("assets", 'style.qss'), os.path.join("raskolnikov", "assets", 'style.qss'), 'DATA')]

pyz = PYZ (a.pure)
exe = EXE( pyz,
 a.scripts,
 a.binaries,
 a.zipfiles,
 a.datas + extrafiles,
 name=os.path.join(root, 'dist', appname),
 debug=False, #True
 strip=True, #None
 upx=True,
 console=False #True
 )

if sys.platform.startswith("darwin"):
 app = BUNDLE (exe,
                 name=os.path.join(root, 'dist', appname+'.app'),
                 #icon=os.path.join(root, 'res', 'icon.icns'),
                 #bundle_identifier=None,
                 version=version)

#shutil.copytree(
# '/Library/Frameworks/QtGui.framework/Versions/Current/Resources/qt_menu.nib',
# os.path.join(root, 'dist', appname+'.app', 'Contents/Resources/qt_menu.nib'))

shutil.copy(
 os.path.join("res", "icon.icns"),
 os.path.join('dist', appname+'.app', 'Contents/Resources/icon-windowed.icns'))
