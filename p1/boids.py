import pygame
import sys
import random
import math

from pygame.locals import *

WIDTH = 1280
HEIGHT = 800
NEIGHBOR_RADIUS = 60
MAX_SPEED = 12
BOID_COUNT = 200
OBSTACLE_RADIUS = 20


# Weights
SEP_WEIGHT = 70
ALIGN_WEIGHT = 35
COH_WEIGHT = 20


def random_initial_velocity():
    return [random.uniform(-1, 1)*MAX_SPEED, random.uniform(-1,1)*MAX_SPEED]


class Boid(object):

    def __init__(self, x, y, angle, image_path):
        self.angle = angle
        self.position = [x, y]
        self.velocity = random_initial_velocity()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.surface = pygame.Surface((15,11), flags=pygame.SRCALPHA)
        self.surface.set_alpha(0)
        self.pos_rect = pygame.Rect((0,0,1,1))
        self.surface.blit(self.image, self.pos_rect)

    def draw(self):
        render_angle = -(self.angle+90)
        render_surface = pygame.transform.rotozoom(self.surface, render_angle, 1.0)
        rot_rect = render_surface.get_rect(center=(self.position[0], self.position[1]))
        screen.blit(render_surface, rot_rect)

    def update(self, neighbors, near_obstacle, near_predators):
        separation_force = self._separate(neighbors)
        alignment_force = self._align(neighbors)
        cohesion_force = self._cohesion(neighbors)
        #if near_obstacle and near_obstacle.within(self.position[0], self.position[1]):
        if near_obstacle:
            avoid_obstacles = [-self.velocity[1], self.velocity[0]]
        else:
            avoid_obstacles = [.0, .0]
        if near_predators:
            avoid_predators = self._separate(near_predators)
        else:
            avoid_predators = [.0, .0]

        # Update velocity
        self.velocity[0] += (separation_force[0] * SEP_WEIGHT) + \
                (alignment_force[0] * ALIGN_WEIGHT) + \
                (cohesion_force[0] * COH_WEIGHT) + \
                (avoid_obstacles[0] * 500) + \
                (avoid_predators[0] * 500)
        self.velocity[1] += (separation_force[1] * SEP_WEIGHT) + \
                (alignment_force[1] * ALIGN_WEIGHT) + \
                (cohesion_force[1] * COH_WEIGHT) + \
                (avoid_obstacles[1] * 500) + \
                (avoid_predators[1] * 500)

        if abs(self.velocity[0]) > MAX_SPEED or abs(self.velocity[1]) > MAX_SPEED:
            # Clamp velocity
            max_dir = max(abs(self.velocity[0]), abs(self.velocity[1]))
            self.velocity[0] = (self.velocity[0] / max_dir) * MAX_SPEED
            self.velocity[1] = (self.velocity[1] / max_dir) * MAX_SPEED
        # Update angle and position
        self.angle = math.degrees(math.atan2(self.velocity[1], self.velocity[0])) % 360
        self.position[0] = (self.position[0] + self.velocity[0]) % WIDTH
        self.position[1] = (self.position[1] + self.velocity[1]) % HEIGHT

    def _separate(self, neighbors):
        force = [.0, .0]
        for neighbor, distance in neighbors:
            if distance == 0 and isinstance(neighbor, Boid):
                force[0] -= neighbor.velocity[0]
                force[1] -= neighbor.velocity[1]
            else:
                force[0] -= (neighbor.position[0] - self.position[0]) / distance
                force[1] -= (neighbor.position[1] - self.position[1]) / distance
        return force

    def _align(self, neighbors):
        if len(neighbors) == 0:
            return self.velocity
        avg_x = sum([neighbor[0].velocity[0] for neighbor in neighbors]) / len(neighbors)
        avg_y = sum([neighbor[0].velocity[1] for neighbor in neighbors]) / len(neighbors)
        return [avg_x, avg_y]

    def _cohesion(self, neighbors):
        if len(neighbors) == 0:
            return self.position
        avg_x = sum([neighbor[0].position[0] for neighbor in neighbors]) / len(neighbors)
        avg_y = sum([neighbor[0].position[1] for neighbor in neighbors]) / len(neighbors)
        return [avg_x - self.position[0], avg_y - self.position[1]] 



class Predator(Boid):

    def __init__(self, x, y, angle, image_path, neighbor_radius):
        super(self.__class__, self).__init__(x, y, angle, image_path)
        self.neighbor_radius = neighbor_radius

    def update(self):
        near_boids = []
        for boid in flock:
            distance = math.hypot(boid.position[0] - self.position[0], boid.position[1] - self.position[1])
            if distance < self.neighbor_radius * 2:
                near_boids.append((boid, distance))

        obstacles = []
        for obstacle in obstacles:
            distance = math.hypot(obstacle.position[0] - self.position[0], obstacle.position[1] - self.position[1])
            if distance < (OBSTACLE_RADIUS * 3):
                obstacles.append((obstacle, distance))


        if near_boids:
            align_with_boids = self._align(near_boids)
            cohesion_force = self._cohesion(near_boids)
        else:
            align_with_boids = [.0, .0]
            cohesion_force = [.0, .0]

        if obstacles:
            avoid_obstacles = [-self.velocity[1], self.velocity[0]]
        else:
            avoid_obstacles = [.0, .0]

        # Update velocity
        self.velocity[0] += (align_with_boids[0] * ALIGN_WEIGHT) + \
                (cohesion_force[0] * COH_WEIGHT) + \
                (avoid_obstacles[0] * 300)
        self.velocity[1] += (align_with_boids[1] * ALIGN_WEIGHT) + \
                (cohesion_force[1] * COH_WEIGHT) + \
                (avoid_obstacles[1] * 300)

        # Clamp velocity
        max_dir = max(abs(self.velocity[0]), abs(self.velocity[1]))
        self.velocity[0] = (self.velocity[0] / max_dir) * (MAX_SPEED - 1)
        self.velocity[1] = (self.velocity[1] / max_dir) * (MAX_SPEED - 1)


        self.angle = math.degrees(math.atan2(self.velocity[1], self.velocity[0])) % 360
        self.position[0] = (self.position[0] + self.velocity[0]) % WIDTH
        self.position[1] = (self.position[1] + self.velocity[1]) % HEIGHT


class Flock:

    def __init__(self, init_num, neighbor_distance):
        self.neighbor_distance = neighbor_distance
        self.boids = []
        for i in range(init_num):
            self.boids.append(Boid(random.randint(0,WIDTH), random.randint(0, HEIGHT), random.randint(0,360), 'assets/boid.png'))

    def __iter__(self):
        for boid in self.boids:
            yield boid

    def add_boid(self):
        self.boids.append(Boid(random.randint(0,WIDTH), random.randint(0, HEIGHT), random.randint(0,360), 'assets/boid.png'))

    def draw(self):
        for boid in self.boids:
            boid.draw()

    def update(self):
        for boid in list(self.boids):
            neighbors = []
            near_obstacle = None
            near_predators = []
            for obstacle in obstacles:
                #distance = math.hypot(obstacle.position[0] - boid.position[0], obstacle.position[1] - boid.position[1])
                #if distance < (OBSTACLE_RADIUS * 3):
                #    near_obstacles.append((obstacle, distance))
                if obstacle.within(boid.position[0], boid.position[1]):
                    near_obstacle = obstacle
                    break
            for other_boid in self.boids:
                if other_boid == boid:
                    continue
                distance = math.hypot(other_boid.position[0] - boid.position[0], other_boid.position[1] - boid.position[1])
                if distance < self.neighbor_distance:
                    neighbors.append((other_boid, distance))
            for predator in predators:
                distance = math.hypot(predator.position[0] - boid.position[0], predator.position[1] - boid.position[1])
                if distance < self.neighbor_distance:
                    near_predators.append((predator, distance))
            boid.update(neighbors, near_obstacle, near_predators)

class Obstacle:
    def __init__(self, x, y, radius):
        self.position = [x, y]
        self.radius = radius

    def draw(self):
        pygame.draw.circle(screen, (0, 0, 0), tuple(self.position), self.radius, 0)

    def within(self, x, y):
        """
        Returns True if the point (x, y) is inside the obstacle
        """
        return ((x - self.position[0]) ** 2 + (y - self.position[1]) ** 2) < self.radius ** 2


pygame.init()
fpsClock = pygame.time.Clock()

size = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Boids are cool")

flock = Flock(BOID_COUNT, NEIGHBOR_RADIUS)
obstacles = []
predators = []

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))
            elif event.key == K_PLUS:
                flock.add_boid()
            elif event.key == K_q:
                SEP_WEIGHT = (SEP_WEIGHT + 1) if SEP_WEIGHT < 100 else SEP_WEIGHT
            elif event.key == K_a:
                SEP_WEIGHT = (SEP_WEIGHT -1) if SEP_WEIGHT > 0 else SEP_WEIGHT
            elif event.key == K_w:
                ALIGN_WEIGHT = (ALIGN_WEIGHT + 1) if ALIGN_WEIGHT < 100 else ALIGN_WEIGHT
            elif event.key == K_s:
                ALIGN_WEIGHT = (ALIGN_WEIGHT - 1) if ALIGN_WEIGHT > 0 else ALIGN_WEIGHT
            elif event.key == K_e:
                COH_WEIGHT = (COH_WEIGHT + 1) if COH_WEIGHT < 100 else COH_WEIGHT
            elif event.key == K_d:
                COH_WEIGHT = (COH_WEIGHT -1) if COH_WEIGHT > 0 else COH_WEIGHT
            elif event.key == K_MINUS:
                try:
                    predators.pop()
                except: pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for obstacle in obstacles:
                    if obstacle.within(event.pos[0], event.pos[1]):
                        obstacles.remove(obstacle)
                        break
                else:
                    obstacles.append(Obstacle(event.pos[0], event.pos[1], OBSTACLE_RADIUS))
            elif event.button == 3:
                predators.append(Predator(event.pos[0], event.pos[1], random.randint(0, 360), 'assets/predator.png', NEIGHBOR_RADIUS))

    screen.fill((255, 255, 255))
    flock.update()
    flock.draw()
    for predator in predators:
        predator.update()
        predator.draw()

    for obstacle in obstacles:
        obstacle.draw()
    pygame.display.flip()
