import { useState, useEffect } from "react";

export default function ModalVotaciones({ show, onClose, id_eleccion, cedula }) {
  const [selected, setSelected] = useState(null);
  const [candidatos, setCandidatos] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [votando, setVotando] = useState(false);
  const [mensajeExito, setMensajeExito] = useState(null);

  const API_BASE = "http://localhost:5000";

  // Obtener candidatos del API
  useEffect(() => {
    console.log("ModalVotaciones - show:", show, "id_eleccion:", id_eleccion);
    
    if (!show || !id_eleccion) {
      console.log("Modal no mostrado o sin id_eleccion");
      return;
    }

    const obtenerCandidatos = async () => {
      setLoading(true);
      setError(null);
      console.log(`Obteniendo candidatos para elección ${id_eleccion}`);
      try {
        const response = await fetch(`${API_BASE}/api/candidatos/${id_eleccion}`);
        console.log("Respuesta del API:", response.status);
        
        if (!response.ok) {
          throw new Error("No se pudieron obtener los candidatos");
        }
        const data = await response.json();
        console.log("Candidatos obtenidos:", data.candidatos);
        setCandidatos(data.candidatos || []);
      } catch (err) {
        console.error("Error al obtener candidatos:", err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    obtenerCandidatos();
  }, [show, id_eleccion]);

  // Registrar el voto
  const handleConfirmarVoto = async () => {
    console.log("Intentando votar - selected:", selected, "cedula:", cedula);
    
    if (!selected) {
      setError("Debe seleccionar un candidato");
      return;
    }
    
    if (!cedula) {
      setError("Debe iniciar sesión para votar");
      return;
    }

    setVotando(true);
    setError(null);
    try {
      const response = await fetch(`${API_BASE}/api/votar`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          cedula: cedula,
          id_eleccion: id_eleccion,
          id_candidato: selected,
        }),
      });

      const data = await response.json();
      console.log("Respuesta del API de votación:", data);

      if (!response.ok) {
        throw new Error(data.error || "Error al registrar el voto");
      }

      setMensajeExito("¡Voto registrado exitosamente!");
      setSelected(null);
      
      // Cerrar modal después de 2 segundos
      setTimeout(() => {
        setMensajeExito(null);
        onClose();
      }, 2000);
    } catch (err) {
      setError(err.message);
      console.error("Error al registrar voto:", err);
    } finally {
      setVotando(false);
    }
  };

  if (!show) return null;

  return (
    <form onSubmit={(e) => { e.preventDefault(); handleConfirmarVoto(); }}>
    <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm flex items-center justify-center px-4">
      <div className="bg-[#1f2937]/90 text-white rounded-3xl shadow-2xl w-full max-w-5xl p-8 border border-white/20 animate-fadeIn overflow-y-auto max-h-[90vh]">

        {/* HEADER */}
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-semibold text-indigo-400">Papeleta de Votación</h2>
          <button 
            type="button" 
            className="text-gray-300 hover:text-white text-xl" 
            onClick={onClose}
            disabled={votando}
          >
            ✕
          </button>
        </div>

        {/* SUBTEXTO */}
        <p className="text-gray-400 text-sm mb-6">
          Seleccione un candidato para registrar su voto. Haga clic sobre la tarjeta del candidato de su preferencia.
        </p>

        {/* AVISO DE LOGIN */}
        {!cedula && (
          <div className="bg-yellow-500/20 border border-yellow-500 text-yellow-300 px-4 py-3 rounded-lg mb-6">
            ⚠️ Debe iniciar sesión para poder votar. Si ya inició sesión, recargue la página.
          </div>
        )}

        {/* MENSAJES DE ERROR Y ÉXITO */}
        {error && (
          <div className="bg-red-500/20 border border-red-500 text-red-300 px-4 py-3 rounded-lg mb-6">
            {error}
          </div>
        )}

        {mensajeExito && (
          <div className="bg-green-500/20 border border-green-500 text-green-300 px-4 py-3 rounded-lg mb-6">
            {mensajeExito}
          </div>
        )}

        {/* CONTENIDO PRINCIPAL */}
        {loading ? (
          <div className="flex justify-center items-center py-12">
            <div className="animate-spin">
              <div className="h-12 w-12 border-4 border-indigo-500/30 border-t-indigo-500 rounded-full"></div>
            </div>
          </div>
        ) : candidatos.length === 0 ? (
          <div className="text-center py-12 text-gray-400">
            <p>No hay candidatos disponibles en esta elección</p>
          </div>
        ) : (
          <>
            {/* GRID de candidatos */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
              {candidatos.map((candidato) => (
                <div
                  key={candidato.id_candidato}
                  onClick={() => !votando && setSelected(candidato.id_candidato)}
                  className={`
                    p-4 rounded-2xl cursor-pointer overflow-hidden border-2 transition-all
                    ${selected === candidato.id_candidato 
                      ? "border-indigo-500 bg-indigo-600/30 scale-105 shadow-lg" 
                      : "border-white/20 bg-[#111827]/80 hover:bg-[#1c2430] hover:border-white/40"
                    }
                    ${votando ? "opacity-50 cursor-not-allowed" : ""}
                  `}
                >
                  {/* Placeholder para foto */}
                  <div className="w-full h-40 bg-gradient-to-br from-indigo-500/20 to-purple-500/20 rounded-lg flex items-center justify-center mb-3 border border-white/10">
                    <span className="text-gray-400 text-sm">Sin foto</span>
                  </div>
                  
                  {/* Información del candidato */}
                  <h3 className="font-semibold text-white text-lg truncate">
                    {candidato.nombre_completo}
                  </h3>
                  <p className="text-gray-400 text-sm line-clamp-2 mb-2">
                    {candidato.propuesta || "Sin propuesta"}
                  </p>
                  <p className="text-xs text-gray-500">
                    ID: {candidato.id_candidato}
                  </p>
                  
                  {/* Indicador de selección */}
                  {selected === candidato.id_candidato && (
                    <div className="mt-2 flex items-center text-indigo-400">
                      <span className="text-sm font-medium">✓ Seleccionado</span>
                    </div>
                  )}
                </div>
              ))}
            </div>

            {/* RESUMEN DE SELECCIÓN */}
            {selected && (
              <div className="bg-indigo-600/20 border border-indigo-500 text-indigo-300 px-4 py-3 rounded-lg mb-6">
                <h4 className="font-semibold mb-2">Candidato seleccionado:</h4>
                <p className="text-sm">
                  {candidatos.find(c => c.id_candidato === selected)?.nombre_completo}
                </p>
              </div>
            )}

            {/* BOTÓN CONFIRMAR */}
            <button
              type="submit"
              disabled={!selected || votando}
              className={`
                w-full py-3 rounded-2xl text-white font-semibold transition text-lg
                ${selected && !votando
                  ? "bg-indigo-600 hover:bg-indigo-700" 
                  : "bg-gray-500 cursor-not-allowed"
                }
              `}
            >
              {votando ? "Registrando voto..." : "Confirmar selección"}
            </button>
          </>
        )}

      </div>
    </div>
    </form>
  );
}