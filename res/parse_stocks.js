import { readFile } from 'fs/promises';

// parses the stocks in stocks.json to get the stock symbols associated with a risk/timeframe
async function parse_stocks(risk, timeframe) {
    var stocks = JSON.parse(await readFile('stocks.json', 'utf8'));
    var stockSymbols = [];
    for (let ticker of Object.keys(stocks)) {
        if (stocks[ticker]["ideal_risk"].includes(risk) && stocks[ticker]["ideal_timeframes"].includes(timeframe)) {
        stockSymbols.push(ticker);
        }
    }
    return stockSymbols;
}


// test:
// let stocks = await parse_stocks('low', 'short');
// for (let stock of stocks) {
//     console.log(stock);
// }