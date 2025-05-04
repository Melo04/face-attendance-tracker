import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route } from "react-router";
import './index.css'
import App from './App.jsx'
import AddUser from './AddUser.jsx';
import { Provider } from "./components/ui/provider"

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Provider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<App />} />
          <Route path="/add_user" element={<AddUser />} />
        </Routes>
      </BrowserRouter>
    </Provider>
  </StrictMode>,
)
