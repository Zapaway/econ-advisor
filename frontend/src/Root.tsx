import { useEffect } from "react";
import { Link, Outlet, useLocation } from "react-router-dom";

const selectedGradient = "bg- bg-opacity-10";

export default function Root() {
  const location = useLocation();
  const pathname = location.pathname;

  useEffect(() => {
    console.log(location);
  }, [location])

  return (
    <div className="drawer lg:drawer-open">
      <input id="my-drawer-2" type="checkbox" className="drawer-toggle" />
      <div className="drawer-content">
        <Outlet />
        <label
          htmlFor="my-drawer-2"
          className="btn btn-primary drawer-button lg:hidden"
        >
        </label>
      </div>
      <div className="drawer-side">
        <label
          htmlFor="my-drawer-2"
          aria-label="close sidebar"
          className="drawer-overlay"
        ></label>
        <ul className="menu p-4 w-80 min-h-full bg-base-200 text-base-content">
          <div className="mx-3 mt-3 mb-5">
            <p className="font-spaceg text-3xl">EconAdvisor</p>
            <p className="text-lg">Investing for everyone.</p>
          </div>
          <li>
            <Link to={`/`} className={pathname === "/" ? "bg-white bg-opacity-10" : ""}>Dashboard</Link>
          </li>
          <li>
            <Link to={`/google-home`} className={pathname === "/google-home" ? "bg-white bg-opacity-10" : ""}>Google Home</Link>
          </li>
          <li>
            <Link to={`/robinhood`} className={pathname === "/robinhood" ? "bg-white bg-opacity-10" : ""}>Robinhood</Link>
          </li>
        </ul>
      </div>
    </div>
  );
}
