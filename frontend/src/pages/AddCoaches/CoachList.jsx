import React, { useState, useEffect } from 'react';
import { getCoaches } from '../../api/coachApi';

const CoachList = () => {
  const [coaches, setCoaches] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCoaches = async () => {
      try {
        const data = await getCoaches();

        console.log("Coaches:", data);

        setCoaches(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchCoaches();
  }, []);

  if (loading) {
    return <div>Loading coaches...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div className="coach-list">
      <h2>Coaches</h2>

      <ul>
        {coaches.map((coach) => (
          <li key={coach.CoachId}>
            <strong>
              {coach.Title && `${coach.Title} `}
              {coach.FirstName} {coach.LastName}
            </strong>
            <br />
            {coach.Email}
            <br />
            {coach.Expertise || "No expertise listed"}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CoachList;