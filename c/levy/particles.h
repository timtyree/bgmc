#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdbool.h>

#define N 100    // Number of particles
#define L 100.0  // Side length of the square domain
#define T 1000   // Number of time steps
#define V 1.0    // Speed of the particles
#define ALPHA 1.5  // Lévy flight exponent
#define CUTOFF 10.0 // Cutoff distance for interactions
#define PI 3.14159265358979323846

typedef struct {
    double x;
    double y;
} Vec2D;

typedef struct {
    Vec2D pos;
    double step_length;
} Particle;

typedef struct {
    Particle data[N];
    int size;
} PriorityQueue;

void init_particles(Particle particles[N]) {
    for (int i = 0; i < N; i++) {
        particles[i].pos.x = rand() / (double)RAND_MAX * L;
        particles[i].pos.y = rand() / (double)RAND_MAX * L;
        particles[i].step_length = 0.0;
    }
}

double levy() {
    double u = rand() / (double)RAND_MAX;
    double v = rand() / (double)RAND_MAX;
    double r = pow(u, -1.0 / ALPHA);
    double theta = 2.0 * M_PI * v;
    return r * sin(theta);
}

void update_position(Particle *p) {
    double dx = levy();
    double dy = levy();
    double norm = sqrt(dx * dx + dy * dy);
    p->pos.x += V * dx / norm;
    p->pos.y += V * dy / norm;
    p->step_length += sqrt((V * dx) * (V * dx) + (V * dy) * (V * dy));
}

void add_particle(PriorityQueue *q, Particle p) {
    q->data[q->size++] = p;
    int i = q->size - 1;
    while (i > 0 && q->data[i].step_length > q->data[(i - 1) / 2].step_length) {
        Particle temp = q->data[i];
        q->data[i] = q->data[(i - 1) / 2];
        q->data[(i - 1) / 2] = temp;
        i = (i - 1) / 2;
    }
}

Particle pop_particle(PriorityQueue *q) {
    Particle result = q->data[0];
    q->size--;
    if (q->size == 0) {
        return result;
    }
    q->data[0] = q->data[q->size];
    int i = 0;
    while (2 * i + 1 < q->size) {
        int left = 2 * i + 1;
        int right = 2 * i + 2;
        int j = left;
        if (right < q->size && q->data[right].step_length > q->data[left].step_length) {
            j = right;
        }
        if (q->data[i].step_length >= q->data[j].step_length) {
            break;
        }
        Particle temp = q->data[i];
        q->data[i] = q->data[j];
        q->data[j] = temp;
        i = j;
    }
    return result;
}

bool distance(Particle p1, Particle p2, double L) {
  // TODO: extract x1,2,y1,2 from p1,2
  double dx = fabs(x1 - x2);
  double dy = fabs(y1 - y2);
  dx = fmin(dx, L - dx);
  dy = fmin(dy, L - dy);
  return sqrt(dx*dx + dy*dy);
}

double levy_rand(double alpha) {
    double r = (double)rand() / RAND_MAX;
    return pow(r, -1.0/alpha);
}

double rand_angle() {
    return 2 * PI * ((double)rand() / RAND_MAX);
}

double wrap(double x, double L) {
    while (x < 0) {
        x += L;
    }
    while (x >= L) {
        x -= L;
    }
    return x;
}

double reflect(double x, double L) {
    while (x < 0) {
        x = -x;
    }
    while (x >= L) {
        x = 2 * L - x;
    }
    return x;
}
