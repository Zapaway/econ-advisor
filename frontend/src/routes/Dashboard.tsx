import axios from "axios";
import { useEffect, useState } from "react";
import { useForm, SubmitHandler } from "react-hook-form";
import GetTickersForm from "../components/GetTickersForm";



export default function Dashboard() {

  return (
    <div className="m-4">
      <GetTickersForm />

    </div>
  );
}
