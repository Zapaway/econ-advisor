import axios from "axios";
import { useEffect, useState } from "react";
import { useForm, SubmitHandler } from "react-hook-form";
import Markdown from "react-markdown";

const LOCALHOST = "http://192.168.92.104:5000";

interface FormInput {
  risk: string;
  timeframe: string;
}
interface FormResult {
  name: string;
  ticker: string;
  blurb: string;
  articleLinks: string[];
}

export default function GetTickersForm() {
  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<FormInput>();
  const onSubmit: SubmitHandler<FormInput> = async (data) => {
    setLoading(true);
    const tickers = await axios.get(`${LOCALHOST}/getTickers`, {
      params: data,
    });

    const finalResult = await Promise.all(
      tickers.data.map(({ ticker, name }: { ticker: string; name: string }) => {
        return new Promise(async (res) => {
          console.log("ticker", res.ticker);
          const ultBlurb = await axios.get(`${LOCALHOST}/blurb`, {
            params: { ticker, name, ...data },
          });
          return res({
            name,
            ticker,
            blurb: ultBlurb.data[0],
            articleLinks: ultBlurb.data[1],
          });
        });
      })
    );
    setLoading(false);

    console.log(finalResult);
    setRes(finalResult);
  };

  const [isLoading, setLoading] = useState(false);
  const [res, setRes] = useState<FormResult[] | null>(null);

  return (
    <div>
      <h1 className="text-3xl font-spaceg mx-5 mt-10 font-bold">
        Welcome back, <span className="underline">User</span>! 👋
      </h1>
      <h1 className="text-xl font-spaceg mx-5 mb-10">
        Let's get some stock suggestions.
      </h1>
      <div className="flex justify-center">
        <form
          onSubmit={handleSubmit(onSubmit)}
          className="dark flex flex-col gap-2 w-full max-w-3xl"
        >
          {/* <input
                    type="text"
                    placeholder="risk"
                    className="input input-bordered w-full max-w-xs"
                    {...register("risk")}
                  /> */}
          <div className="flex flex-row gap-4 w-full items-center justify-center">
            <label className="form-control w-full max-w-md">
              <div className="label w-full">
                <span className="label-text">
                  How much risk are you willing to take?
                </span>
              </div>
              <select
                {...register("risk", { required: true })}
                className={`select select-bordered w-full max-w-md ${
                  errors.risk && "input-error"
                }`}
                disabled={isLoading}
              >
                <option value="">Select...</option>
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </label>
            <label className="form-control w-full max-w-md">
              <div className="label w-full">
                <span className="label-text">What is your timeframe?</span>
              </div>
              <select
                {...register("timeframe", { required: true })}
                className={`select select-bordered w-full max-w-md ${
                  errors.risk && "input-error"
                }`}
                disabled={isLoading}
              >
                <option value="">Select...</option>
                <option value="short">Short</option>
                <option value="medium">Medium</option>
                <option value="long">Long</option>
              </select>
            </label>
            {/* <input
                    type="text"
                    placeholder="Input three"
                    className="input input-bordered w-full max-w-xs"
                  /> */}
          </div>
          <input
            type="submit"
            className={`btn w-full ${isLoading && "btn-disabled"}`}
          />
        </form>
      </div>
      <div className="h-3"></div>
      <div className="m-3">
        {isLoading && <span className="loading loading-bars loading-lg"></span>}
        {res && !isLoading && (
          <div className="bg-gray-900 rounded-md">
            <div className="my-4 pt-4 text-center italic">
              We have {res.length} stocks that might be of interest.
            </div>
            {!!res.length ? (
              res.map(({ name, ticker, blurb, articleLinks }) => {
                return (
                  <ul className="flex flex-col gap-3">
                    <li key={ticker} className="bg-slate-950 rounded-xl p-5">
                      <h1 className="text-xl">
                        {ticker} ({name})
                      </h1>
                      <Markdown>{blurb}</Markdown>
                      <ul className="list-disc">
                        {articleLinks.map((link) => (
                          <li className="ml-3" key={link}>
                            <a
                              href={link}
                              className="text-blue-400 hover:text-blue-300"
                              target="_blank" rel="noopener noreferrer"
                            >
                              {link}
                            </a>
                          </li>
                        ))}
                      </ul>
                    </li>
                  </ul>
                );
                // return (
                //   <div
                //     tabIndex={0}
                //     className="collapse collapse-plus border border-base-300 bg-base-200"
                //   >
                //     <div className="collapse-title text-xl font-medium">
                //       {ticker} ({name})
                //     </div>
                //     <div className="collapse-content">
                //       <div>
                //         <Markdown>{blurb}</Markdown>
                //         <ul className="list-disc">
                //           {articleLinks.map((link) => (
                //             <li className="ml-3" key={link}>
                //               <a
                //                 href={link}
                //                 className="text-blue-400 hover:text-blue-300"
                //               >
                //                 {link}
                //               </a>
                //             </li>
                //           ))}
                //         </ul>
                //       </div>
                //     </div>
                //   </div>
                // );
              })
            ) : (
              <div className="bg-slate-950 rounded-xl p-5">
                Please try another search.
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
