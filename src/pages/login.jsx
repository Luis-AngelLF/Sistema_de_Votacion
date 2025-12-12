import { useState } from "react";

//!CUANDO ESTE LISTO EL SUPABASE DESCOMENTAR ESTA LINEA
import supabase from "../lib/supabase";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");


  async function handleLogin(e) {
    e.preventDefault();
    setError("");

    try {
      const response = await fetch("http://localhost:5000/api/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          correo: email,
          password: password,
        }),
      });

      const data = await response.json();

      if (response.ok && data.success) {
        // Guardar datos del usuario en localStorage si quieres
        localStorage.setItem("usuario", JSON.stringify(data.usuario));
        // Redirigir a Home
        window.location.href = "/home";
      } else {
        setError(data.error || "Credenciales inválidas");
      }
    } catch (error) {
      setError("Error al conectar con el servidor");
      console.error("Error de login:", error);
    }
  }

    return (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-500 via-indigo-500 to-purple-600 p-4">
        
        <div className="backdrop-blur-lg bg-white/10 border border-white/20 shadow-xl rounded-2xl p-10 w-full max-w-md">
            
            <h1 className="text-4xl font-bold text-center text-white mb-6">
            Bienvenido
            </h1>

            <p className="text-center text-white/80 mb-8">
            Inicia sesión para continuar
            </p>

            <form onSubmit={handleLogin} className="space-y-4">
            
            <div>
                <label className="text-white text-sm">Correo</label>
                <input
                type="email"
                onChange={(e) => setEmail(e.target.value)}
                className="w-full mt-1 px-4 py-2 bg-white/20 text-white placeholder-white/60 rounded-lg focus:outline-none focus:ring-2 focus:ring-white/40"
                placeholder="correo@example.com"
                />
            </div>

            <div>
                <label className="text-white text-sm">Contraseña</label>
                <input
                type="password"
                onChange={(e) => setPassword(e.target.value)}
                className="w-full mt-1 px-4 py-2 bg-white/20 text-white placeholder-white/60 rounded-lg focus:outline-none focus:ring-2 focus:ring-white/40"
                placeholder="••••••••"
                />
            </div>

            {error && (
                <p className="text-red-300 text-sm text-center -mt-2">{error}</p>
            )}

            <button
                type="submit"
                className="w-full bg-white text-indigo-600 py-2 mt-4 font-semibold rounded-lg hover:bg-gray-100 transition"
            >
                Entrar
            </button>
            </form>
        </div>
        </div>
    );
}