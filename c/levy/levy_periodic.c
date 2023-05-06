#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

#define PI 3.14159265358979323846

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

double distance(double x1, double y1, double x2, double y2, double L) {
    double dx = fabs(x1 - x2);
    double dy = fabs(y1 - y2);
    dx = fmin(dx, L - dx);
    dy = fmin(dy, L - dy);
    return sqrt(dx*dx + dy*dy);
}

int main() {
    srand(time(NULL));

    int N = 10;
    double L = 10.0;
    int num_steps = 1000;
    double alpha = 1.5;
    double step_size;
    double r = L / 10;

    // Initialize particle positions uniformly on square domain
    double x[N], y[N];
    for (int i = 0; i < N; i++) {
        x[i] = L * ((double)rand() / RAND_MAX);
        y[i] = L * ((double)rand() / RAND_MAX);
    }

    // Perform Lévy walk for each particle
    for (int i = 0; i < num_steps; i++) {
        for (int j = 0; j < N; j++) {
            step_size = levy_rand(alpha);
            double angle = rand_angle();
            x[j] = wrap(x[j] + step_size * cos(angle), L);
            y[j] = wrap(y[j] + step_size * sin(angle), L);

            for (int k = 0; k < j; k++) {
                if (distance(x[j], y[j], x[k], y[k], L) < r) {
                    printf("Particles %d and %d are too close!\n", j, k);
                }
            }

            printf("%f %f\n", x[j], y[j]);
        }
    }

    return 0;
}
