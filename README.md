# yflive v0.1.2

[![Build Status](https://github.com/mbnlc/yflive/actions/workflows/build.yml/badge.svg)](https://github.com/mbnlc/yflive/actions/workflows/build.yml)
[![CodeFactor](https://www.codefactor.io/repository/github/mbnlc/yflive/badge/master)](https://www.codefactor.io/repository/github/mbnlc/yflive/overview/master)

yflive is a [Yahoo! Finance](https://finance.yahoo.com) live data streamer. Originally created as an alternative to scraping prices of Yahoo! Finance, this implements a websocket client for receiving live quotes from Yahoo! Finance directly.

For historic prices or other financial information, [yfinance](https://github.com/ranaroussi/yfinance) is recommended.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install yflive.

```bash
pip install yflive
```

## Usage

```python
from yflive import QuoteStreamer

qs = QuoteStreamer()
qs.subscribe(["AAPL", "TSLA"]) 

qs.on_quote = lambda q: print(q)

qs.start()
```

## Collaboration

**This is very early stage**

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

**yflive** is distributed under the [Apache-2.0 License](http://www.apache.org/licenses/). Review [LICENSE.txt](https://github.com/mbnlc/yflive/blob/master/LICENSE.txt) for further information.
