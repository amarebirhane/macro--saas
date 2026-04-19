# Micro-SaaS Platform - Frontend

The frontend interface for the modern Micro-SaaS Platform. Built for speed, responsiveness, and scale using Vue 3 and Vite, it delivers a deeply polished, premium user experience straight out of the box.

## Key Features

- **Modern Vue 3 Architecture**: Utilizing the Composition API and `<script setup>` for clean, maintainable logic.
- **Lightning Fast Tooling**: Powered by Vite for instantaneous Hot Module Replacement (HMR) and optimized production builds.
- **State Management**: Centralized, modular state management using Pinia to handle authentication, user profiles, and UI state securely.
- **Client-Side Routing**: Vue Router integration with navigation guards for secure, role-based route protection.
- **Dynamic User Experience**: Built-in support for silent authentication refreshes, intelligent error handling, loading states, and dynamic SEO updates.
- **Beautiful Iconography**: Integrated `lucide-vue-next` for consistent and beautiful vector icons throughout the interface.
- **API Integration**: Pre-configured Axios instance with automatic token interceptors for seamless communication with the FastAPI backend.

## Technology Stack

- **Framework**: Vue 3
- **Build Tool**: Vite
- **State Management**: Pinia
- **Routing**: Vue Router
- **HTTP Client**: Axios
- **Icons**: Lucide Icons

## Getting Started

### Prerequisites

- Node.js (v18+ recommended)
- npm or yarn

### Installation

1. **Clone the repository and navigate to frontend**
   ```bash
   git clone <repository-url>
   cd Micro-SaaS/frontend
   ```

2. **Install Dependencies**
   ```bash
   npm install
   ```

3. **Environment Setup**
   Create a `.env` file in the frontend root and specify the backend API URL:
   ```env
   VITE_API_URL=http://localhost:8000/api/v1
   ```

4. **Start the Development Server**
   ```bash
   npm run dev
   ```
   The application will become accessible at `http://localhost:5173` (or the port specified by Vite).

### Building for Production

To create an optimized production build:
```bash
npm run build
```
This will compile and minify the Vue application into the `dist/` directory, ready to be served by any static file hosting service or integrated into the backend's static file delivery if needed.

To preview the production build locally:
```bash
npm run preview
```

## Project Structure Highlights

- `src/components/`: Reusable, modular UI components.
- `src/views/`: Main page components mapping directly to application routes.
- `src/stores/`: Pinia stores handling global state (e.g., AuthStore, UserStore).
- `src/router/`: App routing configuration and authentication boundaries.
- `src/services/` (or `src/api/`): Axios instances and API request abstractions.

## License

This project is licensed under the MIT License - see the LICENSE file for details.