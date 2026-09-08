const store = require('./store');
const bus = require('./bus');

async function publishOrder(order) {
  await store.save(order);
  await bus.send(order);
}

module.exports = { publishOrder };
