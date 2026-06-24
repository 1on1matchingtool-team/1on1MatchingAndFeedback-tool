import React, { useState } from "react";
import { addCoach } from "../../api/coachApi";
import { useNavigate } from "react-router-dom";

const AddCoachPage = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    Title: "",
    FirstName: "",
    LastName: "",
    Email: "",

    Phone: "",
    Chat: "",

    Expertise: "",
    Bio: "",

    SocialMedia: {
      LinkedIn: "",
      GitHub: "",
      Facebook: "",
      Instagram: "",
      Twitter: ""
    },

    CoachingSessions: 0,
    BatchesCoached: 0
  });

  const [isLoading, setIsLoading] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSocialMediaChange = (platform, value) => {
    setFormData({
      ...formData,
      SocialMedia: {
        ...formData.SocialMedia,
        [platform]: value
      }
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      await addCoach(formData);
      alert('Coach created successfully!');
      navigate("/");
    } catch (error) {
      alert(
        error.response?.data?.error ||
        error.message
      );
    } finally {
      setIsLoading(false);
    }
  };

  const canSubmit =
    formData.FirstName.trim() &&
    formData.LastName.trim() &&
    formData.Email.trim();

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-100">
      {/* Header Section */}
      <div className="relative overflow-hidden bg-gradient-to-r from-emerald-900 to-teal-800">
        <div className="absolute inset-0">
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-transparent from-10% to-emerald-900/40"></div>
          <div className="absolute inset-0 bg-noise opacity-10"></div>
        </div>
        
        <div className="relative max-w-4xl px-4 py-16 mx-auto sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-4xl font-extrabold tracking-tight text-white sm:text-5xl lg:text-6xl">
              <span className="block">Add New</span>
              <span className="block text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-lime-400">
                Coach Profile
              </span>
            </h1>
            <p className="max-w-2xl mx-auto mt-6 text-xl text-emerald-200">
              Register a new coach to our network
            </p>
          </div>
        </div>
        
        <div className="absolute bottom-0 left-0 right-0 h-16 bg-gradient-to-t from-gray-50 to-transparent"></div>
      </div>

      {/* Main Form Section */}
      <div className="relative max-w-4xl px-4 py-16 mx-auto -mt-10 sm:px-6 lg:px-8">
        <div className="overflow-hidden bg-white border border-gray-100 shadow-2xl rounded-3xl">
          <div className="px-8 py-8">
            <div className="space-y-6">
              <div className="mb-8 text-center">
                <h3 className="mb-2 text-2xl font-bold text-gray-800">Coach Information</h3>
                <p className="text-gray-600">Enter the coach's professional details</p>
              </div>

              <div className="space-y-6">

                <div className="relative">
                  <label className="block mb-2 text-sm font-semibold text-gray-700">
                    Title
                  </label>

                  <select
                    name="Title"
                    value={formData.Title}
                    onChange={handleInputChange}
                    className="w-full px-4 py-4 text-gray-800 bg-white border-2 border-gray-200 shadow-sm rounded-xl focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100"
                  >
                    <option value="">Please select</option>
                    <option value="Mr.">Mr.</option>
                    <option value="Mrs.">Mrs.</option>
                    <option value="Ms.">Ms.</option>
                    <option value="Miss">Miss</option>
                    <option value="Dr.">Dr.</option>
                    <option value="Prof.">Prof.</option>
                    <option value="Sir">Sir</option>
                    <option value="Madam">Madam</option>
                    <option value="Coach">Coach</option>
                  </select>
                </div>

                <div className="relative">
                  <label>
                    First Name <span className="text-red-500">*</span>
                  </label>
                  <div className="relative">
                    <input
                      type="text"
                      name="FirstName"
                      placeholder="Josh"
                      value={formData.FirstName}
                      onChange={handleInputChange}
                      className="w-full px-4 py-4 text-gray-800 placeholder-gray-400 transition-all duration-300 bg-white border-2 border-gray-200 shadow-sm rounded-xl focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100"
                      required
                    />
                    <div className="absolute inset-y-0 right-0 flex items-center pr-4">
                      <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                      </svg>
                    </div>
                  </div>
                </div>

                <div className="relative">
                  <label>
                    Last Name <span className="text-red-500">*</span>
                  </label>
                  <div className="relative">
                    <input
                      type="text"
                      name="LastName"
                      placeholder="Smith"
                      value={formData.LastName}
                      onChange={handleInputChange}
                      className="w-full px-4 py-4 text-gray-800 placeholder-gray-400 transition-all duration-300 bg-white border-2 border-gray-200 shadow-sm rounded-xl focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100"
                      required
                    />
                    <div className="absolute inset-y-0 right-0 flex items-center pr-4">
                      <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                      </svg>
                    </div>
                  </div>
                </div>

                <div className="relative">
                  <label className="block mb-2 text-sm font-semibold text-gray-700">
                    Email <span className="text-red-500">*</span>
                  </label>

                  <div className="relative">
                    <input
                      type="email"
                      name="Email"
                      placeholder="coach@example.com"
                      value={formData.Email}
                      onChange={handleInputChange}
                      className="w-full px-4 py-4 text-gray-800 placeholder-gray-400 transition-all duration-300 bg-white border-2 border-gray-200 shadow-sm rounded-xl focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100"
                      required
                    />
                    <div className="absolute inset-y-0 right-0 flex items-center pr-4">
                      <svg
                        className="w-5 h-5 text-gray-400"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207"
                        />
                      </svg>
                    </div>
                  </div>
                </div>

                <div className="relative">
                  <label className="block mb-2 text-sm font-semibold text-gray-700">
                    Phone
                  </label>

                  <input
                    type="text"
                    name="Phone"
                    placeholder="+358401234567"
                    value={formData.Phone}
                    onChange={handleInputChange}
                    className="w-full px-4 py-4 text-gray-800 placeholder-gray-400 transition-all duration-300 bg-white border-2 border-gray-200 shadow-sm rounded-xl focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100"
                  />
                </div>

                <div className="relative">
                  <label className="block mb-2 text-sm font-semibold text-gray-700">
                    Preferred Chat
                  </label>

                  <input
                    type="text"
                    name="Chat"
                    placeholder="Telegram, Slack, WhatsApp..."
                    value={formData.Chat}
                    onChange={handleInputChange}
                    className="w-full px-4 py-4 text-gray-800 placeholder-gray-400 transition-all duration-300 bg-white border-2 border-gray-200 shadow-sm rounded-xl focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100"
                  />
                </div>

                <div className="relative">
                  <label className="block mb-2 text-sm font-semibold text-gray-700">
                    Areas of Expertise
                  </label>
                  <input
                    type="text"
                    name="Expertise"
                    placeholder="e.g., Product Management, Marketing, Fundraising"
                    value={formData.Expertise}
                    onChange={handleInputChange}
                    className="w-full px-4 py-4 text-gray-800 placeholder-gray-400 transition-all duration-300 bg-white border-2 border-gray-200 shadow-sm rounded-xl focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100"
                  />
                </div>

                <div className="relative">
                  <label className="block mb-2 text-sm font-semibold text-gray-700">
                    Professional Bio
                  </label>
                  <textarea
                    name="Bio"
                    placeholder="Tell us about the coach's background and expertise..."
                    value={formData.Bio}
                    onChange={handleInputChange}
                    rows={6}
                    className="w-full px-4 py-4 text-gray-800 placeholder-gray-400 transition-all duration-300 bg-white border-2 border-gray-200 shadow-sm resize-none rounded-xl focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100"
                  />
                  <div className="absolute bottom-4 right-4">
                    <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                  </div>
                </div>
              </div>

              <div className="pt-6 mt-6 border-t border-gray-200">
                <h3 className="mb-4 text-xl font-semibold text-gray-800">
                  Social Media
                </h3>
                <p className="mb-6 text-gray-600">
                  Add any social media profiles (all optional)
                </p>
              </div>

              <div className="relative mb-4">
                <label className="block mb-2 text-sm font-semibold text-gray-700">
                  LinkedIn
                </label>
                <input
                  type="url"
                  placeholder="https://linkedin.com/in/username"
                  value={formData.SocialMedia.LinkedIn}
                  onChange={(e) =>
                    handleSocialMediaChange("LinkedIn", e.target.value)
                  }
                  className="w-full px-4 py-4 text-gray-800 placeholder-gray-400 transition-all duration-300 bg-white border-2 border-gray-200 shadow-sm rounded-xl focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100"
                />
              </div>

              <div className="relative mb-4">
                <label className="block mb-2 text-sm font-semibold text-gray-700">
                  GitHub
                </label>
                <input
                  type="url"
                  placeholder="https://github.com/username"
                  value={formData.SocialMedia.GitHub}
                  onChange={(e) =>
                    handleSocialMediaChange("GitHub", e.target.value)
                  }
                  className="w-full px-4 py-4 text-gray-800 placeholder-gray-400 transition-all duration-300 bg-white border-2 border-gray-200 shadow-sm rounded-xl focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100"
                />
              </div>

              <div className="relative mb-4">
                <label className="block mb-2 text-sm font-semibold text-gray-700">
                  Facebook
                </label>
                <input
                  type="url"
                  placeholder="https://facebook.com/username"
                  value={formData.SocialMedia.Facebook}
                  onChange={(e) =>
                    handleSocialMediaChange("Facebook", e.target.value)
                  }
                  className="w-full px-4 py-4 text-gray-800 placeholder-gray-400 transition-all duration-300 bg-white border-2 border-gray-200 shadow-sm rounded-xl focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100"
                />
              </div>

              <div className="relative mb-4">
                <label className="block mb-2 text-sm font-semibold text-gray-700">
                  Instagram
                </label>
                <input
                  type="url"
                  placeholder="https://instagram.com/username"
                  value={formData.SocialMedia.Instagram}
                  onChange={(e) =>
                    handleSocialMediaChange("Instagram", e.target.value)
                  }
                  className="w-full px-4 py-4 text-gray-800 placeholder-gray-400 transition-all duration-300 bg-white border-2 border-gray-200 shadow-sm rounded-xl focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100"
                />
              </div>

              <div className="relative">
                <label className="block mb-2 text-sm font-semibold text-gray-700">
                  Twitter / X
                </label>
                <input
                  type="url"
                  placeholder="https://x.com/username"
                  value={formData.SocialMedia.Twitter}
                  onChange={(e) =>
                    handleSocialMediaChange("Twitter", e.target.value)
                  }
                  className="w-full px-4 py-4 text-gray-800 placeholder-gray-400 transition-all duration-300 bg-white border-2 border-gray-200 shadow-sm rounded-xl focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100"
                />
              </div>

              {/* Submit Button */}
              <div className="flex items-center justify-between pt-6 mt-8 border-t border-gray-100">
                <button
                  type="submit"
                  onClick={() => window.location.href = '/'}
                  className="px-6 py-3 font-semibold text-gray-600 transition-all duration-300 bg-gray-100 shadow-sm rounded-xl hover:bg-gray-200 hover:shadow"
                >
                  <div className="flex items-center">
                    <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                    </svg>
                    Back to Home
                  </div>
                </button>

                <button
                  type="button"
                  onClick={handleSubmit}
                  disabled={isLoading || !canSubmit}
                  className={`px-8 py-3 rounded-xl font-semibold transition-all duration-300 ${
                    canSubmit && !isLoading
                      ? 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white hover:from-emerald-700 hover:to-teal-700 shadow-lg hover:shadow-xl'
                      : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                  }`}
                >
                  <div className="flex items-center">
                    {isLoading ? (
                      <>
                        <svg className="w-4 h-4 mr-3 -ml-1 text-white animate-spin" fill="none" viewBox="0 0 24 24">
                          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        Creating...
                      </>
                    ) : (
                      'Create Coach Profile'
                    )}
                  </div>
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Trust Indicators */}
        <div className="mt-16 text-center">
          <p className="mb-6 text-sm text-gray-500">Join our network of experienced coaches</p>
          <div className="flex items-center justify-center space-x-8 opacity-40">
            <div className="px-6 py-3 bg-gray-200 rounded-lg">
              <span className="text-xs font-semibold text-gray-600">100+ COACHES</span>
            </div>
            <div className="px-6 py-3 bg-gray-200 rounded-lg">
              <span className="text-xs font-semibold text-gray-600">1000+ SESSIONS</span>
            </div>
            <div className="px-6 py-3 bg-gray-200 rounded-lg">
              <span className="text-xs font-semibold text-gray-600">4.9/5 RATING</span>
            </div>
          </div>
        </div>
      </div>

      {/* Background Elements */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none -z-10">
        <div className="absolute rounded-full bg-emerald-300 top-1/4 left-1/4 w-96 h-96 mix-blend-multiply filter blur-3xl opacity-5"></div>
        <div className="absolute bg-teal-300 rounded-full top-1/3 right-1/4 w-96 h-96 mix-blend-multiply filter blur-3xl opacity-5"></div>
        <div className="absolute bg-green-300 rounded-full bottom-1/4 left-1/2 w-96 h-96 mix-blend-multiply filter blur-3xl opacity-5"></div>
      </div>

    </div>
  );
};

export default AddCoachPage;