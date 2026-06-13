import pygame as pg
import numpy as np

def main():
    pg.init()
    screen= pg.display.set_mode((800,600))
    running=True
    clock=pg.time.Clock()
    fuente_fps = pg.font.SysFont("Arial",30)
    hres=120
    halfvres=100
    hArriba=100
    hAbajo=100
    hVertical=hAbajo+hArriba
    mod = hres/60

    mapa = [
         [1,1,1,1,1,1,1,1],
         [1,0,0,0,0,0,0,1],
         [1,0,1,0,0,0,0,1],
         [1,0,1,0,0,0,0,1],
         [1,0,0,1,1,1,0,1],
         [1,0,0,0,1,0,0,1],
         [1,0,0,0,0,0,0,1],
         [1,1,1,1,1,1,1,1]         ]

    posx,posy,rot=1.5,1.5,0
    frame= np.zeros((hres,hVertical,3))
    sky= pg.image.load('Fondo.png')
    sky=pg.surfarray.array3d(pg.transform.scale(sky,(360,hArriba)))
    floor=pg.surfarray.array3d(pg.image.load('piso.png'))

    while running:
        clock.tick()
        for event in pg.event.get():
            if event.type ==pg.QUIT:
                running =False

        for i in range(hres):
            rot_i= rot+np.deg2rad(i/mod-30)
            sin,cos,cos2=np.sin(rot_i),np.cos(rot_i),np.cos(np.deg2rad(i/mod-30))
            frame[i][:hArriba] = sky[int(np.rad2deg(rot_i)%359)][:hArriba]/255
            
            for j in range(hAbajo):
                n=(hAbajo/(hAbajo-j))/cos2
                x,y=posx+cos*n,posy+sin*n

                xx ,yy = int(x*20), int(y*20)
                shade= 0.2+0.8*(1-j/hAbajo)
                if 0<= xx <100 and 0<=yy<100:
                    frame[i][hVertical-j-1]=shade*floor[xx][yy]/255
                else:
                    frame[i][hVertical-j-1]=[0.1,0.1,0.1]
                
                # xx,yy = int(x*2%1*99), int(y*2%1*99)
                # shade = 0.2 + 0.8 * (1-j/hAbajo)
                # frame[i][hVerical-j-1] = shade*floor[xx][yy]/255

            ray_x, ray_y = posx, posy
            distancia = 0.0001
            
            while distancia < 20:
                ray_x += cos * 0.05
                ray_y += sin * 0.05
                distancia += 0.05
                if 0 <= int(ray_x) < len(mapa) and 0 <= int(ray_y) < len(mapa[0]):
                    if mapa[int(ray_x)][int(ray_y)] == 1:
                        break
            distancia = distancia * cos2
            if distancia <= 0:
                distancia = 0.0001
            altura_pared = int(halfvres / distancia)
            tope_superior = max(0, halfvres - altura_pared)
            tope_inferior = min(hVertical, halfvres + altura_pared)
            sombra = 1 / (1 + distancia * distancia * 0.1)
            color_pared = [0.9 * sombra, 0.2 * sombra, 0.9 * sombra]
            for j in range(int(tope_superior), int(tope_inferior)):
                frame[i][j] = color_pared



        surf=pg.surfarray.make_surface(frame*255)
        surf=pg.transform.scale(surf,(800,600))
        screen.blit(surf,(0,0))
        fps_actuales =int(clock.get_fps())
        texto_superficie=fuente_fps.render(f"FPS:{fps_actuales}",True,(0,255,0))
        screen.blit(texto_superficie,(10,10))
        pg.display.update()
        posx,posy,rot=movimiento(posx,posy,rot,pg.key.get_pressed(),mapa)

def movimiento(posx, posy, rot, keys, mapa):
    if keys[pg.K_LEFT] or keys[ord('a')]:
        rot = rot - 0.1
    if keys[pg.K_RIGHT] or keys[ord('d')]:
        rot = rot + 0.1
        
    if keys[pg.K_UP] or keys[ord('w')]:
        nx = posx + np.cos(rot) * 0.1
        ny = posy + np.sin(rot) * 0.1
        if mapa[int(nx)][int(posy)] == 0:
            posx = nx
        if mapa[int(posx)][int(ny)] == 0:
            posy = ny
            
    if keys[pg.K_DOWN] or keys[ord('s')]:
        nx = posx - np.cos(rot) * 0.1
        ny = posy - np.sin(rot) * 0.1
        if mapa[int(nx)][int(posy)] == 0:
            posx = nx
        if mapa[int(posx)][int(ny)] == 0:
            posy = ny
            
    return posx, posy, rot
    
if __name__ =='__main__':
    main()
    pg.quit()