const app = require('express')();
const http = require('http').createServer(app);
const io = require('socket.io')(http);

io.on('connection', (socket) => {
  console.log('a user connected');

  socket.on('disconnect', () => {
    console.log('user disconnected');
  });

  socket.on('category_list', (data) => {
    console.log('category_list', data);
    io.emit('category_list', data);
  });

  socket.on('category_count', (data) => {
    console.log('category_count', data);
    io.emit('category_count', data);
  });
});

http.listen(3000, () => {
  console.log('listening on *:3000');
});
