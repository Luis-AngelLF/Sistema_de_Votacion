import { useState, useEffect } from "react";

export default function Resultados() {
  const [elecciones, setElecciones] = useState([]);
  const [resultados, setResultados] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const API_BASE = "http://localhost:5000";

  // Obtener elecciones
  useEffect(() => {
    const obtenerElecciones = async () => {
      try {
        const response = await fetch(`${API_BASE}/api/elecciones`);
        if (response.ok) {
          const data = await response.json();
          setElecciones(data.elecciones || []);
        }
      } catch (err) {
        setError("Error al obtener elecciones");
      }
    };

    obtenerElecciones();
  }, []);

  // Calcular resultados en tiempo real desde el backend
  useEffect(() => {
    const calcularResultados = async () => {
      if (elecciones.length === 0) return;

      setLoading(true);
      const nuevosResultados = {};

      for (const eleccion of elecciones) {
        try {
          // Obtener resultados calculados desde el backend
          const response = await fetch(`${API_BASE}/api/resultados-tiempo-real/${eleccion.id_eleccion}`);
          if (response.ok) {
            const data = await response.json();
            nuevosResultados[eleccion.id_eleccion] = {
              nombre: eleccion.nombre_eleccion,
              candidatos: data.candidatos || [],
              resultados: data.resultados || {},
              totalVotos: data.total_votos || 0
            };
          }
        } catch (err) {
          console.error("Error calculando resultados para elección:", eleccion.id_eleccion, err);
        }
      }

      setResultados(nuevosResultados);
      setLoading(false);
    };

    calcularResultados();

    // Actualizar cada 30 segundos
    const interval = setInterval(calcularResultados, 30000);
    return () => clearInterval(interval);
  }, [elecciones]);

  return (
    <section
      id="results"
      className="w-full mt-28 px-6 flex justify-center"
    >
      <div
        className="
          max-w-6xl
          w-full
          p-10
          rounded-2xl
          bg-[#1E1B2E]
          backdrop-blur-2xl
          border border-white/10
          shadow-xl
          text-gray-300
        "
      >
        {/* Encabezado */}
        <div className="mb-8">
          <h2 className="text-4xl font-bold text-white flex items-center gap-3">
            Resultados en Tiempo Real
            <span className="material-symbols-rounded text-indigo-400 text-4xl">
              analytics
            </span>
          </h2>
          <p className="text-gray-400 mt-2">
            Visualiza los resultados actualizados automáticamente usando encriptación homomórfica.
            Los datos se mantienen seguros y anónimos.
          </p>
        </div>

        {loading ? (
          <div className="flex justify-center items-center py-12">
            <div className="animate-spin">
              <div className="h-12 w-12 border-4 border-indigo-500/30 border-t-indigo-500 rounded-full"></div>
            </div>
            <p className="ml-4 text-gray-400">Calculando resultados...</p>
          </div>
        ) : error ? (
          <div className="text-center py-12 text-red-400">
            <p>{error}</p>
          </div>
        ) : (
          <div className="space-y-8">
            {Object.entries(resultados).map(([idEleccion, eleccionData]) => (
              <div key={idEleccion} className="bg-[#131b2f] rounded-xl p-6 border border-white/5">
                <h3 className="text-2xl font-semibold text-white mb-4">
                  {eleccionData.nombre}
                </h3>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
                  {eleccionData.candidatos.map((candidato) => {
                    const votos = eleccionData.resultados[candidato.id_candidato] || 0;
                    const porcentaje = eleccionData.totalVotos > 0 ? (votos / eleccionData.totalVotos * 100).toFixed(1) : 0;

                    return (
                      <div
                        key={candidato.id_candidato}
                        className="bg-[#1a1f35] rounded-lg p-4 border border-white/10"
                      >
                        <div className="flex items-center gap-3 mb-3">
                          <div className="w-12 h-12 bg-gradient-to-br from-indigo-500/20 to-purple-500/20 rounded-lg flex items-center justify-center">
                            {candidato.foto_url ? (
                              <img
                                src={candidato.foto_url}
                                alt={candidato.nombre_completo}
                                className="w-full h-full object-cover rounded-lg"
                              />
                            ) : (
                              <span className="text-xs text-gray-400">Sin foto</span>
                            )}
                          </div>
                          <div>
                            <h4 className="font-semibold text-white text-sm truncate">
                              {candidato.nombre_completo}
                            </h4>
                            <p className="text-xs text-gray-400">ID: {candidato.id_candidato}</p>
                          </div>
                        </div>

                        <div className="space-y-2">
                          <div className="flex justify-between text-sm">
                            <span className="text-gray-400">Votos:</span>
                            <span className="text-white font-semibold">{votos}</span>
                          </div>
                          <div className="flex justify-between text-sm">
                            <span className="text-gray-400">Porcentaje:</span>
                            <span className="text-indigo-400 font-semibold">{porcentaje}%</span>
                          </div>
                          <div className="w-full bg-gray-700 rounded-full h-2">
                            <div
                              className="bg-indigo-500 h-2 rounded-full transition-all duration-500"
                              style={{ width: `${porcentaje}%` }}
                            ></div>
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>

                <div className="bg-indigo-600/20 border border-indigo-500/30 rounded-lg p-4">
                  <div className="flex justify-between items-center">
                    <span className="text-indigo-300 font-semibold">Total de Votos:</span>
                    <span className="text-white text-xl font-bold">{eleccionData.totalVotos}</span>
                  </div>
                </div>
              </div>
            ))}

            {Object.keys(resultados).length === 0 && (
              <div className="text-center py-12 text-gray-400">
                <p>No hay elecciones con resultados disponibles</p>
              </div>
            )}
          </div>
        )}

        <div className="mt-8 p-4 bg-yellow-500/10 border border-yellow-500/20 rounded-lg">
          <div className="flex items-start gap-3">
            <span className="material-symbols-rounded text-yellow-400 mt-0.5">info</span>
            <div>
              <h4 className="text-yellow-400 font-semibold mb-1">Información Técnica</h4>
              <p className="text-yellow-300 text-sm">
                Los resultados se calculan usando suma homomórfica Paillier, permitiendo contar votos
                cifrados sin necesidad de desencriptarlos individualmente. Los datos se actualizan automáticamente cada 30 segundos.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}