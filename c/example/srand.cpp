#include <stdlib.h>

std::random_device r;
std::seed_seq seed{r(), r(), r(), r(), r(), r(), r(), r()};
std::mt19937 eng(seed);
int answerPositionArray[8];
std::shuffle(0, 9999, eng);

// std::shuffle(std::begin(answerPositionArray), std::end(answerPositionArray), eng);
