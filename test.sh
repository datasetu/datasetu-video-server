cd root/datasetu-video-server/storage/live
x=$PWD
str=$1
delimiter=%2F
s=$str$delimiter
array=();
while [[ $s ]]; do
    array+=( "${s%%"$delimiter"*}" );
    s=${s#*"$delimiter"};
done;
declare -p array

for element in "${array[@]}"
do
  mkdir "${element}"
  cd "${element}"
done
x="${x}/$1"
cd ..
rm -rf ${array[-1]}
y=$PWD
y="${y}/${array[-1]}"
ln -s ${x} ${y}
