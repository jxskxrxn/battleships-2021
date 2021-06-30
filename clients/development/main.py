# imports
import os
import threading
import time
from client import Battleship

# Linking to the redis server

grpc_host = os.getenv('GRPC_HOST', 'localhost')
grpc_port = os.getenv('GRPC_PORT', '50051')

playing = threading.Event()
playing.set()

battleship = Battleship(grpc_host=grpc_host, grpc_port=grpc_port)

# globally defined variables to use through out the program
global shipHits
global s
# ship hits = amount of hits needed to destroy the ship
shipHits = 0


@battleship.on()
def begin():
    print("--BATTLESHIPS--")


# start turn event, if input matches those coordinates it will proceed otherwise throw an error

@battleship.on()
def start_turn():
    global shipHits
    board_data(player1_board)
    while True:
        if shipHits > 0:
            global s
            s = input('Unleash the cannons!! Shoot eg(A1,B1): ').upper()
            if s == "A1" or s == "A2" or s == "A3" or s == "A4" or s == "A5" or s == "A6" or s == "A7" or s == "A8" or s == "A9" or s == "A10" \
                    or s == "B1" or s == "B2" or s == "B3" or s == "B4" or s == "B5" or s == "B6" or s == "B7" or s == "A8" or s == "A9" or s == "A10" \
                    or s == "C1" or s == "C2" or s == "C3" or s == "C4" or s == "C5" or s == "C6" or s == "C7" or s == "C8" or s == "C9" or s == "C10" \
                    or s == "D1" or s == "D2" or s == "D3" or s == "D4" or s == "D5" or s == "D6" or s == "D7" or s == "D8" or s == "D9" or s == "D10" \
                    or s == "E1" or s == "E2" or s == "E3" or s == "E4" or s == "E5" or s == "E6" or s == "E7" or s == "E8" or s == "E9" or s == "E10" \
                    or s == "F1" or s == "F2" or s == "F3" or s == "F4" or s == "F5" or s == "F6" or s == "F7" or s == "F8" or s == "F9" or s == "F10" \
                    or s == "G1" or s == "G2" or s == "G3" or s == "G4" or s == "G5" or s == "G6" or s == "G7" or s == "G8" or s == "G9" or s == "G10" \
                    or s == "H1" or s == "H2" or s == "H3" or s == "H4" or s == "H5" or s == "H6" or s == "H7" or s == "H8" or s == "H9" or s == "H10" \
                    or s == "I1" or s == "I2" or s == "I3" or s == "I4" or s == "I5" or s == "I6" or s == "I7" or s == "I8" or s == "I9" or s == "I10" \
                    or s == "J1" or s == "J2" or s == "J3" or s == "J4" or s == "J5" or s == "J6" or s == "J7" or s == "J8" or s == "J9" or s == "J10":
                battleship.attack(s)
                break
            else:
                print("Invalid coordinates! Try again")
            continue
        else:
            lose()
            break


# hit event prints an X on hit
@battleship.on()
def hit():
    global s
    player2_board[s] = "X"
    board_data(player2_board)
    print('HIT')


# miss event also checks if you shoot at one coordinate more than once and prints a O
@battleship.on()
def miss():
    global s
    while True:
        if player2_board[s] == "X":
            player2_board[s] = "X"
            board_data(player2_board)
            print('You already shot at those coordinates')
            break
        else:
            player2_board[s] = "O"
            board_data(player2_board)
            print('MISS!')
            break
        continue


# win event sends a message to the player who won
@battleship.on()
def win():
    global s
    player2_board[s] = "X"
    board_data(player2_board)
    print('You WON!! :)')
    playing.clear()


# lose event sends the message to the loser
@battleship.on()
def lose():
    board_data(player1_board)
    print('Game over, You LOST :(')
    playing.clear()


# attack event takes care of sending and receiving attacks at given coordinates
@battleship.on()
def attack(vector):
    global shipHits
    vector = vector[0]
    while True:
        if player1_board[vector] != ' ' and player1_board[vector] != 'M' and player1_board[vector] != 'H':
            player1_board[vector] = 'H'
            battleship.hit()
            shipHits = shipHits - 1
            if shipHits <= 0:
                print(f'Shot hit your ship at {vector}. ')
                print('Ship has lost 1 Hit')
                print(shipHits, "Hit Points remaining.\n")
                try:
                    battleship.defeat()
                except:
                    continue
                break
            else:
                print(f'Shot hit your ship at {vector}. ')
                print('Ship has lost 1 Hit')
                print(shipHits, "Hit Points remaining.\n")
            break

        elif player1_board[vector] == ' ' or player1_board[vector] == 'M':
            player1_board[vector] = 'M'
            battleship.miss()
            print(f'Shot landed close to your fleet; at {vector}')
            print(shipHits, " Hit Points remaining.\n")
            break

        elif player1_board[vector] == 'H':
            battleship.miss()
            print(f'Shot hit again at {vector}. No damage taken ')
            print(shipHits, " Hit Points remaining.\n")
            break

        continue


# adding the ships to the grid with a given length and number of ships
def add_ships():
    add_patrol_boat(1, 2)
    add_destroyer(2, 2)
    add_cruiser(3, 1)
    add_submarine(3, 3)
    add_battleship(4, 1)
    add_aircraft_carrier(5, 1)


# adds the patrol boat to the grid
def add_patrol_boat(patrol_boat_length, patrol_boat_available):
    const_length = patrol_boat_length
    while patrol_boat_available > 0:
        patrol_boat_length = const_length
        while patrol_boat_length > 0:
            global shipHits
            try:
                board_data(player1_board)
                print("Patrol Boats available: ", patrol_boat_available)
                print("Patrol Boat Hits unused: ", patrol_boat_length)
                patrol_boat = input("Place the Patrol Boats anywhere in the board: ").upper()
                if player1_board[patrol_boat] == ' ':
                    player1_board[patrol_boat] = "P"
                    shipHits = shipHits + 1
                    patrol_boat_length = patrol_boat_length - 1
                else:
                    print("Ship is already placed there! Try a different coordinate")
            except:
                print("Invalid input. Try again!")
                continue

        patrol_boat_available = patrol_boat_available - 1
        print("Patrol Boats deployed!.")


def add_destroyer(destroyer_length, destroyer_available):
    const_length = destroyer_length
    while destroyer_available > 0:
        destroyer_length = const_length
        while destroyer_length > 0:
            global shipHits
            try:
                board_data(player1_board)
                print("Destroyers available: ", destroyer_available)
                print("Destroyer Hits unused: ", destroyer_length)
                destroyer = input("Place the Destroyers anywhere in the board: ").upper()
                if player1_board[destroyer] == ' ':
                    player1_board[destroyer] = "D"
                    shipHits = shipHits + 1
                    destroyer_length = destroyer_length - 1
                else:
                    print("Ship is already placed there! Try a different coordinate")
            except:
                print("Invalid input. Try again!")
                continue

        destroyer_available = destroyer_available - 1
        print("Destroyers deployed!.")


def add_cruiser(cruiser_length, cruiser_available):
    const_length = cruiser_length
    while cruiser_available > 0:
        cruiser_length = const_length
        while cruiser_length > 0:
            global shipHits
            try:
                board_data(player1_board)
                print("Cruisers available: ", cruiser_available)
                print("Cruiser Hits unused: ", cruiser_length)
                cruiser = input("Place the Cruisers anywhere in the board: ").upper()
                if player1_board[cruiser] == ' ':
                    player1_board[cruiser] = "C"
                    shipHits = shipHits + 1
                    cruiser_length = cruiser_length - 1
                else:
                    print("Ship is already placed there! Try a different coordinate")
            except:
                print("Invalid input. Try again!")
                continue

        cruiser_available = cruiser_available - 1
        print("Cruisers added to the board.")


def add_submarine(submarine_length, submarine_available):
    const_length = submarine_length
    while submarine_available > 0:
        submarine_length = const_length
        while submarine_length > 0:
            global shipHits
            try:
                board_data(player1_board)
                print("Submarines available: ", submarine_available)
                print("Submarine Hits unused: ", submarine_length)
                submarine = input("Place the Submarines anywhere in the board: ").upper()
                if player1_board[submarine] == ' ':
                    player1_board[submarine] = "S"
                    shipHits = shipHits + 1
                    submarine_length = submarine_length - 1
                else:
                    print("Ship is already placed there! Try a different coordinate")
            except:
                print("Invalid input. Try again!")
                continue

        submarine_available = submarine_available - 1
        print("Submarine added to the board!")


def add_battleship(battleship_length, battleship_available):
    const_length = battleship_length
    while battleship_available > 0:
        battleship_length = const_length
        while battleship_length > 0:
            global shipHits
            try:
                board_data(player1_board)
                print("Battleships available: ", battleship_available)
                print("Battleships hits unused: ", battleship_length)
                battle_ship = input("Place the Battleship anywhere in the board: ").upper()
                if player1_board[battle_ship] == ' ':
                    player1_board[battle_ship] = "B"
                    shipHits = shipHits + 1
                    battleship_length = battleship_length - 1
                else:
                    print("Ship is already placed there! Try a different coordinate")
            except:
                print("Invalid input. Try again!")
                continue

        battleship_available = battleship_available - 1
        print("Battleship added to the board!")


def add_aircraft_carrier(aircraft_carrier_length, aircraft_carrier_available):
    const_length = aircraft_carrier_length
    while aircraft_carrier_available > 0:
        aircraft_carrier_length = const_length
        while aircraft_carrier_length > 0:
            global shipHits
            try:
                board_data(player1_board)
                print("Aircraft Carriers available: ", aircraft_carrier_available)
                print("Aircraft Carriers Hits unused: ", aircraft_carrier_length)
                aircraft_carrier = input("Place the Battleship anywhere in the board: ").upper()
                if player1_board[aircraft_carrier] == ' ':
                    player1_board[aircraft_carrier] = "A"
                    shipHits = shipHits + 1
                    aircraft_carrier_length = aircraft_carrier_length - 1
                else:
                    print("Ship is already placed there! Try a different coordinate")
            except:
                print("Invalid input. Try again!")
                continue

        aircraft_carrier_available = aircraft_carrier_available - 1
        print("Aircraft Carrier added to the board!")


player1_board = {'A1': ' ', 'A2': ' ', 'A3': ' ', 'A4': ' ', 'A5': ' ', 'A6': ' ', 'A7': ' ', 'A8': ' ', 'A9': ' ',
                 'A10': ' ',
                 'B1': ' ', 'B2': ' ', 'B3': ' ', 'B4': ' ', 'B5': ' ', 'B6': ' ', 'B7': ' ', 'B8': ' ', 'B9': ' ',
                 'B10': ' ',
                 'C1': ' ', 'C2': ' ', 'C3': ' ', 'C4': ' ', 'C5': ' ', 'C6': ' ', 'C7': ' ', 'C8': ' ', 'C9': ' ',
                 'C10': ' ',
                 'D1': ' ', 'D2': ' ', 'D3': ' ', 'D4': ' ', 'D5': ' ', 'D6': ' ', 'D7': ' ', 'D8': ' ', 'D9': ' ',
                 'D10': ' ',
                 'E1': ' ', 'E2': ' ', 'E3': ' ', 'E4': ' ', 'E5': ' ', 'E6': ' ', 'E7': ' ', 'E8': ' ', 'E9': ' ',
                 'E10': ' ',
                 'F1': ' ', 'F2': ' ', 'F3': ' ', 'F4': ' ', 'F5': ' ', 'F6': ' ', 'F7': ' ', 'F8': ' ', 'F9': ' ',
                 'F10': ' ',
                 'G1': ' ', 'G2': ' ', 'G3': ' ', 'G4': ' ', 'G5': ' ', 'G6': ' ', 'G7': ' ', 'G8': ' ', 'G9': ' ',
                 'G10': ' ',
                 'H1': ' ', 'H2': ' ', 'H3': ' ', 'H4': ' ', 'H5': ' ', 'H6': ' ', 'H7': ' ', 'H8': ' ', 'H9': ' ',
                 'H10': ' ',
                 'I1': ' ', 'I2': ' ', 'I3': ' ', 'I4': ' ', 'I5': ' ', 'I6': ' ', 'I7': ' ', 'I8': ' ', 'I9': ' ',
                 'I10': ' ',
                 'J1': ' ', 'J2': ' ', 'J3': ' ', 'J4': ' ', 'J5': ' ', 'J6': ' ', 'J7': ' ', 'J8': ' ', 'J9': ' ',
                 'J10': ' '}

player2_board = {'A1': ' ', 'A2': ' ', 'A3': ' ', 'A4': ' ', 'A5': ' ', 'A6': ' ', 'A7': ' ', 'A8': ' ', 'A9': ' ',
                 'A10': ' ',
                 'B1': ' ', 'B2': ' ', 'B3': ' ', 'B4': ' ', 'B5': ' ', 'B6': ' ', 'B7': ' ', 'B8': ' ', 'B9': ' ',
                 'B10': ' ',
                 'C1': ' ', 'C2': ' ', 'C3': ' ', 'C4': ' ', 'C5': ' ', 'C6': ' ', 'C7': ' ', 'C8': ' ', 'C9': ' ',
                 'C10': ' ',
                 'D1': ' ', 'D2': ' ', 'D3': ' ', 'D4': ' ', 'D5': ' ', 'D6': ' ', 'D7': ' ', 'D8': ' ', 'D9': ' ',
                 'D10': ' ',
                 'E1': ' ', 'E2': ' ', 'E3': ' ', 'E4': ' ', 'E5': ' ', 'E6': ' ', 'E7': ' ', 'E8': ' ', 'E9': ' ',
                 'E10': ' ',
                 'F1': ' ', 'F2': ' ', 'F3': ' ', 'F4': ' ', 'F5': ' ', 'F6': ' ', 'F7': ' ', 'F8': ' ', 'F9': ' ',
                 'F10': ' ',
                 'G1': ' ', 'G2': ' ', 'G3': ' ', 'G4': ' ', 'G5': ' ', 'G6': ' ', 'G7': ' ', 'G8': ' ', 'G9': ' ',
                 'G10': ' ',
                 'H1': ' ', 'H2': ' ', 'H3': ' ', 'H4': ' ', 'H5': ' ', 'H6': ' ', 'H7': ' ', 'H8': ' ', 'H9': ' ',
                 'H10': ' ',
                 'I1': ' ', 'I2': ' ', 'I3': ' ', 'I4': ' ', 'I5': ' ', 'I6': ' ', 'I7': ' ', 'I8': ' ', 'I9': ' ',
                 'I10': ' ',
                 'J1': ' ', 'J2': ' ', 'J3': ' ', 'J4': ' ', 'J5': ' ', 'J6': ' ', 'J7': ' ', 'J8': ' ', 'J9': ' ',
                 'J10': ' '}


def board_data(board):
    print('     1   2   3   4   5   6   7   8   9   10  ')
    print('   +---+---+---+---+---+---+---+---+---+---+')
    print(' A' + ' | ' + board['A1'] + ' | ' + board['A2'] + ' | ' + board['A3'] + ' | ' + board['A4'] + ' | ' +
          board[
              'A5'] + ' | ' + board['A6'] + ' | ' + board['A7'] + ' | ' + board['A8'] + ' | ' + board[
              'A9'] + ' | ' + board[
              'A10'] + ' | ')

    print('   +---+---+---+---+---+---+---+---+---+---+')
    print(
        ' B' ' | ' + board['B1'] + ' | ' + board['B2'] + ' | ' + board['B3'] + ' | ' + board['B4'] + ' | ' + board[
            'B5'] + ' | ' + board['B6'] + ' | ' + board['B7'] + ' | ' + board['B8'] + ' | ' + board['B9'] + ' | ' +
        board[
            'B10'] + ' | ')

    print('   +---+---+---+---+---+---+---+---+---+---+')
    print(
        ' C' ' | ' + board['C1'] + ' | ' + board['C2'] + ' | ' + board['C3'] + ' | ' + board['C4'] + ' | ' + board[
            'C5'] + ' | ' + board['C6'] + ' | ' + board['C7'] + ' | ' + board['C8'] + ' | ' + board['C9'] + ' | ' +
        board[
            'C10'] + ' | ')

    print('   +---+---+---+---+---+---+---+---+---+---+')
    print(
        ' D' ' | ' + board['D1'] + ' | ' + board['D2'] + ' | ' + board['D3'] + ' | ' + board['D4'] + ' | ' + board[
            'D5'] + ' | ' + board['D6'] + ' | ' + board['D7'] + ' | ' + board['D8'] + ' | ' + board['D9'] + ' | ' +
        board[
            'D10'] + ' | ')

    print('   +---+---+---+---+---+---+---+---+---+---+')
    print(
        ' E' ' | ' + board['E1'] + ' | ' + board['E2'] + ' | ' + board['E3'] + ' | ' + board['E4'] + ' | ' + board[
            'E5'] + ' | ' + board['E6'] + ' | ' + board['E7'] + ' | ' + board['E8'] + ' | ' + board['E9'] + ' | ' +
        board[
            'E10'] + ' | ')

    print('   +---+---+---+---+---+---+---+---+---+---+')
    print(
        ' F' ' | ' + board['F1'] + ' | ' + board['F2'] + ' | ' + board['F3'] + ' | ' + board['F4'] + ' | ' + board[
            'F5'] + ' | ' + board['F6'] + ' | ' + board['F7'] + ' | ' + board['F8'] + ' | ' + board['F9'] + ' | ' +
        board[
            'F10'] + ' | ')

    print('   +---+---+---+---+---+---+---+---+---+---+')
    print(
        ' G' ' | ' + board['G1'] + ' | ' + board['G2'] + ' | ' + board['G3'] + ' | ' + board['G4'] + ' | ' + board[
            'G5'] + ' | ' + board['G6'] + ' | ' + board['G7'] + ' | ' + board['G8'] + ' | ' + board['G9'] + ' | ' +
        board[
            'G10'] + ' | ')

    print('   +---+---+---+---+---+---+---+---+---+---+')
    print(
        ' H' ' | ' + board['H1'] + ' | ' + board['H2'] + ' | ' + board['H3'] + ' | ' + board['H4'] + ' | ' + board[
            'H5'] + ' | ' + board['H6'] + ' | ' + board['H7'] + ' | ' + board['H8'] + ' | ' + board['H9'] + ' | ' +
        board[
            'H10'] + ' | ')

    print('   +---+---+---+---+---+---+---+---+---+---+')
    print(
        ' I' ' | ' + board['I1'] + ' | ' + board['I2'] + ' | ' + board['I3'] + ' | ' + board['I4'] + ' | ' + board[
            'I5'] + ' | ' + board['I6'] + ' | ' + board['I7'] + ' | ' + board['I8'] + ' | ' + board['I9'] + ' | ' +
        board[
            'I10'] + ' | ')

    print('   +---+---+---+---+---+---+---+---+---+---+')
    print(
        ' J' ' | ' + board['J1'] + ' | ' + board['J2'] + ' | ' + board['J3'] + ' | ' + board['J4'] + ' | ' + board[
            'J5'] + ' | ' + board['J6'] + ' | ' + board['J7'] + ' | ' + board['J8'] + ' | ' + board['J9'] + ' | ' +
        board[
            'J10'] + ' | ')
    print('   +---+---+---+---+---+---+---+---+---+---+\n')


print("\n")
print("WELCOME TO BATTLESHIPS!!")
print("\n")
add_ships()
board_data(player1_board)
print('Waiting for the game to start...')
battleship.join()
while playing.is_set():
    time.sleep(1.0)
