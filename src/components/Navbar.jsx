/**
 * Node Modules
 */
import { useRef, useEffect } from "react";
import PropTypes from "prop-types";

const Navbar = ({ navOpen }) => {
  const lastActiveLink = useRef(null);
  const activeBox = useRef(null);

  const initActiveBox = () => {
    if (!lastActiveLink.current || !activeBox.current) return;

    const el = lastActiveLink.current;
    activeBox.current.style.top = el.offsetTop + "px";
    activeBox.current.style.left = el.offsetLeft + "px";
    activeBox.current.style.width = el.offsetWidth + "px";
    activeBox.current.style.height = el.offsetHeight + "px";
  };

  useEffect(() => {
    initActiveBox();
    window.addEventListener("resize", initActiveBox);

    return () => window.removeEventListener("resize", initActiveBox);
  }, []);

  const activeCurrentLink = (e) => {
    if (!e.target.classList.contains("nav-link")) return;

    lastActiveLink.current?.classList.remove("active");
    e.target.classList.add("active");
    lastActiveLink.current = e.target;

    activeBox.current.style.top = e.target.offsetTop + "px";
    activeBox.current.style.left = e.target.offsetLeft + "px";
    activeBox.current.style.width = e.target.offsetWidth + "px";
    activeBox.current.style.height = e.target.offsetHeight + "px";
  };

  // Items del navbar
  const navItems = [
    {
      label: "Votaciones",
      link: "#tipos",
      className: "nav-link active",
      ref: lastActiveLink,
    },
    {
      label: "Informacion",
      link: "#info",
      className: "nav-link",
    },
    {
      label: "Resultados",
      link: "#results",
      className: "nav-link",
    }
  ];

  return (
    <nav className={`navbar ${navOpen ? "active" : ""}`} onClick={activeCurrentLink}>
      {navItems.map(({ label, link, className, ref }, key) => (
        <a
          href={link}
          className={className}
          key={key}
          ref={ref ? ref : null}
        >
          {label}
        </a>
      ))}

      <div className="active-box" ref={activeBox}></div>
    </nav>
  );
};

Navbar.propTypes = {
  navOpen: PropTypes.bool.isRequired,
};

export default Navbar;
