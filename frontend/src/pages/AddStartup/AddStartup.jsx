import React, { useState } from "react";
import { addStartup } from "../../api/startupApi";
import { useNavigate } from "react-router-dom";

const AddStartup = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    StartupName: "",
    Website: "",
    Status: "alive",

    StartupDescription: "",
    PreviousNames: "",

    StartupMembers: [
      {
        Name: "",
        Email: "",
        Phone: "",
        Role: "",
        Level: ""
      }
    ],

    StartupSocialMedia: {
      LinkedIn: "",
      GitHub: "",
      Facebook: "",
      Instagram: "",
      Twitter: ""
    }
  });

  const [isLoading, setIsLoading] = useState(false);
  const [currentStep, setCurrentStep] = useState(1);
  const totalSteps = 3;

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleMemberChange = (index, field, value) => {
    const updatedMembers = [...formData.StartupMembers];
    updatedMembers[index] = {
      ...updatedMembers[index],
      [field]: value
    };
    setFormData({
      ...formData,
      StartupMembers: updatedMembers
    });
  };

  const addMember = () => {
    setFormData({
      ...formData,
      StartupMembers: [
        ...formData.StartupMembers,
        {
          Name: "",
          Email: "",
          Phone: "",
          Role: "",
          Level: ""
        }
      ]
    });
  };

  const removeMember = (index) => {
    if (formData.StartupMembers.length === 1) return;

    setFormData({
      ...formData,
      StartupMembers: formData.StartupMembers.filter(
        (_, i) => i !== index
      )
    });
  };

  const handleSocialMediaChange = (platform, value) => {
    setFormData({
      ...formData,
      StartupSocialMedia: {
        ...formData.StartupSocialMedia,
        [platform]: value
      }
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const payload = {
        StartupName: formData.StartupName.trim(),
        Website: formData.Website.trim(),
        Status: formData.Status,
        PreviousNames: formData.PreviousNames
          ? formData.PreviousNames
              .split(",")
              .map(name => name.trim())
              .filter(Boolean)
          : [],

        StartupMembers: formData.StartupMembers.map(member => ({
          name: member.Name.trim(),
          email: member.Email.trim(),
          phone: member.Phone.trim(),
          role: member.Role.trim(),
          level: member.Level.trim()
        })),

        StartupSocialMedia: formData.StartupSocialMedia,
        StartupDescription: formData.StartupDescription.trim()
      };

      await addStartup(payload);

      alert("Startup added successfully!");

      navigate("/");
    } catch (error) {
      console.error("Error adding startup:", error);
      alert("Failed to add startup.");
    } finally {
      setIsLoading(false);
    }
  };

  const nextStep = (e) => {
    if (e) {
        e.preventDefault();
        e.stopPropagation();
    }
    console.log("NEXT STEP", currentStep);
    if (currentStep < totalSteps) {
        setCurrentStep(prev => prev + 1);
    }
  };

  const prevStep = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const canProceed = () => {
    if (currentStep === 1) {
      return (
        formData.StartupName.trim() !== "" &&
        formData.Website.trim() !== "" &&
        formData.StartupMembers[0].Name.trim() !== "" &&
        formData.StartupMembers[0].Email.trim() !== ""
      );
    }

    return true;
  };

  const renderStepContent = () => {
    switch (currentStep) {
      case 1:
        return (
          <div className="space-y-6">
            <div className="mb-8 text-center">
              <h3 className="mb-2 text-2xl font-bold text-gray-800">Basic Information</h3>
              <p className="text-gray-600">Let's start with the essentials about your startup</p>
            </div>

            <div className="space-y-6">
              <div className="relative">
                <label className="block mb-2 text-sm font-semibold text-gray-700">
                  Startup Name <span className="text-red-500">*</span>
                </label>
                <div className="relative">
                  <input
                    type="text"
                    name="StartupName"
                    placeholder="Enter your startup name"
                    value={formData.StartupName}
                    onChange={handleInputChange}
                    className="w-full px-4 py-4 text-gray-800 placeholder-gray-400 transition-all duration-300 bg-white border-2 border-gray-200 shadow-sm rounded-xl focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100"
                    required
                  />
                  <div className="absolute inset-y-0 right-0 flex items-center pr-4">
                    <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                    </svg>
                  </div>
                </div>
              </div>

              <div className="relative">
                <div className="relative">
                  <label className="block mb-2 text-sm font-semibold text-gray-700">
                    Website <span className="text-red-500">*</span>
                  </label>

                  <input
                    type="url"
                    name="Website"
                    placeholder="https://yourstartup.com"
                    value={formData.Website}
                    onChange={handleInputChange}
                    className="w-full px-4 py-4 text-gray-800 placeholder-gray-400 transition-all duration-300 bg-white border-2 border-gray-200 shadow-sm rounded-xl focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100"
                    required
                  />
                </div>
              </div>

              <div className="relative">
                <label className="block mb-2 text-sm font-semibold text-gray-700">
                  Status <span className="text-red-500">*</span>
                </label>

                <select
                  name="Status"
                  value={formData.Status}
                  onChange={handleInputChange}
                  className="w-full px-4 py-4 text-gray-800 bg-white border-2 border-gray-200 shadow-sm rounded-xl focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100"
                >
                  <option value="alive">Alive</option>
                  <option value="on-pause">On-pause</option>
                  <option value="dead">Dead</option>
                </select>
              </div>

              {formData.StartupMembers.map((member, index) => (
                <div
                  key={index}
                  className="pt-4 mt-6 border-t border-gray-200"
                >
                  <div className="flex items-center justify-between mb-4">
                    <h4 className="text-lg font-semibold text-gray-800">
                      {index === 0
                        ? "Primary Startup Member"
                        : `Startup Member ${index + 1}`}
                    </h4>

                    {formData.StartupMembers.length > 1 && (
                      <button
                        type="button"
                        onClick={() => removeMember(index)}
                        className="text-sm font-medium text-red-600 hover:text-red-700"
                      >
                        Remove
                      </button>
                    )}
                  </div>

              <div className="relative">
                <label className="block mb-2 text-sm font-semibold text-gray-700">
                  Member Name <span className="text-red-500">*</span>
                </label>

                <input
                  type="text"
                  placeholder="John Smith"
                  value={member.Name}
                  onChange={(e) =>
                    handleMemberChange(index, "Name", e.target.value)
                  }
                  className="w-full px-4 py-4 text-gray-800 placeholder-gray-400 transition-all duration-300 bg-white border-2 border-gray-200 shadow-sm rounded-xl focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100"
                  required
                />
              </div>

              <div className="relative">
                <label className="block mb-2 text-sm font-semibold text-gray-700">
                  Member Email <span className="text-red-500">*</span>
                </label>

                <div className="relative">
                  <input
                    type="email"
                    placeholder="member@yourstartup.com"
                    value={member.Email}
                    onChange={(e) =>
                      handleMemberChange(index, "Email", e.target.value)
                    }
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
                  Member Phone
                </label>

                <input
                  type="text"
                  placeholder="+358401234567"
                  value={member.Phone}
                  onChange={(e) =>
                    handleMemberChange(index, "Phone", e.target.value)
                  }
                  className="w-full px-4 py-4 text-gray-800 placeholder-gray-400 transition-all duration-300 bg-white border-2 border-gray-200 shadow-sm rounded-xl focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100"
                />
              </div>

              <div className="relative">
                <label className="block mb-2 text-sm font-semibold text-gray-700">
                  Member Role
                </label>

                <input
                  type="text"
                  placeholder="Founder, CTO, CEO..."
                  value={member.Role}
                  onChange={(e) =>
                    handleMemberChange(index, "Role", e.target.value)
                  }
                  className="w-full px-4 py-4 text-gray-800 placeholder-gray-400 transition-all duration-300 bg-white border-2 border-gray-200 shadow-sm rounded-xl focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100"
                />
              </div>

              <div className="relative">
                <label className="block mb-2 text-sm font-semibold text-gray-700">
                  Member Level
                </label>

                <input
                  type="text"
                  placeholder="Senior, Junior, Executive..."
                  value={member.Level}
                  onChange={(e) =>
                    handleMemberChange(index, "Level", e.target.value)
                  }
                  className="w-full px-4 py-4 text-gray-800 placeholder-gray-400 transition-all duration-300 bg-white border-2 border-gray-200 shadow-sm rounded-xl focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100"
                />
              </div>
            </div>
          ))}
          <div className="pt-4">
            <button
              type="button"
              onClick={addMember}
              className="px-5 py-3 text-white bg-indigo-600 rounded-xl hover:bg-indigo-700 transition"
            >
              + Add Another Member
            </button>
          </div>

        </div>
      </div>
    );

      case 2:
        return (
          <div className="space-y-6">
            <div className="mb-8 text-center">
              <h3 className="mb-2 text-2xl font-bold text-gray-800">Tell Your Story</h3>
              <p className="text-gray-600">Help us understand what makes your startup unique</p>
            </div>

            <div className="relative">
              <label className="block mb-2 text-sm font-semibold text-gray-700">
                Startup Description
              </label>
              <textarea
                name="StartupDescription"
                placeholder="Describe your startup's mission, vision, and what problem you're solving..."
                value={formData.StartupDescription}
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
        );

      case 3:
        return (
          <div className="space-y-6">
            <div className="mb-8 text-center">
              <h3 className="mb-2 text-2xl font-bold text-gray-800">
                Online Presence
              </h3>
              <p className="text-gray-600">
                Add any social media links your startup uses (all optional)
              </p>
            </div>

            <div className="space-y-5">

              <div>
                <label className="block mb-2 text-sm font-semibold text-gray-700">
                  LinkedIn
                </label>
                <input
                  type="url"
                  name="LinkedIn"
                  placeholder="https://linkedin.com/company/yourstartup"
                  value={formData.StartupSocialMedia.LinkedIn}
                  onChange={(e) =>
                    handleSocialMediaChange("LinkedIn", e.target.value)
                  }
                  className="w-full px-4 py-4 text-gray-800 border-2 border-gray-200 rounded-xl focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100"
                />
              </div>

              <div>
                <label className="block mb-2 text-sm font-semibold text-gray-700">
                  GitHub
                </label>
                <input
                  type="url"
                  name="GitHub"
                  placeholder="https://github.com/yourstartup"
                  value={formData.StartupSocialMedia.GitHub}
                  onChange={(e) =>
                    handleSocialMediaChange("GitHub", e.target.value)
                  }
                  className="w-full px-4 py-4 text-gray-800 border-2 border-gray-200 rounded-xl focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100"
                />
              </div>

              <div>
                <label className="block mb-2 text-sm font-semibold text-gray-700">
                  Facebook
                </label>
                <input
                  type="url"
                  name="Facebook"
                  placeholder="https://facebook.com/yourstartup"
                  value={formData.StartupSocialMedia.Facebook}
                  onChange={(e) =>
                    handleSocialMediaChange("Facebook", e.target.value)
                  }
                  className="w-full px-4 py-4 text-gray-800 border-2 border-gray-200 rounded-xl focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100"
                />
              </div>

              <div>
                <label className="block mb-2 text-sm font-semibold text-gray-700">
                  Instagram
                </label>
                <input
                  type="url"
                  name="Instagram"
                  placeholder="https://instagram.com/yourstartup"
                  value={formData.StartupSocialMedia.Instagram}
                  onChange={(e) =>
                    handleSocialMediaChange("Instagram", e.target.value)
                  }
                  className="w-full px-4 py-4 text-gray-800 border-2 border-gray-200 rounded-xl focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100"
                />
              </div>

              <div>
                <label className="block mb-2 text-sm font-semibold text-gray-700">
                  Twitter / X
                </label>
                <input
                  type="url"
                  name="Twitter"
                  placeholder="https://x.com/yourstartup"
                  value={formData.StartupSocialMedia.Twitter}
                  onChange={(e) =>
                    handleSocialMediaChange("Twitter", e.target.value)
                  }
                  className="w-full px-4 py-4 text-gray-800 border-2 border-gray-200 rounded-xl focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100"
                />
              </div>

            </div>
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-100">
      {/* Header Section */}
      <div className="relative overflow-hidden bg-gradient-to-r from-indigo-900 to-purple-800">
        <div className="absolute inset-0">
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-transparent from-10% to-indigo-900/40"></div>
          <div className="absolute inset-0 bg-noise opacity-10"></div>
        </div>
        
        <div className="relative max-w-4xl px-4 py-16 mx-auto sm:px-6 lg:px-8">
          <div className="text-center">
            <div className="inline-block mb-4">
              <span className="px-4 py-2 text-sm font-semibold tracking-wider text-indigo-100 uppercase rounded-full bg-indigo-700/50 backdrop-blur-sm">
                Join Our Ecosystem
              </span>
            </div>
            <h1 className="text-4xl font-extrabold tracking-tight text-white sm:text-5xl lg:text-6xl">
              <span className="block">Register Your</span>
              <span className="block text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-emerald-400">
                Startup Today
              </span>
            </h1>
            <p className="max-w-2xl mx-auto mt-6 text-xl text-indigo-200">
              Join thousands of innovative startups in our AI-powered acceleration platform
            </p>
          </div>
        </div>
        
        <div className="absolute bottom-0 left-0 right-0 h-16 bg-gradient-to-t from-gray-50 to-transparent"></div>
      </div>

      {/* Main Form Section */}
      <div className="relative max-w-4xl px-4 py-16 mx-auto -mt-10 sm:px-6 lg:px-8">
        <div className="overflow-hidden bg-white border border-gray-100 shadow-2xl rounded-3xl">
          {/* Progress Bar */}
          <div className="px-8 py-6 border-b border-gray-100 bg-gradient-to-r from-indigo-50 to-purple-50">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-800">Registration Progress</h2>
              <span className="text-sm font-medium text-gray-600">
                Step {currentStep} of {totalSteps}
              </span>
            </div>
            <div className="flex space-x-4">
              {[1, 2, 3].map((step) => (
                <div key={step} className="flex-1">
                  <div className={`h-2 rounded-full transition-all duration-300 ${
                    step <= currentStep ? 'bg-gradient-to-r from-indigo-500 to-purple-500' : 'bg-gray-200'
                  }`} />
                  <div className="mt-2 text-xs font-medium text-center">
                    <span className={step <= currentStep ? 'text-indigo-600' : 'text-gray-400'}>
                      {step === 1 && 'Basic Info'}
                      {step === 2 && 'Description'}
                      {step === 3 && 'Online Presence'}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Form Content */}
          <form
            className="px-8 py-8"
            onSubmit={handleSubmit}
          >
            {renderStepContent()}

            {/* Navigation Buttons */}
            <div className="flex items-center justify-between pt-6 mt-8 border-t border-gray-100">
              <button
                type="button"
                onClick={prevStep}
                disabled={currentStep === 1}
                className={`px-6 py-3 rounded-xl font-semibold transition-all duration-300 ${
                  currentStep === 1
                    ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300 shadow-sm hover:shadow'
                }`}
              >
                <div className="flex items-center">
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                  </svg>
                  Previous
                </div>
              </button>

              <div className="flex space-x-4">
                <button
                  type="button"
                  onClick={() => navigate("/")}
                  className="px-6 py-3 font-semibold text-gray-600 transition-all duration-300 bg-gray-100 shadow-sm rounded-xl hover:bg-gray-200 hover:shadow"
                >
                  Cancel
                </button>

                {currentStep < totalSteps ? (
                  <button
                    type="button"
                    onClick={(e) => nextStep(e)}
                    disabled={!canProceed()}
                    className={`px-8 py-3 rounded-xl font-semibold transition-all duration-300 ${
                      canProceed()
                        ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white hover:from-indigo-700 hover:to-purple-700 shadow-lg hover:shadow-xl'
                        : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                    }`}
                  >
                    <div className="flex items-center">
                      Continue
                      <svg className="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                      </svg>
                    </div>
                  </button>
                ) : (
                  <button
                    type="submit"
                    disabled={isLoading || !canProceed()}
                    className={`px-8 py-3 rounded-xl font-semibold transition-all duration-300 ${
                      !isLoading && canProceed()
                        ? 'bg-gradient-to-r from-emerald-600 to-cyan-600 text-white hover:from-emerald-700 hover:to-cyan-700 shadow-lg hover:shadow-xl'
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
                          Registering...
                        </>
                      ) : (
                        <>
                          <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                          </svg>
                          Complete Registration
                        </>
                      )}
                    </div>
                  </button>
                )}
              </div>
            </div>
          </form>
        </div>

        {/* Trust Indicators */}
        <div className="mt-16 text-center">
          <p className="mb-6 text-sm text-gray-500">Trusted by innovative startups worldwide</p>
          <div className="flex items-center justify-center space-x-8 opacity-40">
            <div className="px-6 py-3 bg-gray-200 rounded-lg">
              <span className="text-xs font-semibold text-gray-600">500+ STARTUPS</span>
            </div>
            <div className="px-6 py-3 bg-gray-200 rounded-lg">
              <span className="text-xs font-semibold text-gray-600">50+ COUNTRIES</span>
            </div>
            <div className="px-6 py-3 bg-gray-200 rounded-lg">
              <span className="text-xs font-semibold text-gray-600">95% SUCCESS RATE</span>
            </div>
          </div>
        </div>
      </div>

      {/* Background Elements */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none -z-10">
        <div className="absolute bg-indigo-300 rounded-full top-1/4 left-1/4 w-96 h-96 mix-blend-multiply filter blur-3xl opacity-5"></div>
        <div className="absolute bg-purple-300 rounded-full top-1/3 right-1/4 w-96 h-96 mix-blend-multiply filter blur-3xl opacity-5"></div>
        <div className="absolute rounded-full bg-cyan-300 bottom-1/4 left-1/2 w-96 h-96 mix-blend-multiply filter blur-3xl opacity-5"></div>
      </div>

      {/* Global Styles */}
      <style>{`
        .bg-noise {
          background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%' height='100%' filter='url(%23noiseFilter)' opacity='0.2'/%3E%3C/svg%3E");
        }
      `}</style>
    </div>
  );
};

export default AddStartup;