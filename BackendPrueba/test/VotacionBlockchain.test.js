const VotacionBlockchain = artifacts.require("VotacionBlockchain");

contract("VotacionBlockchain", (accounts) => {

  const admin = accounts[0];
  const user1 = accounts[1];
  const user2 = accounts[2];

  let contrato;

  before(async () => {
    contrato = await VotacionBlockchain.deployed();
  });

  it("Debe crear una elección correctamente", async () => {
    const idEleccion = 1;
    const nombre = "Eleccion Presidencial";
    const inicio = Math.floor(Date.now() / 1000) - 5;
    const fin = Math.floor(Date.now() / 1000) + 999;

    const tx = await contrato.crearEleccion(idEleccion, nombre, inicio, fin, { from: admin });

    assert.equal(tx.logs[0].event, "EleccionCreada", "Evento incorrecto");

    const eleccion = await contrato.elecciones(idEleccion);
    assert.equal(eleccion.idEleccion.toNumber(), idEleccion);
    assert.equal(eleccion.nombre, nombre);
    assert.equal(eleccion.activa, true);
  });

  it("Debe registrar un voto correctamente", async () => {
    const idEleccion = 1;
    const idVoto = 10;
    const hashVoto = web3.utils.soliditySha3("testvote123"); // hash simulado

    const tx = await contrato.registrarVoto(idEleccion, idVoto, hashVoto, { from: user1 });

    assert.equal(tx.logs[0].event, "VotoRegistrado", "Evento incorrecto");
    assert.equal(tx.logs[0].args.hashVoto, hashVoto);

    const voto = await contrato.votos(hashVoto);
    assert.equal(voto.idEleccion.toNumber(), idEleccion);
    assert.equal(voto.idVoto.toNumber(), idVoto);
    assert.equal(voto.hashVoto, hashVoto);
  });

  it("Debe evitar votos duplicados", async () => {
    const idEleccion = 1;
    const idVoto = 11;
    const hashVoto = web3.utils.soliditySha3("duplicado123");

    await contrato.registrarVoto(idEleccion, idVoto, hashVoto, { from: user2 });

    try {
      await contrato.registrarVoto(idEleccion, idVoto, hashVoto, { from: user2 });
      assert.fail("El contrato aceptó un voto duplicado");
    } catch (error) {
      assert.include(error.message, "Ya existe");
    }
  });

  it("Debe cerrar una elección", async () => {
    const idEleccion = 1;

    const tx = await contrato.cerrarEleccion(idEleccion, { from: admin });

    assert.equal(tx.logs[0].event, "EleccionCerrada");

    const eleccion = await contrato.elecciones(idEleccion);
    assert.equal(eleccion.activa, false);
  });

  it("Debe publicar un resultado", async () => {
    const idEleccion = 1;
    const idCandidato = 5;
    const hashResultado = web3.utils.soliditySha3("resultado123");

    const tx = await contrato.publicarResultado(idEleccion, idCandidato, hashResultado, { from: admin });

    assert.equal(tx.logs[0].event, "ResultadoPublicado");

    const resultado = await contrato.resultados(idEleccion, idCandidato);
    assert.equal(resultado.hashResultado, hashResultado);
  });

});
