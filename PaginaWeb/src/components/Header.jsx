/**
 * Node Modules
*/
import { useState } from "react";

/**
 * Components
*/
import Navbar from "./navbar";

const Header = () => {
  const [navOpen, setNavOpen] = useState(false);

  return (
    <header className="fixed top-0 left-0 w-full h-20 flex items-center z-40">
      <div className="max-w-screen-2xl w-full mx-auto px-4 flex justify-center items-center md:px-6 md:grid-cols-[1fr,3fr,1fr]">

        {/* Modo claro/oscuro */}
        {/*<ModeToggle /> */}

        {/* NAVBAR + BOTÓN MOBILE */}
        <div className="relative md:justify-self-center">

          {/* Botón hamburguesa SOLO EN MÓVIL */}
          <div className="relative md:hidden">
            <button
              className="menu-btn"
              onClick={() => setNavOpen(prev => !prev)}
            >
              <span className="material-symbols-rounded">
                {navOpen ? "close" : "menu"}
              </span>
            </button>
          </div>

          {/* Navbar */}
          <Navbar navOpen={navOpen} />
        </div>

        {/* Botón "Contactame" SOLO Desktop */}
        {/*<a
          href="#contact"
          className="btn btn-secondary max-md:hidden flex md:justify-self-end"
        >
          Contactame
        </a>*/}

      </div>
    </header>
  );
};

export default Header;
