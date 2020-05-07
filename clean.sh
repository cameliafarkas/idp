docker rmi $(docker images --filter "dangling=true" -q --no-trunc)
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker-compose down -v
docker system prune 
