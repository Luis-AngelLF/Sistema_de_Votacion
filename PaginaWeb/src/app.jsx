import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./pages/login";
import Home from "./pages/home";
// import { AuthProvider } from "./context/AuthContext";

export default function App() {
  return (
    //!<AuthProvider> DESCOMENTAR CUANDO ESTE LISTO EL SUPABASE, DEJAR LA PARTE DE AUTHPROVIDER
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/home" element={<Home />} />
        </Routes>
      </BrowserRouter>
    //!</AuthProvider> DESCOMENTAR CUANDO ESTE LISTO EL SUPABASE, DEJAR LA PARTE DE AUTHPROVIDER
  );
}
