# spyfaux
This is very easy spyfaux implementation. The project only allows create room, returns location and role

## installation
pip3 install flask  
pip3 install gevent  

## API calls
create room  
curl -X post localhost:5000/room_create  
  
check room    
curl --header "Content-Type: application/json" \  
 --data '{"room_no":"167639"}' \  
 localhost:5000/room_check  
  
join room  
curl --header "Content-Type: application/json" \  
 --data '{"room_no":"167639"}' \  
 localhost:5000/room_join  
  
stop room to accept new players  
curl --header "Content-Type: application/json" \  
 --data '{"room_no":"167639","pass":"47"}' \  
 localhost:5000/room_stop  
