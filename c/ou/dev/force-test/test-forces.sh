clear
date
echo "/* Testing Effect of Attractive/Repulsive Force On Mean Collision Time */\n"
echo "Printing the mean time to first reaction (seconds) before/after turning on a large attractive force..."
FN='4-control.input'
./../../return_CollTime.x < $FN | grep "Tavg"
FN='4-test.input'
./../../return_CollTime.x < $FN | grep "Tavg"
echo "If Tavg got smaller, then the rate of collision was increased by a large attractive force.\n"

echo "Testing the effect of turning on large repulsive force..."
FN='2-control.input'
./../../return_CollTime.x < $FN | grep "Tavg"
FN='2-test.input'
./../../return_CollTime.x < $FN | grep "Tavg"
echo "If Tavg got larger, then the rate of collision was decreased by a large repulsive force."

echo "Printing the mean time to first reaction (seconds) before/after turning on a small attractive force..."
FN='1-control.input'
./../../return_CollTime.x < $FN | grep "Tavg"
FN='1-test.input'
./../../return_CollTime.x < $FN | grep "Tavg"
echo "If Tavg got smaller, then the rate of collision was increased by a small attractive force.\n"

echo "Testing the effect of turning on small repulsive forces..."
FN='3-control.input'
./../../return_CollTime.x < $FN | grep "Tavg"
FN='3-test.input'
./../../return_CollTime.x < $FN | grep "Tavg"
echo "If Tavg got larger, then the rate of collision was decreased by a small repulsive force."
# echo "If Tavg got smaller, then the rate of collision was decreased by a small repulsive force."
# echo "^this last result is suprising. Nota bene: only nearest neighbor interactions are being used here."
date
