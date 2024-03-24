import axios from "axios";
import { useEffect, useState } from "react";
import { useForm, SubmitHandler } from "react-hook-form";


const LOCALHOST = "place your URL here";


interface FormInput {
    risk: string;
    timeframe: string;
  }
  interface Stock {
    ideal_risks: string[];
    ideal_timeframes: string[];
  }

export default function Dashboard() {
    const {
        register,
        handleSubmit,
        watch,
        formState: { errors },
      } = useForm<FormInput>();
      const onSubmit: SubmitHandler<FormInput> = async (data) => {
        const res = await axios.get(`${LOCALHOST}/getTickers`, { params: data });
        setRes(res.data);
      };
      
      const [res, setRes] = useState<string[] | null>(null);
    
      // parses the stocks in stocks.json to get the stock symbols associated with a risk/timeframe
      // const parse_stocks = (risk: string, timeframe: string) => {
      //   if (!stocks) return;
    
      //   const stockSymbols: string[] = [];
      //   for (let ticker of Object.keys(stocks)) {
      //     if (
      //       stocks[ticker].ideal_risks.includes(risk) &&
      //       stocks[ticker].ideal_timeframes.includes(timeframe)
      //     ) {
      //       stockSymbols.push(ticker);
      //     }
      //   }
      //   return stockSymbols;
      // };
    
      // useEffect(() => {
      //   (async () => {
      //     const response = await fetch('/stocks.json');
      //     // const data = await readFile("stocks.json", "utf8");
      //     const stocks: Record<string, Stock> = await response.json();
      //     setStocks(stocks);
      //   })();
      // }, []);
    
      return (
        <div>
          <form onSubmit={handleSubmit(onSubmit)} className="dark flex flew-row gap-1">
            <input
              type="text"
              placeholder="risk"
              className="input input-bordered w-full max-w-xs"
              {...register("risk")}
            />
            <input
              type="text"
              placeholder="timeframes"
              className="input input-bordered w-full max-w-xs"
              {...register("timeframe")}
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
