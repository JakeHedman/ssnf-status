# ssnf-status

Tiny flask service to show operational info from SSNF ISPs as HTML

## Usage
### Installing dependencies
`
easy_install virtualenv
virtualenv env
source env/bin/activate
pip install -r requirements.txt
`
### Running
`
source env/bin/activate
python ssnf-status.py
`

or: (To restart on crash)
`
screen
source env/bin/activate
while true; do; python ssnf-status.py; sleep 1; done;
ctrl+a+d
`
