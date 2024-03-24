import axios from "axios";
import { useEffect, useState } from "react";
import { useForm, SubmitHandler } from "react-hook-form";

const LOCALHOST = "http://192.168.92.104:5000/";

interface FormInput {
  risk: string;
  timeframe: string;
}
interface FormResult {
  ticker: string;
  description: string;
}

export default function GetTickersForm() {
  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<FormInput>();
  const onSubmit: SubmitHandler<FormInput> = async (data) => {
    // const res = await axios.get(`${LOCALHOST}/getTickers`, { params: data });
    // console.log(res);
    // setRes(res.data);
    setRes([
    //   { ticker: "AAPL", description: "I love Apple" },
    //   { ticker: "PPL", description: "Yo" },
    ]);
  };

  const [res, setRes] = useState<FormResult[] | null>(null);

  return (
    <div>
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
                className="input input-bordered w-full max-w-md"
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
                className="input input-bordered w-full max-w-md"
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
          <input type="submit" className="btn w-full" />
        </form>
      </div>
      <div className="h-3"></div>
      <div className="m-3">
        {res && (
          <div className="bg-gray-900 rounded-md">
            <div className="my-4 pt-4 text-center italic">
              We have {res.length} stocks we would like to recommend.
            </div>
            {!!res.length ? (<ul className="flex flex-col gap-3">
              {res.map(({ ticker, description }) => (
                <li key={ticker} className="bg-slate-950 rounded-xl p-5">
                  <h1 className="text-xl">{ticker}</h1>
                  <p className="">
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed
                    do eiusmod tempor incididunt ut labore et dolore magna
                    aliqua. Ut enim ad minim veniam, quis nostrud exercitation
                    ullamco laboris nisi ut aliquip ex ea commodo consequat.
                    Duis aute irure dolor in reprehenderit in voluptate velit
                    esse cillum dolore eu fugiat nulla pariatur. Excepteur sint
                    occaecat cupidatat non proident, sunt in culpa qui officia
                    deserunt mollit anim id est laborum.
                  </p>
                </li>
              ))}
            </ul>) : <div className="bg-slate-950 rounded-xl p-5">Please try another search.</div>}
          </div>
        )}
      </div>
    </div>
  );
}
