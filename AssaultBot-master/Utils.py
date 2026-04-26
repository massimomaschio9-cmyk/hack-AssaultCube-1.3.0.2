from Vector3 import *
from Offsets import *
import math
import win32api

def get_enemies():
    enemies = []
    try:
        # Leggiamo la lista e il conteggio attuale
        list_base = procID.read_int(module_base_address + entity_list_ptr)
        count = procID.read_int(module_base_address + num_players_ptr)
        my_team = procID.read_int(entity_base_address + entity.team_offset)
        
        for i in range(1, count):
            en_ptr = procID.read_int(list_base + (i * 4))
            if not en_ptr: continue
            
            hp = procID.read_int(en_ptr + entity.health_offset)
            team = procID.read_int(en_ptr + entity.team_offset)
            
            # Se è vivo ed è un nemico (team diverso)
            if 0 < hp <= 1000 and team != my_team:
                enemies.append(en_ptr)
    except: pass
    return enemies

def silent_aim():
    if win32api.GetAsyncKeyState(0x01): # Tasto sinistro mouse
        local_pos = Vector3(procID.read_float(entity_base_address + entity.xOffset),
                           procID.read_float(entity_base_address + entity.yOffset),
                           procID.read_float(entity_base_address + entity.zOffset))
        enemies = get_enemies()
        target = None
        min_dist = 9999.0
        
        for en in enemies:
            en_pos = Vector3(procID.read_float(en + entity.xOffset),
                             procID.read_float(en + entity.yOffset),
                             procID.read_float(en + entity.zOffset))
            dist = local_pos.magnitude(en_pos)
            if dist < min_dist:
                min_dist = dist
                target = en_pos
        
        if target:
            procID.write_float(entity_base_address + entity.yawOffset, local_pos.yawAngle(target))
            procID.write_float(entity_base_address + entity.pitchOffset, local_pos.pitchAngle(target))

def get_esp_data(w, h):
    res = []
    try:
        matrix = [procID.read_float(module_base_address + view_matrix_ptr + i*4) for i in range(16)]
        enemies = get_enemies()
        for en in enemies:
            ex = procID.read_float(en + entity.xOffset)
            ey = procID.read_float(en + entity.yOffset)
            ez = procID.read_float(en + entity.zOffset)
            
            clip_w = ex * matrix[3] + ey * matrix[7] + ez * matrix[11] + matrix[15]
            if clip_w < 0.2: continue
            
            clip_x = ex * matrix[0] + ey * matrix[4] + ez * matrix[8] + matrix[12]
            clip_y = ex * matrix[1] + ey * matrix[5] + ez * matrix[9] + matrix[13]
            
            nx, ny = clip_x / clip_w, clip_y / clip_w
            res.append({'x': (w / 2 * nx) + (nx + w / 2), 'y': -(h / 2 * ny) + (ny + h / 2)})
    except: pass
    return res

def mass_kill_score():
    enemies = get_enemies()
    mx = procID.read_float(entity_base_address + entity.xOffset)
    my = procID.read_float(entity_base_address + entity.yOffset)
    mz = procID.read_float(entity_base_address + entity.zOffset)
    for en in enemies:
        # Teletrasporta nemico su di te per darti la kill
        procID.write_float(en + entity.xOffset, mx)
        procID.write_float(en + entity.yOffset, my)
        procID.write_float(en + entity.zOffset, mz)
        procID.write_int(en + entity.health_offset, 0)

def teleport_to_closest():
    enemies = get_enemies()
    if enemies:
        # Prende il primo nemico rilevato
        target = enemies[0]
        tx = procID.read_float(target + entity.xOffset)
        ty = procID.read_float(target + entity.yOffset)
        tz = procID.read_float(target + entity.zOffset)
        procID.write_float(entity_base_address + entity.xOffset, tx)
        procID.write_float(entity_base_address + entity.yOffset, ty)
        procID.write_float(entity_base_address + entity.zOffset, tz)