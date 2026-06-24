import axios from './axiosConfig';

export const getCoaches = async () => {
  try {
    const response = await axios.get('/api/v1/coaches/all');
    return response.data;
  } catch (error) {
    console.error('Error fetching coaches:', error);
    throw error;
  }
};

export const addCoach = async (coachData) => {
  try {
    const response = await axios.post('/api/v1/coaches', coachData);
    return response.data;
  } catch (error) {
    console.error('Error adding coach:', error);
    throw error;
  }
};