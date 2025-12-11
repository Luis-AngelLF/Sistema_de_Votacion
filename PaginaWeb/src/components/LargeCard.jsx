export default function LargeCard({ title, description, onCardClick, href }) {
  return (
    <div
      onClick={onCardClick}
      className="
        h-122
        w-56
        md:w-64
        rounded-2xl
        p-6
        bg-[#1E1B2E]/80
        border border-white/10
        backdrop-blur-xl
        shadow-2xl
        cursor-pointer
        flex flex-col
        justify-between
        transition-all
        hover:-translate-y-1
        hover:shadow-2xl
        hover:shadow-indigo-500/20
      "
    >
      {/* Si hay href, se envuelve solo el contenido */}
      {href ? (
        <a href={href} className="block">
          <h2 className="text-lg font-semibold text-white mb-2">{title}</h2>
          <p className="text-gray-300 text-sm">{description}</p>
        </a>
      ) : (
        <>
          <h2 className="text-lg font-semibold text-white mb-2">{title}</h2>
          <p className="text-gray-300 text-sm">{description}</p>
        </>
      )}
    </div>
  );
}
