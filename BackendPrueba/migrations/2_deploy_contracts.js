const VotacionBlockchain = artifacts.require("VotacionBlockchain");

module.exports = function (deployer) {
  deployer.deploy(VotacionBlockchain, {
    gas: 8000000
  });
};
