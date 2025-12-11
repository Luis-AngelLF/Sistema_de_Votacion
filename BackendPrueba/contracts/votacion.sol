// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title VotacionBlockchain
 * @dev Contrato para almacenar pruebas de auditoría de votos y resultados.
 *      NO almacena votos cifrados, solo hashes y metadata mínima.
 */
contract VotacionBlockchain {
    
    // ============================================
    // ESTRUCTURAS
    // ============================================

    struct RegistroVoto {
        uint256 idEleccion;      // Elección a la que pertenece el voto
        uint256 idVoto;          // ID interno del voto en la base de datos
        bytes32 hashVoto;        // Hash del ciphertext
        uint256 timestamp;       // Momento en blockchain
        address registradoPor;   // Dirección que realizó el registro
    }

    struct Eleccion {
        uint256 idEleccion;
        string nombre;
        uint256 fechaInicio;
        uint256 fechaFin;
        bool activa;
        address creador;
        uint256 totalVotos;
    }

    struct ResultadoEleccion {
        uint256 idEleccion;
        uint256 idCandidato;
        bytes32 hashResultado;   // Hash de la suma homomórfica
        uint256 timestamp;
    }

    // ============================================
    // VARIABLES DE ESTADO
    // ============================================

    mapping(bytes32 => RegistroVoto) public votos;
    mapping(uint256 => Eleccion) public elecciones;
    mapping(uint256 => bytes32[]) public votosPorEleccion;
    mapping(uint256 => mapping(uint256 => ResultadoEleccion)) public resultados;

    address public admin;
    uint256 public totalVotosGlobal;

    // ============================================
    // EVENTOS
    // ============================================

    event VotoRegistrado(bytes32 indexed hashVoto, uint256 indexed idEleccion, uint256 idVoto);
    event EleccionCreada(uint256 indexed idEleccion, string nombre);
    event EleccionCerrada(uint256 indexed idEleccion);
    event ResultadoPublicado(uint256 indexed idEleccion, uint256 indexed idCandidato, bytes32 hashResultado);

    // ============================================
    // MODIFICADORES
    // ============================================

    modifier soloAdmin() {
        require(msg.sender == admin, "No autorizado");
        _;
    }

    modifier eleccionActiva(uint256 _idEleccion) {
        Eleccion memory e = elecciones[_idEleccion];
        require(e.activa, "Eleccion cerrada");
        require(block.timestamp >= e.fechaInicio && block.timestamp <= e.fechaFin, "Fuera de tiempo");
        _;
    }

    // ============================================
    // CONSTRUCTOR
    // ============================================

    constructor() {
        admin = msg.sender;
    }

    // ============================================
    // FUNCIONES
    // ============================================

    function crearEleccion(
        uint256 _idEleccion,
        string memory _nombre,
        uint256 _inicio,
        uint256 _fin
    ) public soloAdmin {
        require(!elecciones[_idEleccion].activa, "Ya existe");

        elecciones[_idEleccion] = Eleccion({
            idEleccion: _idEleccion,
            nombre: _nombre,
            fechaInicio: _inicio,
            fechaFin: _fin,
            activa: true,
            creador: msg.sender,
            totalVotos: 0
        });

        emit EleccionCreada(_idEleccion, _nombre);
    }

    function registrarVoto(
        uint256 _idEleccion,
        uint256 _idVoto,
        bytes32 _hashVoto
    ) public eleccionActiva(_idEleccion) returns (bytes32) {

        require(votos[_hashVoto].timestamp == 0, "Ya existe");

        votos[_hashVoto] = RegistroVoto({
            idEleccion: _idEleccion,
            idVoto: _idVoto,
            hashVoto: _hashVoto,
            timestamp: block.timestamp,
            registradoPor: msg.sender
        });

        votosPorEleccion[_idEleccion].push(_hashVoto);
        elecciones[_idEleccion].totalVotos++;
        totalVotosGlobal++;

        emit VotoRegistrado(_hashVoto, _idEleccion, _idVoto);
        return _hashVoto;
    }

    function cerrarEleccion(uint256 _idEleccion) public soloAdmin {
        require(elecciones[_idEleccion].activa, "Ya cerrada");
        elecciones[_idEleccion].activa = false;
        emit EleccionCerrada(_idEleccion);
    }

    function publicarResultado(
        uint256 _idEleccion,
        uint256 _idCandidato,
        bytes32 _hashResultado
    ) public soloAdmin {

        resultados[_idEleccion][_idCandidato] = ResultadoEleccion({
            idEleccion: _idEleccion,
            idCandidato: _idCandidato,
            hashResultado: _hashResultado,
            timestamp: block.timestamp
        });

        emit ResultadoPublicado(_idEleccion, _idCandidato, _hashResultado);
    }
}
