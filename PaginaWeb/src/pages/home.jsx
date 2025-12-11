import { useState } from "react";
import Header from "../components/header";
import LargeGrid from "../components/LargeGrid";
import Informacion from "../components/Informacion";
import ModalVotaciones from "../components/ModalVotaciones";

export default function Home() {
  const [openModal, setOpenModal] = useState(false);

  return (
    <div className="min-h-screen">
      <Header />

      <main className="pt-20 px-6">
        <LargeGrid onCardClick={() => setOpenModal(true)} />
        <Informacion />
      </main>

      <ModalVotaciones
        show={openModal}
        onClose={() => setOpenModal(false)}
      />
    </div>
  );
}
