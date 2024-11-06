#!/usr/bin/python

import os
import socket
import select
import pickle
import pygame
import threading

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 22632

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.setblocking(True)

server_socket.bind((IP, PORT))

server_socket.listen(5)

sockets_list = [server_socket]

clients_data = {}

bullets_list = []
scores_dict = {}


def sendData(socket, address, data):
	sent_data = pickle.dumps(data)
	data_header = f"{len(sent_data):<{HEADER_LENGTH}}".encode("utf-8")
	
	try:
		socket.send(data_header + sent_data)

	except ConnectionResetError as e:
		print(f"Closed connection from {clients_data[socket].getUsername()} : {address[0]} / {address[1]}")
		return


def receiveData(client_socket):
	try:
		data_header = client_socket.recv(HEADER_LENGTH)

		if not len(data_header):
			return False

		data_length = int(data_header.decode("utf-8").strip())

		data = client_socket.recv(data_length)

		return pickle.loads(data)

	except Exception as e:
		print(e)
		return False


def control():
	while True:
		command = input()
		if command == "exit()":
			for socket in clients_data:
				socket.close()
			os._exit(0)


def threaded_client(client_socket, client_address):
		player = receiveData(client_socket)

		if not player:
			return

		sockets_list.append(client_socket)

		clients_data[client_socket] = player

		print(f"Welcome to {player.getUsername()} : {client_address[0]} / {client_address[1]}")

		# playsound("./assets/connection_sound.mp3", block=False)

		scores_dict[player.getUsername()] = 0

		players_to_send = [value for key, value in clients_data.items() if key != client_socket]
		data_to_send = {"players": players_to_send, "bullets": bullets_list}
		sendData(client_socket, client_address, data_to_send)

		while True:
			player = receiveData(client_socket)

			if not player:
				print(f"Closed connection from {clients_data[client_socket].getUsername()} : {client_address[0]} / {client_address[1]}")
				sockets_list.remove(client_socket)
				del scores_dict[clients_data[client_socket].getUsername()]
				del clients_data[client_socket]
				return

			##################################################################
			##################### GAME RUNNING ON SERVER #####################
			##################################################################

			touched = 0

			# player.update()

			if player.getShooting():
				bullets_list.append(Bullet(player.getPos() + player.getDirection() * 21, player.getDirection() * 10 + player.getVel()))

			for bullet in bullets_list:
				bullet.update()
				if player.collideWithPoint(bullet.getPos()):
					scores_dict[player.getUsername()] += 1
					bullets_list.remove(bullet)
					touched = 1

				if bullet.isOffScreen():
					if bullet in bullets_list:
						bullets_list.remove(bullet)

			##################################################################
			##################################################################

			clients_data[client_socket] = player

			players_to_send = [value for key, value in clients_data.items() if key != client_socket]
			data_to_send = {"players": players_to_send, "bullets": bullets_list, "scores" : scores_dict, "touched" : touched}
			sendData(client_socket, client_address, data_to_send)


control_thread = threading.Thread(target=control)
control_thread.start()

while True:
	client_socket, client_address = server_socket.accept()

	client_thread = threading.Thread(target=threaded_client, args=(client_socket, client_address))
	client_thread.start()

