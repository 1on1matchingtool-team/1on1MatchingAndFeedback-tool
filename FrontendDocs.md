# Frontend Documentation
#### Updated 24 June 2026


## Table of Contents

1. [Overview](#1-overview)
2. [Folder Structure](#2-folder-structure)
3. [Technology Stack](#3-technology-stack)
4. [Application Routing](#4-application-routing)
5. [Authentication](#5-authentication)
6. [Pages and Components](#6-pages-and-components)
7. [API Integration](#7-api-integration)
8. [Styling](#8-styling)
9. [Environment Variables](#9-environment-variables)
10. [Future Improvements](#10-future-improvements)

---

## 1. Overview

The frontend of the **1on1MatchingAndFeedbackTool** is built with React and Tailwind CSS, providing separate interfaces for administrators and startup users through a responsive single-page application.
It uses React Router for client-side routing, Google OAuth for user authentication, and communicates with the Flask backend through REST APIs to manage startups, coaches, scheduling, and matching data.
Additionally, it includes role-based navigation, protected routes, an administrative dashboard, user dashboard, and modern UI components to support the complete coaching and matching workflow.

---

## 2. Folder Structure

```
frontend/
├── app/
│   ├── components/
│   │   └── LoginForm.jsx
├── public/
│   ├── index.html
│   ├── favicon.ico
│   └── manifest.json
├── src/
│   ├── api/
│   │   ├── axiosConfig.js
│   │   ├── coachApi.js
│   │   └── startupApi.js
│   ├── pages/
│   │   ├── AddCoaches/
│   │   │   ├── AddCoaches.jsx
│   │   │   ├── AddTime.jsx
│   │   │   └── CoachesList.jsx
│   │   ├── AddCoachesView/
│   │   │   └── AddCoachesView.jsx
│   │   ├── AddStartup/
│   │   │   └── AddStartup.jsx
│   │   ├── AddStartupView/
│   │   │   └── AddStartupView.jsx
│   │   ├── Home/
│   │   │   └── Home.jsx
│   │   ├── login/
│   │   │   ├── AdminLogin.jsx
│   │   │   ├── googleauth.jsx
│   │   │   ├── LoginPage.jsx
│   │   │   └── SignupPage.jsx
│   │   ├── StartMatching/
│   │   ├── UserHome/
│   │   │   ├── UserHome.jsx
│   │   │   └── UserProfile.jsx
│   ├── App.js
│   ├── index.js
│   ├── index.css
│   └── reportWebVitals.js
├── architecture.md
└── tailwind.config.js

```

---

## 3. Technology Stack

The frontend is built with React in a component-based structure, interacting with a Flask backend via REST APIs. It features role-based authentication and employs Google OAuth for user login, while styling is achieved through Tailwind CSS and contemporary UI libraries for a responsive user experience.

### 3.1 React

The application is built with React using functional components and React Hooks.

**Features:**
- Component-based architecture
- React Hooks (useState, useEffect)
- Client-side rendering
- Reusable page and component structure

### 3.2 React Router

Navigation is managed with react-router-dom.

**Features:**
- Public and protected routes
- Role-based routing (Admin/User)
- Automatic redirects after login/logout
- Route guards using `ProtectedRoute` and `UserRoute`

### 3.3 Authentication

Authentication combines Google OAuth and local application state.

**Features:**
- Google OAuth integration
- Admin login support
- User login support
- Authentication persistence using `localStorage`
- Logout functionality with session cleanup

### 3.4 API Communication

Communication with the backend is handled using Axios.

**Features:**
- Centralized Axios configuration
- Startup API module
- Coach API module
- REST API communication with the Flask backend

### 3.5 Styling and UI

The user interface uses Tailwind CSS together with additional React UI libraries.

**Features:**
- Tailwind CSS utility classes
- Responsive layouts
- Framer Motion page animations
- Lucide React icons
- Modern dashboard interface

### 3.6 State Management

The current application uses React's built-in state management.

**Features:**
- useState for component state
- Role and User session management
- Local storage synchronization

### 3.7 Development Tools

The frontend is developed using the standard React development environment. 

**Technologies:**
- Node.js
- npm
- Create React App
- ESLint

---

## 4. Application Routing

The application utilizes **React Router** for page navigation, with routing centralized in `App.js`. This includes configurations for public routes, protected routes, and role-based access control. Authentication state is stored in `localStorage`, enabling users to stay signed in after refreshing the browser until they log out.

### 4.1 Public Routes

These routes are accessible without authentication.

| Route         | Component        | Description                            |
| ------------- | ---------------- | -------------------------------------- |
| `/login`      | `LoginPage.jsx`  | Main user login page with Google OAuth |
| `/SignupPage` | `SignupPage.jsx` | Admin login page                       |

### 4.2 Admin Routes

Admin pages are protected by the `ProtectedRoute` component and require the user role to be **admin**.

| Route                 | Component            |
| --------------------- | -------------------- |
| `/`                   | `Home.jsx`           |
| `/add-startup`        | `AddStartup.jsx`     |
| `/view-startups`      | `AddStartupView.jsx` |
| `/add-coaches`        | `AddCoaches.jsx`     |
| `/view-coaches`       | `AddCoachesView.jsx` |
| `/coach-availability` | `AddTime.jsx`        |
| `/start-matching`     | `Start Matching.jsx` |

### 4.3 User Routes

User pages are protected by the `UserRoute` component and are accessible only to authenticated non-admin users.

| Route             | Component         |
| ----------------- | ----------------- |
| `/user-dashboard` | `UserHome.jsx`    |
| `/user-profile`   | `UserProfile.jsx` |

### 4.4 Route Protection

Role-based access control is implemented using two custom route wrappers. 

#### 4.4.1 ProtectedRoute

Used for administrator pages.

**Features:**
Verifies user authentication
- Restricts access to administrators
- Redirects unauthenticated users to /login
- Redirects authenticated non-admin users to /user-dashboard

#### 4.4.2 UserRoute

Used for regular user pages.

**Features:**
- Verifies user authentication
- Prevents administrators from accessing user pages
- Redirects unauthenticated users to /login
- Redirects administrators back to the admin dashboard

### 4.5 Authentication Flow

Authentication state is managed inside `App.js`.

**Workflow**
1. User signs in through Google OAuth or Admin Login.
2. Authentication state is stored in localStorage.
3. User role (admin or user) is saved.
4. User information is stored for dashboard usage.
5. Protected routes become accessible.
6. Clicking Logout clears the stored session and redirects the user to /login.

### 4.6 Default Redirection

Unknown routes are automatically redirected based on the current authentication state.

| User State        | Redirect          |
| ----------------- | ----------------- |
| Not authenticated | `/login`          |
| Admin             | `/`               |
| User              | `/user-dashboard` |

---

## 5. Authentication

The frontend supports two authentication methods: **Google OAuth** for regular users and a dedicated **Admin Login** for administrators. Authentication state is managed within `App.js` and persisted using `localStorage` to maintain user sessions across browser refreshes.

### 5.1 Google OAuth Authentication

Regular users authenticate using Google OAuth through the `GoogleOAuthProvider`.

**Features:**
- Google account sign-in
- Retrieves authenticated user information
- Stores user profile for dashboard use
- Redirects users to the User Dashboard after successful login

### 5.2 Admin Authentication

Administrators authenticate through a dedicated login page.

**Features:**
- Separate administrator login
- Assigns the admin role
- Grants access to protected administrative routes
- Redirects to the Admin Dashboard after login

### 5.3 Session Management

Authentication status is stored locally to preserve the user's session. These values are restored when the application is reloaded, allowing authenticated users to remain signed in until they log out.

| Key               | Purpose                                          |
| ----------------- | ------------------------------------------------ |
| `isAuthenticated` | Stores login status                              |
| `userRole`        | Stores the current user role (`admin` or `user`) |
| `userData`        | Stores authenticated user information            |

### 5.4 Role-Based Access Control

Access permissions are enforced through custom route guards.

**Admin**
- Access to administrative dashboard
- Startup management
- Coach management
- Availability management
- Matching functionality
**User**
- Access to User Dashboard
- Profile management
- User-specific pages

Unauthorized users are automatically redirected to the appropriate page based on their authentication status and role.

### 5.5 Logout

Logging out removes all authentication data from localStorage and resets the application state.
The logout functionality was enhanced to properly clear the stored session and redirect authenticated users back to the main login page, preventing access to protected routes after logout.

**Logout Process**
1. Clear authentication status
2. Remove stored user role
3. Remove stored user information
4. Redirect to /login

---

## 6. Pages and Components

The frontend consists of reusable pages and components, where each page corresponds to a key feature of the application, and shared components deliver common functionalities like authentication and user interface interactions.

### 6.1 App.js

App.js serves as the application's entry point and central routing configuration.

**Responsibilities:**
- Initializes Google OAuth
- Configures React Router
- Defines public and protected routes
- Manages authentication state
- Implements role-based access control
- Handles login and logout workflows

### 6.2 Login Pages

Located in `src/pages/login/` which manages user authentication

**Main Components**

| Component        | Purpose                            |
| ---------------- | ---------------------------------- |
| `LoginPage.jsx`  | Main login page using Google OAuth |
| `SignupPage.jsx` | Administrator login page           |
| `AdminLogin.jsx` | Admin authentication component     |
| `googleauth.jsx` | Google OAuth integration           |

### 6.3 Admin Pages

Located in `src/pages/` which provides the main administration features.
These pages below allow administrators to manage startups, coaches, availability, and the matching process.

**Main Pages:**
- Home/
- AddStartup/
- AddStartupView/
- AddCoaches/
- AddCoachesView/
- StartMatching/

### 6.4 User Pages

Located in `src/pages/UserHome/`, which provides pages for authenticated users.
These pages below display user information and profile-related features.

**Components:**
- UserHome.jsx
- UserProfile.jsx

### 6.5 API Modules

Located in `src/api/` which centralizes communication with the backend.

**Files:**
- axiosConfig.js
- startupApi.js
- coachApi.js

### 6.6 Shared Components

Located in `app/components/` which contains reusable UI components shared across the application.

**Components:**
- LoginForm.jsx

---

## 7. API Integration

The frontend communicates with the Flask backend through REST APIs using **Axios**. API requests are centralized in the `src/api/` directory to separate backend communication from the user interface.

API communication is separated into dedicated modules, making the frontend easier to maintain and extend as additional backend endpoints become available.

### 7.1 Axios Configuration

File `src/api/axiosConfig.js` defines the shared Axios instance used throughout the application.

**Features:**
- Backend base URL configuration
- Common request settings
- Centralized API communication

### 7.2 Startup API

File  `src/api/startupApi.js` handles API requests related to startup management.

**Features:**
- Retrieve startup data
- Create new startups
- Communicate with the backend using REST endpoints

### 7.3 Coach API

File  `src/api/coachApi.js` handles API requests related to coach management.

**Features:**
- Retrieve coach data
- Register new coaches
- Communicate with the backend using REST endpoints

### 7.4 Frontend–Backend Communication

The frontend exchanges JSON data with the backend through HTTP requests.

| Method | Purpose                    |
|---------|----------------------------|
| GET | Retrieve existing data     |
| POST | Create new records         |
| PATCH | Update existing records    |
| DELETE | Remove records             |

---

## 8. Styling

The frontend uses **Tailwind CSS** as its primary styling framework, providing a responsive and utility-first approach for building the user interface. Additional libraries are used to enhance animations and user experience.

### 8.1 Tailwind CSS

Tailwind CSS is used throughout the application to build consistent and responsive layouts.

**Features:**
- Utility-first CSS framework
- Responsive page layouts
- Modern dashboard interface
- Consistent spacing, colors, and typography

### 8.2 User Interface

The application follows a clean and modern design across both administrator and user pages.

**Features:**
- Gradient backgrounds
- Responsive cards and tables
- Form validation feedback
- Interactive buttons and navigation

### 8.3 Animations

Animations are implemented using **Framer Motion** to improve user interaction.

**Features:**
- Page transitions
- Button hover effects
- Smooth component animations

---

## 9. Environment Variables

The frontend supports a small set of environment variables for configuration.
These variables allow the application to communicate with the backend without modifying the source code.

### 9.1 **`REACT_APP_BACKEND_URL`**

- Defines the base URL used for all backend API requests.
- Used by the shared Axios configuration (`src/api/axiosConfig.js`).
- **Default** (development):
  ```text
  http://127.0.0.1:5000
  ```
- Can be changed when deploying the frontend to another backend server.

### 9.2 **Optional Development Variables**

These variables may be useful during local development but are not required by the application.

- `HOST`
- `PORT`
- `BROWSER`

---

## 10. Future Improvements

The frontend has been significantly expanded to support authentication, role-based access control, startup and coach management, and user dashboards. 
The following areas remain opportunities for future development.

### 10.1 Complete User Features

Continue expanding the user experience after authentication.

**Possible Improvements:**

- Add user meeting history
- Display assigned coach information
- Show upcoming coaching sessions
- Extend user profile management

### 10.2 Coach Management

Further improve coach administration pages.

**Possible Improvements:**

- Coach search and filtering
- Edit coach information
- Delete coach records
- Enhanced availability management

### 10.3 Startup Management

Improve startup administration beyond the current functionality.

**Possible Improvements:

- Edit startup information
- Delete startup records
- Search and filtering
- Improved validation and error handling

### 10.4 Matching Workflow

Continue improving the integration between the frontend and the backend matching engine.

**Possible Improvements:**

- Display matching progress
- Present matching results in a dedicated interface
- Improve user feedback during long-running operations

### 10.5 User Interface and User Experience

Continue refining the overall user interface.

**Possible Improvements:**

- Improve responsive design
- Add loading indicators
- Improve accessibility
- Maintain a consistent design system across all pages
---

This document reflects the frontend architecture and implementation as of **24 June 2026**. Future contributors should update this documentation whenever new pages, routing logic, authentication flows, or API integrations are introduced.