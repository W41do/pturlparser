[![penterepTools](https://www.penterep.com/external/penterepToolsLogo.png)](https://www.penterep.com/)


# PTURLPARSER
> Tool for extracting URLs from HTML and JavaScript

pturlparser is a tool that analyzes web pages and extracts all URLs from them, including links found in HTML and JavaScript content.

## Installation

```
pip install pturlparser # THIS IS NOT WORKING - use the option below
```
Alternative install:
```
git clone https://github.com/W41do/pturlparser.git
```
Then navigate to this folder:
```
cd /pturlparser/pturlparser/
```
To use the tool you will need to use:
```
python3 pturlparser.py
```
instead of
```
pturlparser
```

## Add to PATH (if necessary)
If you cannot invoke the script in your terminal, its probably because its not in your PATH. Fix it by running commands below.

> Add to PATH for Bash
```bash
echo "export PATH=\"`python3 -m site --user-base`/bin:\$PATH\"" >> ~/.bashrc
source ~/.bashrc
```

> Add to PATH for ZSH
```bash
echo "export PATH=\"`python3 -m site --user-base`/bin:\$PATH\"" >> ~/.zshrc
source ~/.zshrc
```

## Usage examples
```
pturlparser -u https://www.example.com
pturlparser -u https://www.example.com -o json
pturlparser -u https://www.example.com -o text
... TODO
```

## Options
```
Output options: -o/--output [console/json/text]
...TODO
```

## Dependencies
```
TODO
```

## Version History
```
0.0.1
    - Alpha release
```

## License

Copyright (c) 2023 Penterep Security s.r.o.

pturlparser is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

pturlparser is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with pturlparser. If not, see https://www.gnu.org/licenses/.

## Warning

You are only allowed to run the tool against the websites which
you have been given permission to pentest. We do not accept any
responsibility for any damage/harm that this application causes to your
computer, or your network. Penterep is not responsible for any illegal
or malicious use of this code. Be Ethical!