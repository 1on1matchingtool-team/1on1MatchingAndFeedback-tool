import React, { useState, useEffect } from "react";
import { getStartups } from "../../api/startupApi";

const AddStartupView = () => {
  const [startups, setStartups] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch the startup data from the backend
  useEffect(() => {
    const fetchStartups = async () => {
      try {
        const data = await getStartups();
        console.log("Data received:", data);
        setStartups(data);
      } catch (error) {
        console.error("Error fetching data:", error);
        setError("Error fetching data");
      } finally {
        setIsLoading(false);
      }
    }; // Debug: Log the error status

    fetchStartups();
  }, []);

  if (isLoading) {
    return <div className="p-8">Loading...</div>;
  }

  if (error) {
    return <div className="p-8 text-red-600">{error}</div>;
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-purple-200 via-purple-400 to-purple-600">
      <div className="max-w-[720px] w-full">
        <div className="relative flex flex-col w-full h-full bg-white shadow-md text-slate-700 rounded-xl bg-clip-border">
          <div className="relative mx-4 mt-4 overflow-hidden bg-white rounded-none text-slate-700 bg-clip-border">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold text-slate-800">
                  All Startups
                </h3>
                <p className="text-slate-500">Browse all startups data</p>
              </div>
              <div className="flex flex-col gap-2 shrink-0 sm:flex-row">
                <button
                  className="flex select-none items-center gap-2 rounded bg-slate-800 py-2.5 px-4 text-xs font-semibold text-white shadow-md shadow-slate-900/10 transition-all hover:shadow-lg hover:shadow-slate-900/20 focus:opacity-[0.85] focus:shadow-none active:opacity-[0.85] active:shadow-none disabled:pointer-events-none disabled:opacity-50 disabled:shadow-none"
                  type="button"
                  onClick={() => (window.location.href = "/")}
                >
                  Return
                </button>
              </div>
            </div>
          </div>

          <div className="p-0 overflow-scroll">
            <table className="w-full mt-4 text-left table-auto min-w-max">
              <thead>
                <tr>
                  <th className="p-4 transition-colors cursor-pointer border-y border-slate-200 bg-slate-50 hover:bg-slate-100">
                    Startup Name
                  </th>
                  <th className="p-4 transition-colors cursor-pointer border-y border-slate-200 bg-slate-50 hover:bg-slate-100">
                    Members
                  </th>
                  <th className="p-4 transition-colors cursor-pointer border-y border-slate-200 bg-slate-50 hover:bg-slate-100">
                    Website
                  </th>
                  <th className="p-4 transition-colors cursor-pointer border-y border-slate-200 bg-slate-50 hover:bg-slate-100">
                    Status
                  </th>
                  <th className="p-4 transition-colors cursor-pointer border-y border-slate-200 bg-slate-50 hover:bg-slate-100">
                    Meetings Count
                  </th>
                </tr>
              </thead>
              <tbody>
                {startups.length > 0 ? (
                  startups.map((startup) => (
                    <tr key={startup.StartupId}>
                      <td className="p-4 border-b border-slate-200">
                        {startup.StartupName}
                      </td>
                      <td className="p-4 border-b border-slate-200">
                        {startup.StartupMembers?.length > 0
                          ? startup.StartupMembers.map(member => member.name).join(", ") : "No members"}
                      </td>
                      <td className="p-4 border-b border-slate-200">
                        <a
                          href={startup.Website}
                          target="_blank"
                          rel="noreferrer"
                          className="text-blue-600 underline"
                        >
                          {startup.Website}
                        </a>
                      </td>
                      <td className="p-4 border-b border-slate-200">
                        {startup.Status}
                      </td>
                      <td className="p-4 border-b border-slate-200">
                        {startup.MeetingsCount}
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="5" className="p-4 text-center">
                      No data available
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AddStartupView;
