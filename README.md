# Annotate

Simple GTK tool to annotate screenshots in the clipboard.
For Linux.

## Install

Copy code to a directory of your choice.

Create a file `~/.local/share/applications/annotate.desktop`:
```
[Desktop Entry]
Encoding=UTF-8
Version=1.0
Terminal=false
Type=Application
Name=Annotate
Icon={INSTALL_LOCATION}/annotate/icon.png
Exec={INSTALL_LOCATION}/annotate/main.py
StartupNotify=true
StartupWMClass=annotate
```

Replace `{INSTALL_LOCATION}` with the absoute path to the install location.

## References

- The Python GTK+ 3 Tutorial: https://python-gtk-3-tutorial.readthedocs.io/en/latest/index.html
- Gnome API Reference: https://developer.gnome.org/gdk3/stable/reference.html
- PyCairo API Reference: https://pycairo.readthedocs.io/en/latest/reference/index.html
- PyCairo tutorial: http://zetcode.com/gfx/pycairo/
- PyGObject API Reference: https://lazka.github.io/pgi-docs/
  - Gdk Reference: https://lazka.github.io/pgi-docs/Gdk-3.0/index.html
- Gnome Python Tutorial for beginners: https://developer.gnome.org/gnome-devel-demos/stable/tutorial.py.html.en
