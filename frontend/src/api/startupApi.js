import axios from './axiosConfig';

export const getStartups = async () => {
  try {
    const response = await axios.get('/api/v1/startups/all');
    return response.data;
  } catch (error) {
    console.error('Error fetching startups:', error);
    throw error;
  }
};

export const addStartup = async (startupData) => {
  try {
    const response = await axios.post('/api/v1/startups', startupData);
    return response.data;
  } catch (error) {
    console.error('Error adding startup:', error);
    throw error;
  }
};