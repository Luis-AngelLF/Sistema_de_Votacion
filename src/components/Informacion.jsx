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
            ¿Cómo Votar?
            <span className="material-symbols-rounded text-indigo-400 text-4xl">
              how_to_vote
            </span>
          </h2>
          <p className="text-gray-400 mt-2">
            Aprende sobre nuestro sistema de votación seguro, anónimo y basado en criptografía avanzada.
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
              <span className="material-symbols-rounded text-indigo-400">security</span>
              <h3 className="text-lg font-semibold text-white">Votación Segura</h3>
            </div>
            <p className="text-gray-400 text-sm leading-relaxed">
              Tu voto está protegido con encriptación homomórfica Paillier, que permite
              cálculos sobre datos cifrados sin revelar su contenido.
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
              <span className="material-symbols-rounded text-indigo-400">privacy_tip</span>
              <h3 className="text-lg font-semibold text-white">Anonimato Total</h3>
            </div>
            <p className="text-gray-400 text-sm leading-relaxed">
              El sistema garantiza el anonimato completo. Nadie puede relacionar tu voto
              con tu identidad, ni siquiera los administradores del sistema.
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
              <span className="material-symbols-rounded text-indigo-400">blockchain</span>
              <h3 className="text-lg font-semibold text-white">Blockchain</h3>
            </div>
            <p className="text-gray-400 text-sm leading-relaxed">
              Cada voto genera un hash único almacenado en blockchain, permitiendo
              verificar la integridad sin comprometer el anonimato.
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
              <span className="material-symbols-rounded text-indigo-400">verified</span>
              <h3 className="text-lg font-semibold text-white">Verificación</h3>
            </div>
            <p className="text-gray-400 text-sm leading-relaxed">
              Puedes verificar que tu voto fue contado correctamente sin revelar
              por quién votaste, gracias a las propiedades matemáticas de la encriptación.
            </p>
          </div>

        </div>

        {/* Guía de votación */}
        <div className="mt-8 p-6 rounded-xl bg-[#131b2f] border border-white/5">
          <h3 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
            <span className="material-symbols-rounded text-indigo-400">checklist</span>
            Pasos para Votar
          </h3>
          <div className="space-y-3 text-gray-400 text-sm">
            <div className="flex items-start gap-3">
              <span className="text-indigo-400 font-bold">1.</span>
              <p>Inicia sesión con tu cédula y contraseña.</p>
            </div>
            <div className="flex items-start gap-3">
              <span className="text-indigo-400 font-bold">2.</span>
              <p>Selecciona la elección activa en la que deseas participar.</p>
            </div>
            <div className="flex items-start gap-3">
              <span className="text-indigo-400 font-bold">3.</span>
              <p>Revisa la información de los candidatos y selecciona tu preferencia.</p>
            </div>
            <div className="flex items-start gap-3">
              <span className="text-indigo-400 font-bold">4.</span>
              <p>Confirma tu voto. El sistema lo encriptará automáticamente.</p>
            </div>
            <div className="flex items-start gap-3">
              <span className="text-indigo-400 font-bold">5.</span>
              <p>Recibirás confirmación con tu hash único de blockchain.</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
