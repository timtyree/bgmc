#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include "particles.h"

#define N 100
#define L 100.0
#define T 1000
#define V 1.0
#define ALPHA 1.5
#define CUTOFF 10.0

int main(void) {
    Particle particles[N];
    PriorityQueue queue;
    queue.size = 0;
    init_particles(particles);
    for (int i = 0; i < N; i++) {
        add_particle(&queue, particles[i]);
    }
    for (int t = 0; t < T; t++) {
        Particle p1 = pop_particle(&queue);
        update_position(&p1);
        add_particle(&queue, p1);
        for (int i = 0; i < queue.size; i++) {
            Particle p2 = queue.data[i];
            if (distance(p1, p2, L / 10.0)) {
                printf("Particles %d and %d are too close at time step %d!\n", p1.index, p2.index, t);
            }
        }
    }
    return 0;
}
