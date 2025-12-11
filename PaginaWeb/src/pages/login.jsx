import { useState } from "react";

//!CUANDO ESTE LISTO EL SUPABASE DESCOMENTAR ESTA LINEA
// import supabase from "../lib/supabase";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");


    //!CUANDO ESTE LISTO EL SUPABASE USAR ESTE CODIGO PARA EL LOGINs

  /** 
  async function handleLogin(e) {
    e.preventDefault();
    const { data, error } = await supabase.auth.signInWithPassword({ email, password });
    if (error) {
      setError("Correo o contraseña incorrectos");
      return;
    }
    window.location.href = "/home";
  }*/

    async function handleLogin(e) {
        e.preventDefault();

        // Simulación de login local
        if (email === "test@correo.com" && password === "123456") {
        // redirigir a Home
        window.location.href = "/home";
        } else {
        setError("Correo o contraseña incorrectos");
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

