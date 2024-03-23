import { useEffect, useState } from "react";
import { useForm, SubmitHandler } from "react-hook-form";

interface FormInput {
  ideal_risk: string;
  ideal_timeframes: string;
}
interface Stock {
  ideal_risk: string[];
  ideal_timeframes: string[];
}

export default function Root() {
  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<FormInput>();
  const onSubmit: SubmitHandler<FormInput> = (data) => setRes(parse_stocks(data.ideal_risk, data.ideal_timeframes) ?? null);
  
  const [stocks, setStocks] = useState<Record<string, Stock> | null>();
  const [res, setRes] = useState<string[] | null>(null);

  // parses the stocks in stocks.json to get the stock symbols associated with a risk/timeframe
  const parse_stocks = (risk: string, timeframe: string) => {
    if (!stocks) return;

    const stockSymbols: string[] = [];
    for (let ticker of Object.keys(stocks)) {
      if (
        stocks[ticker].ideal_risk.includes(risk) &&
        stocks[ticker].ideal_timeframes.includes(timeframe)
      ) {
        stockSymbols.push(ticker);
      }
    }
    return stockSymbols;
  };

  useEffect(() => {
    (async () => {
      const response = await fetch('/stocks.json');
      // const data = await readFile("stocks.json", "utf8");
      const stocks: Record<string, Stock> = await response.json();
      setStocks(stocks);
    })();
  }, []);

  return (
    <div>
      <form onSubmit={handleSubmit(onSubmit)} className="dark flex flew-row gap-1">
        <input
          type="text"
          placeholder="risk"
          className="input input-bordered w-full max-w-xs"
          {...register("ideal_risk")}
        />
        <input
          type="text"
          placeholder="timeframes"
          className="input input-bordered w-full max-w-xs"
          {...register("ideal_timeframes")}
        />
        {/* <input
        type="text"
        placeholder="Input three"
        className="input input-bordered w-full max-w-xs"
      /> */}
        <input type="submit" className="btn" />
      </form>

      {res && (
        <ul>
          {res.map((x, i) => (
            <li key={i}>{x}</li>
          ))}
        </ul>
      )}
    </div>
  );
}
