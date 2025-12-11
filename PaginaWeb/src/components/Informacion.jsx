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
            Necesitas 
            <span className="material-symbols-rounded text-indigo-400 text-4xl">
              Saberlo!!
            </span>
          </h2>
          <p className="text-gray-400 mt-2">
            Consulta el estado del sistema, procesos activos y guías rápidas
            para navegar dentro del panel administrativo.
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
              <span className="material-symbols-rounded text-indigo-400">settings</span>
              <h3 className="text-lg font-semibold text-white">Configuración</h3>
            </div>
            <p className="text-gray-400 text-sm leading-relaxed">
              Revisa el estado general del sistema, parámetros configurados y
              ajustes activos.
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
              <span className="material-symbols-rounded text-indigo-400">sync</span>
              <h3 className="text-lg font-semibold text-white">Procesos Activos</h3>
            </div>
            <p className="text-gray-400 text-sm leading-relaxed">
              Visualiza información en tiempo real sobre módulos activos y
              actividad reciente.
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
              <span className="material-symbols-rounded text-indigo-400">dashboard</span>
              <h3 className="text-lg font-semibold text-white">Estado Visual</h3>
            </div>
            <p className="text-gray-400 text-sm leading-relaxed">
              Accede a resúmenes claros, indicadores visuales y métricas clave
              del sistema.
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
              <span className="material-symbols-rounded text-indigo-400">menu_book</span>
              <h3 className="text-lg font-semibold text-white">Guías Rápidas</h3>
            </div>
            <p className="text-gray-400 text-sm leading-relaxed">
              Accede a instrucciones breves que te ayudarán a comprender cada
              módulo sin complicaciones.
            </p>
          </div>

        </div>
      </div>
    </section>
  );
}
