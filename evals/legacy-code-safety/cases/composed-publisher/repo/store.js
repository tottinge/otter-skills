async function save(order) {
  throw new Error(`production store unavailable for ${order.id}`);
}

module.exports = { save };
