export REDIS_CONTAINER_NAME="pebg-ecommerce-redis"
export REDIS_PASSWORD="redis"


sudo docker run \
--name $REDIS_CONTAINER_NAME \
-p 38379:6379 \
-d redis --appendonly yes --requirepass $REDIS_PASSWORD