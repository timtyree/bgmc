clear
date
echo "/* Testing Effect of Strong/Weak Forces with inverse power law forces between nearest neighbors. */\n"
echo "Printing the mean time to first reaction (seconds) before/after turning on a large attractive force..."
FN='4-control.input'
./../../return_CollTime.x < $FN | grep "Tavg"
FN='4-test.input'
./../../return_CollTime.x < $FN | grep "Tavg"
echo "If Tavg got smaller, then the rate of collision was increased by a large attractive force.\n"

echo "Printing the mean time to first reaction (seconds) before/after turning on a large repulsive force..."
FN='2-control.input'
./../../return_CollTime.x < $FN | grep "Tavg"
FN='2-test.input'
./../../return_CollTime.x < $FN | grep "Tavg"
echo "If Tavg got larger, then the rate of collision was decreased by a large repulsive force.\n"

echo "Printing the mean time to first reaction (seconds) before/after turning on a small attractive force..."
FN='1-control.input'
./../../return_CollTime.x < $FN | grep "Tavg"
FN='1-test.input'
./../../return_CollTime.x < $FN | grep "Tavg"
echo "If Tavg got smaller, then the rate of collision was increased by a small attractive force.\n"

echo "Printing the mean time to first reaction (seconds) before/after turning on a small repulsive force..."
FN='3-control.input'
./../../return_CollTime.x < $FN | grep "Tavg"
FN='3-test.input'
./../../return_CollTime.x < $FN | grep "Tavg"
echo "If Tavg got larger, then the rate of collision was decreased by a small repulsive force."
# echo "If Tavg got smaller, then the rate of collision was decreased by a small repulsive force."
# echo "^this last result is suprising. Nota bene: only nearest neighbor interactions are being used here."
date
