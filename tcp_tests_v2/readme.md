# Requirements
1. Python 3.x, the very latest stable release is recommended
2. Python virtual environment using whatever mechanism you like ([Conda](https://www.geeksforgeeks.org/set-up-virtual-environment-for-python-using-anaconda/), [Pipenv](https://docs.python-guide.org/dev/virtualenvs/), [Out of the box](https://docs.python.org/3/library/venv.html))
# Setup
1. Once your virtual environment is activated, run ```sudo pip3 install -r requirements.txt``` (it may be the case I forgot a requirement, so you might need to install it when you see an import error)

# Usage
* Below is a template that you can use.  Import and set up logging if you wish
* See the file ```shared.py``` for available servers, ports and tokens.  You can always just use whatever values you wish
* Create a test.Test() object.  Note ```max_lines``` indicates the max number of messages to process
* Prepackaged tests are available from the test.Test() object.  Create your own if you wish
* To create your own, you can use tcp.Tools() as it returns a dictionary with data

```python
import shared
import test
from loguru import logger
logger.add(<log_path>, format='{time} {name} {message}', level='DEBUG', rotation="500 MB", retention="10 days")
server = shared.Endpoints.v2_production.value
port = shared.Ports.v2_production.value
token = shared.Tokens.full_v2.value

test = test.Test(server=server, port=port, token=token, max_lines=100000, label='full_feed')
test.some_test_here()
```
If you wish to force checkpoint to a specific date, you set ```reset_date``` in the format *_2021-03-08T11:45:09.840Z_*.
