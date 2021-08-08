N=20
FN='tmp.input'
clear
cd ..
./gcc.sh
cd dev
date
echo "/* Testing Effect of Adding a 1cm Basin of Attraction between (i) nearest neighbors and (ii) vector summed forces. */\n"

echo """Key Results made repeatable here:
  1. when using reflective boundary conditions, a small constant repulsive force decreased the annihilation rate independent of whether or not forces were only considered if they were between nearest neighbors.
  2. if periodic boundary conditions were used, however, a small constant repulsive force _increased_ the annihilation rate if the forces were considered as a vector sum between all particles.

This same result emerged independent of 1/r forces or 1/r^2 forces being used.
"""

#Note: setting second particle within range of the first particle did not change the relation between Case 1 and Case 2
# echo '0.1 2 5 15000 20 1 1e-05 1e-05 10 50 1234 0 1 0 0 1 2' > $FN
echo "\n/* * * turning on periodic boundary conditions and inverse power law forces * * */\n"

echo "/***Case 1: nearest neighbor summed forces***/"
echo "Printing the mean time to first reaction (seconds) before/after adding a constant repulsive force for a 1cm basin of attraction..."
echo 0.1 2 5 15000 20 1 1e-05 1e-05 10 ${N} 1234 0 0 0 0 1 2 > $FN
./../return_CollTime.x < $FN | grep "Tavg"
echo 0.1 2 5 15000 20 1 1e-05 1e-05 10 ${N} 1234 0 0 0 0 1 4 > $FN
./../return_CollTime.x < $FN | grep "Tavg"
echo "If Tavg got lower, then the rate of collision was _increased_ by a constant repulsive force.\n"

echo "/***Case 2: vector summed forces***/"
echo "Printing the mean time to first reaction (seconds) before/after adding a constant repulsive force for a 1cm basin of attraction..."
FN='tmp.input'
echo 0.1 2 5 15000 20 1 1e-05 1e-05 10 ${N} 1234 0 0 0 0 0 2 > $FN
./../return_CollTime.x < $FN | grep "Tavg"
echo 0.1 2 5 15000 20 1 1e-05 1e-05 10 ${N} 1234 0 0 0 0 0 4 > $FN
./../return_CollTime.x < $FN | grep "Tavg"
echo "If Tavg got higher, then the rate of collision was decreased by a constant repulsive force.\n"

echo "\n/* * * turning on inverse squared power law forces * * */\n"

echo "/***Case 3: nearest neighbor summed forces with inverse square powerlaw attraction***/"
echo "Printing the mean time to first reaction (seconds) before/after adding a constant repulsive force for a 1cm basin of attraction..."
echo 0.1 2 5 15000 20 1 1e-05 1e-05 10 ${N} 1234 1 0 0 0 1 3 > $FN
./../return_CollTime.x < $FN | grep "Tavg"
echo 0.1 2 5 15000 20 1 1e-05 1e-05 10 ${N} 1234 1 0 0 0 1 5 > $FN
./../return_CollTime.x < $FN | grep "Tavg"
echo "If Tavg got lower, then the rate of collision was _increased_ by a constant repulsive force.\n"

echo "/***Case 4: vector summed forces with inverse square powerlaw attraction***/"
echo "Printing the mean time to first reaction (seconds) before/after adding a constant repulsive force for a 1cm basin of attraction..."
FN='tmp.input'
echo 0.1 2 5 15000 20 1 1e-05 1e-05 10 ${N} 1234 1 0 0 0 0 3 > $FN
./../return_CollTime.x < $FN | grep "Tavg"
echo 0.1 2 5 15000 20 1 1e-05 1e-05 10 ${N} 1234 1 0 0 0 0 5 > $FN
./../return_CollTime.x < $FN | grep "Tavg"
echo "If Tavg got higher, then the rate of collision was decreased by a constant repulsive force.\n"

echo "\n/* * * turning on reflecing boundary conditions and inverse power law forces * * */\n"

echo "/***Case 5: nearest neighbor summed forces***/"
echo "Printing the mean time to first reaction (seconds) before/after adding a constant repulsive force for a 1cm basin of attraction..."
echo 0.1 2 5 15000 20 1 1e-05 1e-05 10 ${N} 1234 1 0 0 0 1 2 > $FN
./../return_CollTime.x < $FN | grep "Tavg"
echo 0.1 2 5 15000 20 1 1e-05 1e-05 10 ${N} 1234 1 0 0 0 1 4 > $FN
./../return_CollTime.x < $FN | grep "Tavg"
echo "If Tavg got higher, then the rate of collision was decreased by a constant repulsive force.\n"

echo "/***Case 6: vector summed forces***/"
echo "Printing the mean time to first reaction (seconds) before/after adding a constant repulsive force for a 1cm basin of attraction..."
FN='tmp.input'
echo 0.1 2 5 15000 20 1 1e-05 1e-05 10 ${N} 1234 1 0 0 0 0 2 > $FN
./../return_CollTime.x < $FN | grep "Tavg"
echo 0.1 2 5 15000 20 1 1e-05 1e-05 10 ${N} 1234 1 0 0 0 0 4 > $FN
./../return_CollTime.x < $FN | grep "Tavg"
echo "If Tavg got higher, then the rate of collision was decreased by a constant repulsive force.\n"

echo "\n/* * * turning on inverse squared power law forces * * */\n"

echo "/***Case 7: nearest neighbor summed forces with inverse square powerlaw attraction***/"
echo "Printing the mean time to first reaction (seconds) before/after adding a constant repulsive force for a 1cm basin of attraction..."
echo '0.1 2 5 15000 20 1 1e-05 1e-05 10 ${N} 1234 1 0 0 0 1 3' > $FN
./../return_CollTime.x < $FN | grep "Tavg"
echo '0.1 2 5 15000 20 1 1e-05 1e-05 10 ${N} 1234 1 0 0 0 1 5' > $FN
./../return_CollTime.x < $FN | grep "Tavg"
echo "If Tavg got higher, then the rate of collision was decreased by a constant repulsive force.\n"

echo "/***Case 8: vector summed forces with inverse square powerlaw attraction***/"
echo "Printing the mean time to first reaction (seconds) before/after adding a constant repulsive force for a 1cm basin of attraction..."
FN='tmp.input'
echo '0.1 2 5 15000 20 1 1e-05 1e-05 10 ${N} 1234 1 0 0 0 0 3' > $FN
./../return_CollTime.x < $FN | grep "Tavg"
echo '0.1 2 5 15000 20 1 1e-05 1e-05 10 ${N} 1234 1 0 0 0 0 5' > $FN
./../return_CollTime.x < $FN | grep "Tavg"
echo "If Tavg got higher, then the rate of collision was decreased by a constant repulsive force.\n"
date
