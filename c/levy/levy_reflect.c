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

int main() {
    srand(time(NULL));

    int N = 10;
    double L = 10.0;
    int num_steps = 1000;
    double alpha = 1.5;
    double step_size;

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
            x[j] += step_size * cos(angle);
            y[j] += step_size * sin(angle);

            // Reflect particles at boundary of domain
            if (x[j] < 0) {
                x[j] = -x[j];
            } else if (x[j] > L) {
                x[j] = 2 * L - x[j];
            }
            if (y[j] < 0) {
                y[j] = -y[j];
            } else if (y[j] > L) {
                y[j] = 2 * L - y[j];
            }

            printf("%f %f\n", x[j], y[j]);
        }
    }

    return 0;
}
