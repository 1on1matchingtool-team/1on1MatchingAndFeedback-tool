import React from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

export default function Home({ onLogout }) {
  const navigate = useNavigate();
  
  // Simplified stats data
  const stats = {
    totalStartups: 247,
    totalCoaches: 89,
    activeMatches: 156,
    pendingReviews: 12
  };

  // Updated quick actions with View All Coaches option
  const quickActions = [
    {
      title: "Add New Startup",
      subtitle: "Register company",
      icon: "M12 6v6m0 0v6m0-6h6m-6 0H6",
      action: () => navigate("/add-startup"),
      gradient: "from-blue-500 to-blue-600",
      bgGradient: "from-blue-50 to-blue-100",
      iconBg: "bg-blue-500"
    },
    {
      title: "View All Startups",
      subtitle: "Browse companies",
      icon: "M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4",
      action: () => navigate("/view-startups"),
      gradient: "from-cyan-500 to-cyan-600",
      bgGradient: "from-cyan-50 to-cyan-100",
      iconBg: "bg-cyan-500"
    },
    {
      title: "Onboard Coach",
      subtitle: "Add new mentor",
      icon: "M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z",
      action: () => navigate("/add-coaches"),
      gradient: "from-emerald-500 to-emerald-600",
      bgGradient: "from-emerald-50 to-emerald-100",
      iconBg: "bg-emerald-500"
    },
    {
      title: "View All Coaches",
      subtitle: "Browse mentors",
      icon: "M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z",
      action: () => navigate("/view-coaches"),
      gradient: "from-indigo-500 to-indigo-600",
      bgGradient: "from-indigo-50 to-indigo-100",
      iconBg: "bg-indigo-500"
    },
    {
      title: "Set Availability",
      subtitle: "Coach time slots",
      icon: "M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z",
      action: () => navigate("/coach-availability"),
      gradient: "from-amber-500 to-amber-600",
      bgGradient: "from-amber-50 to-amber-100",
      iconBg: "bg-amber-500"
    },
    {
      title: "AI Matching",
      subtitle: "Run algorithm",
      icon: "M13 10V3L4 14h7v7l9-11h-7z",
      action: () => navigate("/start-matching"),
      gradient: "from-purple-500 to-purple-600",
      bgGradient: "from-purple-50 to-purple-100",
      iconBg: "bg-purple-500"
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      {/* Header */}
      <div className="sticky top-0 z-10 border-b shadow-sm bg-white/80 backdrop-blur-lg border-gray-200/50">
        <div className="px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="flex items-center justify-center w-10 h-10 shadow-lg bg-gradient-to-r from-indigo-600 to-purple-600 rounded-xl">
                <svg xmlns="http://www.w3.org/2000/svg" className="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
                </svg>
              </div>
              <div>
                <h1 className="text-2xl font-bold text-transparent bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text">
                  Admin Dashboard
                </h1>
                <p className="text-sm font-medium text-gray-600">Sampo Acceleration Suite</p>
              </div>
            </div>
            <div className="flex items-center space-x-6">
              <div className="text-sm font-medium text-gray-500">
                {new Date().toLocaleString()}
              </div>

              <button
                onClick={onLogout}
                className="px-4 py-2 text-sm font-medium text-gray-700 transition-colors bg-white border border-gray-200 rounded-lg hover:bg-gray-50"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="p-8 mx-auto max-w-7xl">
        {/* Quick Actions */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="p-8 mb-8 bg-white border shadow-xl rounded-2xl border-white/20"
        >
          <h2 className="mb-6 text-2xl font-bold text-gray-800">Quick Actions</h2>
          <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
            {quickActions.map((action, index) => (
              <motion.button
                key={index}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={action.action}
                className={`p-6 rounded-2xl bg-gradient-to-br ${action.bgGradient} border border-white/50 shadow-lg transition-all duration-300`}
              >
                <div className={`w-12 h-12 ${action.iconBg} rounded-xl shadow-lg mb-4 flex items-center justify-center`}>
                  <svg xmlns="http://www.w3.org/2000/svg" className="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={action.icon} />
                  </svg>
                </div>
                <h3 className="mb-1 text-lg font-bold text-gray-800">{action.title}</h3>
                <p className="text-sm font-medium text-gray-600">{action.subtitle}</p>
              </motion.button>
            ))}
          </div>
        </motion.div>

        {/* Stats Overview */}
        <div className="grid grid-cols-1 gap-6 mb-8 md:grid-cols-2 lg:grid-cols-4">
          {[
            { 
              title: "Total Startups", 
              value: stats.totalStartups, 
              icon: "M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4",
              gradient: "from-blue-500 to-blue-600"
            },
            { 
              title: "Active Coaches", 
              value: stats.totalCoaches, 
              icon: "M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z",
              gradient: "from-emerald-500 to-emerald-600"
            },
            { 
              title: "Active Matches", 
              value: stats.activeMatches, 
              icon: "M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z",
              gradient: "from-purple-500 to-purple-600"
            },
            { 
              title: "Pending Reviews", 
              value: stats.pendingReviews, 
              icon: "M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z",
              gradient: "from-orange-500 to-orange-600"
            }
          ].map((stat, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className={`p-6 text-white shadow-lg rounded-2xl bg-gradient-to-br ${stat.gradient}`}
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="mb-1 text-sm font-medium">{stat.title}</p>
                  <p className="text-3xl font-bold">{stat.value}</p>
                </div>
                <div className="p-3 bg-white/20 rounded-xl">
                  <svg xmlns="http://www.w3.org/2000/svg" className="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={stat.icon} />
                  </svg>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
}