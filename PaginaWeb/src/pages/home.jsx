import { useState, useEffect } from "react";
import Header from "../components/Header";
import LargeGrid from "../components/LargeGrid";
import Informacion from "../components/Informacion";
import ModalVotaciones from "../components/ModalVotaciones";

export default function Home() {
  const [openModal, setOpenModal] = useState(false);
  const [selectedEleccion, setSelectedEleccion] = useState(null);
  const [cedula, setCedula] = useState(null);

  // Obtener la cédula del usuario del localStorage o contexto
  useEffect(() => {
    const userData = localStorage.getItem("usuario");
    if (userData) {
      try {
        const user = JSON.parse(userData);
        setCedula(user.cedula);
      } catch (error) {
        console.error("Error al parsear datos del usuario:", error);
        // Redirigir al login si hay error en los datos
        window.location.href = "/login";
      }
    } else {
      // Redirigir al login si no hay datos de usuario
      window.location.href = "/login";
    }
  }, []);

  const handleCardClick = (id_eleccion) => {
    setSelectedEleccion(id_eleccion);
    setOpenModal(true);
  };

  return (
    <div className="min-h-screen">
      <Header />

      <main className="pt-20 px-6">
        <LargeGrid onCardClick={handleCardClick} />
        <Informacion />
      </main>

      <ModalVotaciones
        show={openModal}
        onClose={() => setOpenModal(false)}
        id_eleccion={selectedEleccion}
        cedula={cedula}
      />
    </div>
  );
}