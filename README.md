# httpserver-from-scratch

I wanted to understand what exactly is happening when I send and receive files from web servers using the protocol 'HTTP'.

I now understand that the communication between a client (requester) and server (responder) is established using TCP (Transfer Control Protocol) for transmitting the client socket and address to the server socket over the internet (via IP i.e. Internet Protocol).

I have also implemented a WSGI (Web Server Gateway Interface) that takes allows exchange of data packets between the web application (that communicated with the web server), and the client.