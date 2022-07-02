### Hexlet tests and linter status:
[![Actions Status](https://github.com/Unshock/python-project-lvl3/workflows/hexlet-check/badge.svg)](https://github.com/Unshock/python-project-lvl3/actions)
[![hexlet-check](https://github.com/Unshock/python-project-lvl3/actions/workflows/tests-and-linter-check.yml/badge.svg)](https://github.com/Unshock/python-project-lvl3/actions/workflows/tests-and-linter-check.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/7a23aae7f3a889a03cb0/maintainability)](https://codeclimate.com/github/Unshock/python-project-lvl3/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/7a23aae7f3a889a03cb0/test_coverage)](https://codeclimate.com/github/Unshock/python-project-lvl3/test_coverage)
## "Page loader" study project for Hexlet.io 
### Description:
##### The project consists of a utility that saves given web page locally. 

### Page loader install
The project exists only on ***github*** and for usage could be installed using ***pip*** command:

    python3 -m pip install --user git+https://github.com/Unshock/python-project-lvl3.git

### Page loader run
By default, the program downloads web-page to the directory it was run from. Run of the program is carried out by the command below:

    page-loader URL
To set the directory you can use options that can be applied by the commands below: 
    
    page-loader URL --output /home/user/web-pages

    page-loader URL -o /home/user/web-pages

Page loader can be also imported while using python

    python3

    from page_loader import download

    download('https://website.org/', 'existing_directory')


#### Asciinema demonstrations of install, program usage and import of the module
[![asciicast](https://asciinema.org/a/RjHe25jBuR7WYAHORa85JVcnr.svg)](https://asciinema.org/a/RjHe25jBuR7WYAHORa85JVcnr)
[![asciicast](https://asciinema.org/a/RmzZoZlQar8yWm8bjWwN6lDaS.svg)](https://asciinema.org/a/RmzZoZlQar8yWm8bjWwN6lDaS)
[![asciicast](https://asciinema.org/a/Pji39aH2C2clrD96uKbm9kVQ5.svg)](https://asciinema.org/a/Pji39aH2C2clrD96uKbm9kVQ5)