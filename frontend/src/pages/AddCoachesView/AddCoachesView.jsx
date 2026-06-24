import React, { useEffect, useState } from "react";
import { getCoaches } from "../../api/coachApi";

const AddCoachesView = () => {
  const [coaches, setCoaches] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCoaches = async () => {
      try {
        const data = await getCoaches();
        console.log("Coaches:", data);
        setCoaches(data);
      } catch (err) {
        console.error(err);
        setError("Error fetching coaches");
      } finally {
        setIsLoading(false);
      }
    };

    fetchCoaches();
  }, []);

  if (isLoading) {
    return <div className="p-8">Loading...</div>;
  }

  if (error) {
    return <div className="p-8 text-red-600">{error}</div>;
  }

  return (
    <div
        className="flex items-center justify-center min-h-screen bg-gradient-to-br from-purple-200 via-purple-400 to-purple-600">
      <div className="max-w-[720px] w-full">
        <div className="relative flex flex-col w-full h-full bg-white shadow-md text-slate-700 rounded-xl bg-clip-border">

          <div className="relative mx-4 mt-4 overflow-hidden bg-white rounded-none text-slate-700 bg-clip-border">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold text-slate-800">
                  All Coaches
                </h3>
                <p className="text-slate-500">
                  Browse all coaches
                </p>
              </div>

              <button
                  className="flex select-none items-center gap-2 rounded bg-slate-800 py-2.5 px-4 text-xs font-semibold text-white shadow-md shadow-slate-900/10 transition-all hover:shadow-lg hover:shadow-slate-900/20 focus:opacity-[0.85] focus:shadow-none active:opacity-[0.85] active:shadow-none disabled:pointer-events-none disabled:opacity-50 disabled:shadow-none"
                  onClick={() => (window.location.href = "/")}
              >
                Return
              </button>
            </div>
          </div>

          <div className="p-0 overflow-scroll">
            <table className="w-full mt-4 text-left table-auto min-w-max">
              <thead>
                <tr>
                  <th className="p-4 transition-colors cursor-pointer border-y border-slate-200 bg-slate-50 hover:bg-slate-100">
                    Name
                  </th>

                  <th className="p-4 transition-colors cursor-pointer border-y border-slate-200 bg-slate-50 hover:bg-slate-100">
                    Email
                  </th>

                  <th className="p-4 transition-colors cursor-pointer border-y border-slate-200 bg-slate-50 hover:bg-slate-100">
                    Phone
                  </th>

                  <th className="p-4 transition-colors cursor-pointer border-y border-slate-200 bg-slate-50 hover:bg-slate-100">
                    Expertise
                  </th>

                  <th className="p-4 transition-colors cursor-pointer border-y border-slate-200 bg-slate-50 hover:bg-slate-100">
                    Coaching Sessions
                  </th>
                </tr>
              </thead>
              <tbody>
                {coaches.length > 0 ? (
                  coaches.map((coach) => (
                    <tr key={coach.CoachId}>
                      <td className="p-4 border-b border-slate-200">
                        {coach.Title && `${coach.Title} `}
                        {coach.FirstName} {coach.LastName}
                      </td>

                      <td className="p-4 border-b border-slate-200">
                        {coach.Email}
                      </td>

                      <td className="p-4 border-b border-slate-200">
                        {coach.Phone || "-"}
                      </td>

                      <td className="p-4 border-b border-slate-200">
                        {coach.Expertise || "No expertise listed"}
                      </td>

                      <td className="p-4 border-b border-slate-200">
                        {coach.CoachingSessions}
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="5" className="p-4 text-center">
                      No coaches found
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

export default AddCoachesView;