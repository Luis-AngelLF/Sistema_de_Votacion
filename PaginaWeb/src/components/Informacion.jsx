export default function Informacion() {
  return (
    <section
      id="info"
      className="w-full mt-28 px-6 flex justify-center"
    >
      <div
        className="
          max-w-4xl
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
            Información sobre 
            <span className="material-symbols-rounded text-indigo-400 text-4xl">
              Votaciones 2026
            </span>
          </h2>
          <p className="text-gray-400 mt-2">
            Todo lo que necesitas saber sobre el proceso de votación, seguridad de tu voto
            y cómo participar en las elecciones.
          </p>
        </div>

        {/* Contenido en tarjetas */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          
          {/* Tarjeta 1 */}
          <div
            className="
              p-6
              rounded-xl
              bg-[#131b2f]
              border border-white/5
              hover:border-indigo-400/40
              hover:shadow-lg
              hover:shadow-indigo-500/10
              transition-all
            "
          >
            <div className="flex items-center gap-3 mb-3">
              <span className="material-symbols-rounded text-indigo-400"> •</span>
              <h3 className="text-lg font-semibold text-white">Cómo Votar</h3>
            </div>
            <p className="text-gray-400 text-sm leading-relaxed">
              Selecciona tu candidato de preferencia en la papeleta digital.
              Tu voto se encripta automáticamente para garantizar la privacidad
              y seguridad de tu elección.
            </p>
          </div>

          {/* Tarjeta 2 */}
          <div
            className="
              p-6
              rounded-xl
              bg-[#131b2f]
              border border-white/5
              hover:border-indigo-400/40
              hover:shadow-lg
              hover:shadow-indigo-500/10
              transition-all
            "
          >
            <div className="flex items-center gap-3 mb-3">
              <span className="material-symbols-rounded text-indigo-400">•</span>
              <h3 className="text-lg font-semibold text-white">Privacidad del Voto</h3>
            </div>
            <p className="text-gray-400 text-sm leading-relaxed">
              Tu voto está completamente protegido. Utilizamos encriptación Paillier
              para garantizar que nadie pueda conocer tu elección, ni siquiera
              el administrador del sistema.
            </p>
          </div>

          {/* Tarjeta 3 */}
          <div
            className="
              p-6
              rounded-xl
              bg-[#131b2f]
              border border-white/5
              hover:border-indigo-400/40
              hover:shadow-lg
              hover:shadow-indigo-500/10
              transition-all
            "
          >
            <div className="flex items-center gap-3 mb-3">
              <span className="material-symbols-rounded text-indigo-400"> •</span>
              <h3 className="text-lg font-semibold text-white">Validación del Voto</h3>
            </div>
            <p className="text-gray-400 text-sm leading-relaxed">
              Cada voto se registra en la blockchain para garantizar su integridad.
              Puedes verificar que tu voto fue contabilizado correctamente sin
              revelar tu elección.
            </p>
          </div>

          {/* Tarjeta 4 */}
          <div
            className="
              p-6
              rounded-xl
              bg-[#131b2f]
              border border-white/5
              hover:border-indigo-400/40
              hover:shadow-lg
              hover:shadow-indigo-500/10
              transition-all
            "
          >
            <div className="flex items-center gap-3 mb-3">
              <span className="material-symbols-rounded text-indigo-400"> •</span>
              <h3 className="text-lg font-semibold text-white">Auditoría Transparente</h3>
            </div>
            <p className="text-gray-400 text-sm leading-relaxed">
              Todos los votos se registran en la blockchain pública. Los resultados
              son auditables y verificables por cualquiera, garantizando total
              transparencia en el proceso electoral.
            </p>
          </div>

        </div>
      </div>
    </section>
  );
}
