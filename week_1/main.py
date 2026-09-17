import pygame
import numpy as np
import random

# Configuration

WIDTH = 800
HEIGHT = 800

BOWL_CENTER = np.array([WIDTH / 2, HEIGHT / 2], dtype=float)
BOWL_RADIUS = 300

# Start with 1 ball, then 2. Many at once is the bonus.
NUM_PARTICLES = 20
PARTICLE_RADIUS = 12
PARTICLE_SPEED = 150.0

# Pixels per second squared, not m/s^2. Note that +y points DOWN on screen.
GRAVITY = 900.0

# How much speed survives a bounce. 1.0 loses nothing, below 1.0 is weaker.
WALL_RESTITUTION = 1.0
RESTITUTION = 1.003
DAMPING_FACTOR = 0.0055       # trail and error value 

FPS = 60

positions = []
velocities = []

for i in range(NUM_PARTICLES):

    # A random spot inside the bowl, with the whole ball fitting.
    angle = random.uniform(0, 2 * np.pi)
    distance = random.uniform(0,BOWL_RADIUS-PARTICLE_RADIUS)

    positions.append(BOWL_CENTER + distance * np.array([
        np.cos(angle),
        np.sin(angle)
    ]))

    # A random direction, at roughly PARTICLE_SPEED.
    # Swap for np.array([0.0, 0.0]) to drop the ball from rest.
    angle = random.uniform(0, 2 * np.pi)

    velocities.append(PARTICLE_SPEED * np.array([
        np.cos(angle),
        np.sin(angle)
    ]))

# Pygame setup

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Particle Simulation")

clock = pygame.time.Clock()

running = True

# Main loop

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    # Seconds since the last frame. This is your timestep.
    dt = clock.tick(FPS) / 1000.0

    ###########################################################################
    # TODO: Make every ball fall, and bounce it off the wall of the bowl.     #
    #                                                                         #
    # Two things happen here, in an order that matters.                       #
    #                                                                         #
    # First, it falls. Gravity is an acceleration, so ask yourself what it    #
    # changes directly: the position, or the velocity? And once that has      #
    # changed, what does the ball's new position depend on?                   #
    #                                                                         #
    # Second, it has to stay in the bowl. Work out how you would even         #
    # tell that it has escaped, given that you know where the centre of       #
    # the bowl is, how wide the bowl is, and how wide the ball is.            #
    # Careful: the ball is drawn with a radius of its own, so its edge        #
    # reaches the wall before its centre would.                               #
    #                                                                         #
    # Once you know it has escaped, two things need fixing. Where should      #
    # the ball actually be, and what should its velocity become? For the      #
    # velocity, only the part heading into the wall should change. The        #
    # part sliding along the wall carries on untouched. WALL_RESTITUTION      #
    # decides how much of the incoming speed comes back out.                  #
    ###########################################################################
    
    # CODE STARTS HERE.

    for i in range(NUM_PARTICLES):
        velocities[i] += [0, GRAVITY*dt]    #kind of same thing here, updates the velocity vecotr on basis of accelaration. 
        #HERE IM UPDATING THE VELOCITY BEFORE THE POSITION BECAUSE 
        positions[i] += velocities[i]*dt    #updates position vector to make it such that vector constantly changes on basis of velocity
    

        normal_vector = positions[i]-BOWL_CENTER                                                                                #makes normal vector perpendicular to bowl at the point of conact between the ball & bowl
        normal_vector_magnitude = np.linalg.norm(normal_vector)                                                                 #assigns magnitude of normal
        normal_component_of_velocities_magnitude = np.dot(normal_vector,velocities[i])/normal_vector_magnitude                  #this is very important, it basically calculates the magnitude of the component of the velocity vecor which is in the direction of the normal
        normal_component_of_velocities = normal_vector * (normal_component_of_velocities_magnitude/normal_vector_magnitude)     #makes the normal componenet with magnitude info from the above line
        tangential_component_of_velocities = velocities[i] - normal_component_of_velocities                                     #this is used to make the tangential component

        #the above code is used to split the velocity vector into 2 perpendicular coponenets, one in the normal and other in the tangetial direction

        if (normal_vector_magnitude)>BOWL_RADIUS-PARTICLE_RADIUS:
            #offset = normal_vector_0*(np.linalg.norm(positions[0])-BOWL_RADIUS)
            #positions[0] -= offset

            unit_normal = normal_vector / np.linalg.norm(normal_vector)
            positions[i] = BOWL_CENTER + unit_normal * (BOWL_RADIUS-PARTICLE_RADIUS)        #these 2 lines are used to correct clipping the of ball outside the bowl. 

            velocities[i] =  tangential_component_of_velocities - (RESTITUTION)*normal_component_of_velocities       
            #this is the main thing, it keeps the tangential vecotr the same, and multiplies restitution and switches direction 
            #of normal componenet

    

    ###########################################################################
    #                            END OF YOUR CODE                             #
    ###########################################################################

    ###########################################################################
    # TODO: Make the balls bounce off each other.                             #
    #                                                                         #
    # Start with the condition. Given two balls, what has to be true          #
    # about where they are for them to be touching? Every ball has the        #
    # same radius, which makes this simpler than it sounds.                   #
    #                                                                         #
    # Then the response. A collision changes velocities, not positions.       #
    # Which direction does the change act along, and how would you get        #
    # that direction from the two positions you have? Only the motion         #
    # along that direction matters, the rest is unaffected.                   #
    #                                                                         #
    # One trap worth thinking about: two balls that are overlapping but       #
    # already moving apart should be left alone. If you bounce them again     #
    # they will get stuck together. How would you tell "approaching"          #
    # from "separating"?                                                      #
    #                                                                         #
    # Finally, this has to happen for every pair of balls, not just one.      #
    ###########################################################################
      
    # CODE STARTS HERE.
    
    #very honestly, the logic as well as the code running the collision i wrote by hand, but the way to initialise 2 separate balls and 
    # make them both follow the same bit of code i learnt thru ai. it would be very helpful if, before the strat of the next workshop if 
    # we could just learn a bit more about the velocities[0], velocities[1] stuff and why it works that way.

    point_of_contact = []
    vector_of_impact = []

    for i in range(NUM_PARTICLES):
        for j in range(i+1, NUM_PARTICLES):
            distance = np.linalg.norm(positions[i]-positions[j])
            if (distance <= 2*PARTICLE_RADIUS and distance>0):
                point_of_contact = (positions[i]+positions[j])/2
                vector_of_impact = positions[i]-positions[j]
                vector_of_impact_magnitude = np.linalg.norm(vector_of_impact)
                vel_i_impact_magnitude = np.dot(velocities[i], vector_of_impact)/vector_of_impact_magnitude
                vel_i_impact = vector_of_impact * (vel_i_impact_magnitude/vector_of_impact_magnitude)
                vel_i_tangential = velocities[i] - vel_i_impact
                vector_of_impact = vector_of_impact
                vel_j_impact_magnitude = np.dot(velocities[j], vector_of_impact)/vector_of_impact_magnitude
                vel_j_impact = vector_of_impact * (vel_j_impact_magnitude/vector_of_impact_magnitude)
                vel_j_tangential = velocities[j] - vel_j_impact
                velocities[j] = vel_j_tangential + RESTITUTION*vel_i_impact
                velocities[i] = vel_i_tangential + RESTITUTION*vel_j_impact


        

    ###########################################################################
    #                            END OF YOUR CODE                             #
    ###########################################################################

    # Render

    screen.fill((20, 20, 25))

    pygame.draw.circle(
        screen,
        (180, 180, 180),
        BOWL_CENTER.astype(int),
        BOWL_RADIUS,
        width=3
    )

    for position in positions:
        pygame.draw.circle(
            screen,
            (220, 220, 220),
            position.astype(int),
            PARTICLE_RADIUS
        )

    pygame.display.flip()

pygame.quit()
