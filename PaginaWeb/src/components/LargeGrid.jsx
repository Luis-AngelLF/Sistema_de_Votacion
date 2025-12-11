import LargeCard from "./LargeCard";

export default function LargeGrid({ onCardClick }) {
  return (
    <>
      <div
        id="tipos"
        className="flex flex-wrap gap-8 justify-center mt-28 px-6"
      >
        <LargeCard
          title="Votaciones"
          description="Accede al módulo principal."
          onCardClick={onCardClick}
        />

        <LargeCard
          title="Gestión"
          description="Control de usuarios y módulos administrativos."
          onCardClick={onCardClick}
        />

        <LargeCard
          title="Reportes"
          description="Visualiza información detallada."
          onCardClick={onCardClick}
        />

        <LargeCard
          title="Reportes"
          description="Visualiza información detallada."
          onCardClick={onCardClick}
        />
      </div>
    </>
  );
}
