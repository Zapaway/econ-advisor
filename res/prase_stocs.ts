import * as fs from 'fs';
import { promisify } from 'util';

const readFile = promisify(fs.readFile);

interface Stock {
    ideal_risk: string[];
    ideal_timeframes: string[];
}

// parses the stocks in stocks.json to get the stock symbols associated with a risk/timeframe
async function parse_stocks(risk: string, timeframe: string): Promise<string[]> {
    const data = await readFile('stocks.json', 'utf8');
    const stocks: Record<string, Stock> = JSON.parse(data);
    const stockSymbols: string[] = [];
    for (let ticker of Object.keys(stocks)) {
        if (stocks[ticker].ideal_risk.includes(risk) && stocks[ticker].ideal_timeframes.includes(timeframe)) {
            stockSymbols.push(ticker);
        }
    }
    return stockSymbols;
}

// test:
(async () => {
    let stocks = await parse_stocks('low', 'short');
    for (let stock of stocks) {
        console.log(stock);
    }
})();