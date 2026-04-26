from Memory import *

# Indirizzi aggiornati per AssaultCube 1.3.0.2
entity_list_ptr = 0x18AC04   # Lista dei giocatori
num_players_ptr = 0x191FD4   # Numero di giocatori nel server
local_player_ptr = 0x17E0A8  # Il tuo personaggio
view_matrix_ptr = 0x17DFD0   # Matrice per il calcolo ESP

class Entity:
    health_offset = 0xEC
    team_offset = 0x30C
    xOffset = 0x4
    yOffset = 0x8
    zOffset = 0xC
    yawOffset = 0x34
    pitchOffset = 0x38
    ammo_offset = 0x140 

entity = Entity()

# Caricamento dinamico della base del giocatore locale
try:
    entity_base_address = procID.read_int(module_base_address + local_player_ptr)
except:
    entity_base_address = 0