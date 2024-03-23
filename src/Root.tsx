import { useState } from "react";
import { useForm, SubmitHandler } from "react-hook-form"


type Input = {
  
};
// type Result = {

// };

export default function Root() {
  const [res, useRes] = useState<string[] | null>(null);

  return (
    <div className="dark flex flew-row gap-1">
      <input
        type="text"
        placeholder="Input one"
        className="input input-bordered w-full max-w-xs"
      />
      <input
        type="text"
        placeholder="Input two"
        className="input input-bordered w-full max-w-xs"
      />
      <input
        type="text"
        placeholder="Input three"
        className="input input-bordered w-full max-w-xs"
      />
      <button className="btn">Submit</button>

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
