Title: Building your PyInstaller App for multiple OSs with GitHub Actions

Previously, I’d written about building a [graphical user interface (GUI) for a command line tool (CLI) with PySimpleGUI and packaging it up with PyInstaller](@/2023-03-26-python-gui-pyinstaller.md). One drawback I noted with this (and is [noted by PyInstaller themselves](https://pyinstaller.org/en/stable/usage.html#supporting-multiple-operating-systems)) is that you can’t cross compile. This is a pain when I want to be able to build the app for operating systems (OS) I don’t have access too or don’t really want to spin up a virtual machine just to build an executeable. 

A natural solution to this feels like [GitHub actions](https://github.com/features/actions) which comes out of the box with runners for windows, macOS and Linux. GitHub actions are GitHubs offering for continuous integration and development and allow you to write simple yml based workflows that are executed on conditions (such as a new tag being pushed to the repo for a release). I love GitHub actions and regularly use and abuse them (see [hackpad Templator](https://github.com/ARCTraining/hackpad-templator)), mostly I like them for deploying things like this blog! Or for automated testing on my repositories. 

In this instance I want to setup an action that will build my executable on a new git tag, zip up all the bits from the build and deposit that in a GitHub release for the associated tag. Making it easier for me to grab a version of the app for different operating system if someone comes asking (not that I’m expecting hordes). 

I found some existing [pre built actions for building with PyInstaller](https://github.com/marketplace/actions/pyinstaller-windows) which seemed a reasonable first cut but rather decided to go down the route of just writing a series of shell steps instead. This better replicated my experience locally and didn’t lock the action in to any dependencies (it also meant if it broke I owned it!). I started off with an action like this:

```yml
name: build-exe

# Only run this when the master branch changes
on:
  push:
    tags:
      - "v*"

# This job installs dependencies, build the book, and pushes it to `gh-pages`
jobs:
  build-exe:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v4
        with:
          python-version: "3.10"
      - name: Install redwrench
        shell: bash -l {0}
        run: |
          pip3 install .
      - name: install PyInstaller
        shell: bash -l {0}
        run: |
          pip3 install pyinstaller==5.9.0
      - name: Build Pyinstaller .exe
        shell: bash -l {0}
        run: |
          pyinstaller -n redwrench --onefile --windowed app.py
      - uses: montudor/action-zip@v1
        with:
          args: zip -qq -r ${{ matrix.os }}-${{github.ref_name}}.zip dist
      - uses: softprops/action-gh-release@v1
        with:
          files: ${{ matrix.os }}-${{github.ref_name}}.zip
```

This does a couple of things:
1. Sets up the job to run on a matrix of different operating systems 
2. Checks out my repository cause we need the code to build the thing!
3. Installs the package redwrench because it’s a custom package and we want PyInstaller to package it up
4. Installs PyInstaller 
5. Runs a PyInstaller line to create a single file, windowed app with the name redwrench 
6. Use an existing action to zip everything in the dist directory up (dist is where PyInstaller puts stuff by default)
7. Use another action for uploading artefacts from action runs to releases 

This didn’t work first time (do any actions ever?) because my zip action uses docker (rather than JavaScript) and so was limited to Linux only action runners. No problem I’ll go find a different zip action. So I switched this for this:

```yml
- uses: vimtor/action-zip@v1
with:
    files: dist/
    recursive: false
    dest: ${{ matrix.os }}-${{github.ref_name}}.zip
```

And woo! I’ve got an action that works and uploads my artefacts to a release. 

On further testing on Windows I found this didn’t quite work. My windows windowed app failed silently, something I’m investigating. So after some local testing (I found a windows device!) I find that using —windowed is giving some issues. Without this setting all seems well (although further investigation is required. However, this means I need to update my action because I now want to run a different PyInstaller step for windows. GitHub actions allow you to do this easily with if blocks so I change the follow sections to this:

```yml
- name: Build Pyinstaller .exe (macOS and Linux)
if: matrix.os != 'windows-latest'
shell: bash -l {0}
run: |
    pyinstaller -n redwrench --onefile --windowed app.py
- name: Build Pyinstaller .exe (Windows)
if: matrix.os == 'windows-latest'
shell: bash -l {0}
run: |
    pyinstaller -n redwrench --onefile app.py
```

And this gets me to a happy place.

So overall I end up with an action like this:

```yml
name: build-exe

# Only run this when the master branch changes
on:
  push:
    tags:
      - "v*"

# This job installs dependencies, build the book, and pushes it to `gh-pages`
jobs:
  build-exe:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v4
        with:
          python-version: "3.10"
      - name: Install redwrench
        shell: bash -l {0}
        run: |
          pip3 install .
      - name: install PyInstaller
        shell: bash -l {0}
        run: |
          pip3 install pyinstaller==5.9.0
      - name: Build Pyinstaller .exe (macOS and Linux)
        if: matrix.os != 'windows-latest'
        shell: bash -l {0}
        run: |
          pyinstaller -n redwrench --onefile --windowed app.py
      - name: Build Pyinstaller .exe (Windows)
        if: matrix.os == 'windows-latest'
        shell: bash -l {0}
        run: |
          pyinstaller -n redwrench --onefile app.py
      - uses: vimtor/action-zip@v1
        with:
          files: dist/
          recursive: false
          dest: ${{ matrix.os }}-${{github.ref_name}}.zip
      - uses: softprops/action-gh-release@v1
        with:
          files: ${{ matrix.os }}-${{github.ref_name}}.zip
```

This does feel like a lot of effort to cross compile but it’s nice, the PyInstaller docs are great and the whole experience is very impressive given the complexity of what is going on. 
