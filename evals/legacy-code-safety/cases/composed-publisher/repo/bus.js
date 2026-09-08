async function send(order) {
  throw new Error(`production bus unavailable for ${order.id}`);
}

module.exports = { send };
