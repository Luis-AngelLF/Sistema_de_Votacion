import { useState, useEffect } from "react";
import LargeCard from "./LargeCard";

export default function LargeGrid({ onCardClick }) {
  const [elecciones, setElecciones] = useState([]);
  const [loading, setLoading] = useState(false);

  const API_BASE = "http://localhost:5000/";

  // Obtener elecciones del API
  useEffect(() => {
    const obtenerElecciones = async () => {
      setLoading(true);
      try {
        const response = await fetch(`${API_BASE}/api/elecciones`);
        if (response.ok) {
          const data = await response.json();
          setElecciones(data.elecciones || []);
        }
      } catch (error) {
        console.error("Error al obtener elecciones:", error);
      } finally {
        setLoading(false);
      }
    };

    obtenerElecciones();
  }, []);

  return (
    <>
      <div
        id="tipos"
        className="flex flex-wrap gap-8 justify-center mt-28 px-6"
      >
        {loading ? (
          <div className="text-center">
            <p className="text-gray-400">Cargando elecciones...</p>
          </div>
        ) : elecciones.length === 0 ? (
          <div className="text-center">
            <p className="text-gray-400">No hay elecciones disponibles</p>
          </div>
        ) : (
          elecciones.map((eleccion) => (
            <LargeCard
              key={eleccion.id_eleccion}
              title={eleccion.nombre_eleccion}
              description={eleccion.descripcion}
              estado={eleccion.estado}
              onCardClick={() => onCardClick(eleccion.id_eleccion)}
            />
          ))
        )}
      </div>
    </>
  );
}