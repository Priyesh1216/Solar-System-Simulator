import pygame
import sys
import math

pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
#Title of the window
pygame.display.set_caption("Solar System")

#RGB Values for colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)

FONT = pygame.font.SysFont("comicsans", 16)



class Planet:

    #Distance from the sun in meters
    AU = 149.6e6 * 1000

    #Gravitational constant
    G = 6.67428e-11

    # 1AU = 100 pixels CHECK
    SCALE = 250 / AU

    # 1 day
    TIMESTEP = 3600*24

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

        #In kg
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0
        

        #To move in a circular type of motion, need a x-velocity & a y-velocity
        self.x_vel = 0
        self.y_vel = 0


#Draw the circles
    def draw (self, win):
        #Note that top-left is (0,0)
        x = self.x * self.SCALE + WIDTH/2
        y = self.y * self.SCALE + HEIGHT/2

        if len(self.orbit) > 2:
            # To draw the white line following the orbit of the planet
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y* self.SCALE + HEIGHT /2
                updated_points.append((x,y))


            pygame.draw.lines(win, self.color, False, updated_points, 2)

        
        pygame.draw.circle(win, self.color, (x,y), self.radius)


        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 1)}km", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2))



    def attraction (self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y

        distance = math.sqrt(distance_x**2 + distance_y**2)

        if other.sun:
            self.distance_to_sun = distance


        #Straight-line force
        force = self.G * self.mass * other.mass / distance**2

        #To get the angle
        theta = math.atan2(distance_y, distance_x)

        force_x = math.cos(theta)*force
        force_y = math.sin(theta)*force

        return force_x, force_y
    

    # Loop through all the planets, calculate the force of attraction between the current planet and all pf the other planets
    # Calculate what the velocity needs to be for these planets
    # Move the planets by that velocity
    def update_position (self, planets):
        total_fx = total_fy = 0

        for planet in planets:
            #If the planet is itself
            if self == planet:
                continue

            fx, fy = self.attraction (planet)
            total_fx += fx
            total_fy += fy

        # F = m/a
        # a = f / m
        self.x_vel += total_fx / self.mass * self.TIMESTEP

        self.y_vel += total_fy / self.mass * self.TIMESTEP
        

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP  
        self.orbit.append((self.x, self.y))  


def main ():
    run = True

    #To regulate the framerate of our simulation
    clock = pygame.time.Clock()

# Planet (x, y, radius, color, mass)
    sun = Planet(0, 0, 30, YELLOW, 1.98892*10**30 )
    sun.sun = True

    earth = Planet (-1*Planet.AU, 0, 16, BLUE, 5.9742*10**24)
    earth.y_vel = 29.783 * 1000 #m/s

    mars = Planet (-1.524*Planet.AU, 0, 12 , RED, 6.39*10**23)
    mars.y_vel = 24.077 * 1000 #m/s

    mercury = Planet (0.387 *Planet.AU, 0, 9, DARK_GREY, 0.330*10**24)
    mercury.y_vel = - 47.4 * 1000 #m/s

    venus = Planet (0.723 * Planet.AU, 0, 14, WHITE, 4.8685*10**24)
    venus.y_vel = -35.02 * 1000 #m/s
    
    planets = [sun, earth, mars, mercury, venus]

    while run:
        #Run this loop a maxiumum of 60 times per second
        clock.tick(60)         

        WIN.fill((0,0,0))

        #Background
        #WIN.fill(WHITE)

        #Draw on the screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update ()

    pygame.quit()

main ()
