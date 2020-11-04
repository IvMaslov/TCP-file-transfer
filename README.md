# TCP-file-transfer
It's a data exchange program written in python

Ivan Maslov 3.11.2020

# Overview
It is a small command line file sharing utility written in Python.Tested on version 3.8.3
Runs without additional libraries.The program is based on the built-in socket module.
It uses IPv4 addresses,IPv6 addresses doesn't work.The client chooses which data to send to the server:
text or bytes.Then client enters the name of the file or the line to be sent to the server.
Server accepts data and saves it or prints text to the console.
