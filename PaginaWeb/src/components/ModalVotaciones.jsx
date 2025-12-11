import { useState } from "react";

export default function ModalVotaciones({ show, onClose }) {
  const [selected, setSelected] = useState(null);

  if (!show) return null;

  const opciones = Array.from({ length: 10 }, (_, i) => ({
    id: i + 1,
    img: null, // aquí se reemplazará por la foto/logo del candidato
  }));

  return (
    <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm flex items-center justify-center px-4">
      <div className="bg-[#1f2937]/90 text-white rounded-3xl shadow-2xl w-full max-w-5xl p-8 border border-white/20 animate-fadeIn overflow-y-auto max-h-[90vh]">

        {/* HEADER */}
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-semibold text-indigo-400">Papeleta de Votación</h2>
          <button className="text-gray-300 hover:text-white text-xl" onClick={onClose}>
            ✕
          </button>
        </div>

        {/* SUBTEXTO */}
        <p className="text-gray-400 text-sm mb-6">
          Seleccione un recuadro para registrar su voto. Cada cuadrado representará un candidato con su foto o logo.
        </p>

        {/* GRID de 4 columnas con más espacio vertical */}
        <div className="grid grid-cols-4 gap-x-6 gap-y-6 justify-items-center mb-6">
          {opciones.map((opc) => (
            <div
              key={opc.id}
              onClick={() => setSelected(opc.id)}
              className={`
                h-40 w-40 rounded-2xl flex items-center justify-center cursor-pointer overflow-hidden border transition-all
                ${selected === opc.id 
                  ? "border-indigo-500 bg-indigo-600/30 scale-105 shadow-lg" 
                  : "border-white/20 bg-[#111827]/80 hover:bg-[#1c2430]"
                }
              `}
            >
              {opc.img ? (
                <img 
                  src={opc.img} 
                  alt={`Candidato ${opc.id}`} 
                  className="h-full w-full object-cover rounded-xl"
                />
              ) : (
                <span className="text-gray-300 text-3xl font-bold">{opc.id}</span>
              )}
            </div>
          ))}
        </div>

        {/* BOTÓN CONFIRMAR */}
        <button
          disabled={!selected}
          className={`
            w-full py-3 rounded-2xl text-white font-semibold transition text-lg
            ${selected 
              ? "bg-indigo-600 hover:bg-indigo-700" 
              : "bg-gray-500 cursor-not-allowed"
            }
          `}
        >
          Confirmar selección
        </button>

      </div>
    </div>
  );
}
