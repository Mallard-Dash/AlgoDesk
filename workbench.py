from colorama import Fore, init
init()

red = Fore.RED
green = Fore.GREEN
blue = Fore.BLUE
mag = Fore.MAGENTA
yel = Fore.YELLOW


print(f"{mag} |------------------------------------------------------------------------------|\n"
    f" |*************************Available tickers************************************|\n",
    f"{blue}|------------------------------------------------------------------------------|\n"
    f" {green}|Ticker|	{red}|Company /Asset|	        {yel}|Category              {blue}         |\n",
    f"{blue}|------------------------------------------------------------------------------|\n",
    f"{green}|1. AAPL   |  {red}|Apple Inc.                |{yel}|Big Tech Stock                      |\n",
    f"{green}|2. NVDA   |  {red}|Nvidia Corp.              |{yel}|AI/Semiconductor Stock              |\n",
    f"{green}|3. MSFT   |  {red}|Microsoft Corp.           |{yel}|Software Stock                      |\n",
    f"{green}|4. SPY    |  {red}|S&P 500   ETF Broad Market|{yel}|(Tracks the top 500 US companies)   |\n",
    f"{green}|5. GLD    |  {red}|SPDR Gold Shares          |{yel}|Commodity (Tracks the price of gold)|\n",
    f"{green}|6. USO    |  {red}|United States Oil Fund    |{yel}|Commodity (Tracks the price of oil) |\n",
    f"{green}|7. JPM    |  {red}|JPMorgan Chase & Co.      |{yel}|Finance/Bank Stock                  |\n",
    f"{green}|8. BTC-USD|  {red}|Bitcoin                   |{yel}|Cryptocurrency                      |\n",
    f"{blue}|------------------------------------------------------------------------------|")

