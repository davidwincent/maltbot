# maltbot
_maltbot_ is a slack bot with different interests, including :beer:


### setup on Linux or Darwin
Install Python 3.5 or later - https://www.python.org/

`$ [sudo] pip install virtualenv`

`$ virtualenv PYMALT`

Acticate virtualenv _PYMALT_ - https://virtualenv.pypa.io/en/latest/userguide/ 

`$ git clone git@github.com:davidwincent/maltbot.git` - or forked repository if
you want to contribute ;)

`$ cd maltbot`

`$ pip install -r requirements.txt`

`$ [sudo] chmod u+x ./runtest`

`$ [sudo] chmod u+x ./start`

### usage
`./runtest` - run tests and watch file changes until CTRL+C

`./start` - start _maltbot_ - reads slack api keys found in `./env`
