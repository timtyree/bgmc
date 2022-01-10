clear
date
###########################################################################################################
# Testing Effect of Location of (Anti)Hookean On Mean Collision Time
###########################################################################################################
echo "/* Testing Effect of Location of (Anti)Hookean On Mean Collision Time */"
echo "/* If Tavg got larger/smaller, then the rate of collision was decreased/increased. */\n"
echo "/* | -------- | */ "
echo "/* | CONTROLS | */ "
echo "/* | -------- | */ "
echo "*Let spring constant be zero, varkappa=0."
echo "Printing the mean time to first reaction (in seconds) for nondeterministic forces only (control) for ntips=8 and ntips=16."
FN='1-control.input'
./../../return_CollTime.x < $FN | grep "Tavg"
FN='2-control.input'
./../../return_CollTime.x < $FN | grep "Tavg"

echo "/* | -------- | */ "
echo "/* |  TESTS   | */ "
echo "/* | -------- | */ "
echo "*Let spring constant be positive, varkappa>0."
echo "**Let preferred distance equal zero, x0=0."
echo "Printing the mean time to first reaction (in seconds) with  for ntips=8 and ntips=16."
FN='1-test.input'
./../../return_CollTime.x < $FN | grep "Tavg"
FN='2-test.input'
./../../return_CollTime.x < $FN | grep "Tavg"

echo "**Let preferred distance be positive, x0=0.2."
echo "Printing the mean time to first reaction (in seconds) with  for ntips=8 and ntips=16."
FN='3-test.input'
./../../return_CollTime.x < $FN | grep "Tavg"
FN='4-test.input'
./../../return_CollTime.x < $FN | grep "Tavg"

echo "**Let preferred distance be positive, x0=0.5."
echo "Printing the mean time to first reaction (in seconds) with  for ntips=8 and ntips=16."
FN='5-test.input'
./../../return_CollTime.x < $FN | grep "Tavg"
FN='6-test.input'
./../../return_CollTime.x < $FN | grep "Tavg"

echo "\nLet spring constant be negative, varkappa<0."
echo "**Let preferred distance equal zero, x0=0."
echo "Printing the mean time to first reaction (in seconds) with  for ntips=8 and ntips=16."
FN='7-test.input'
./../../return_CollTime.x < $FN | grep "Tavg"
FN='8-test.input'
./../../return_CollTime.x < $FN | grep "Tavg"

echo "**Let preferred distance be positive, x0=0.2."
echo "Printing the mean time to first reaction (in seconds) with  for ntips=8 and ntips=16."
FN='9-test.input'
./../../return_CollTime.x < $FN | grep "Tavg"
FN='10-test.input'
./../../return_CollTime.x < $FN | grep "Tavg"

echo "**Let preferred distance be positive, x0=0.5."
echo "Printing the mean time to first reaction (in seconds) with  for ntips=8 and ntips=16."
FN='11-test.input'
./../../return_CollTime.x < $FN | grep "Tavg"
FN='12-test.input'
./../../return_CollTime.x < $FN | grep "Tavg"

###########################################################################################################
# Archive
###########################################################################################################
# echo "If Tavg got smaller, then the rate of collision was decreased by a small repulsive force."
# echo "^this last result is suprising. Nota bene: only nearest neighbor interactions are being used here."
date
