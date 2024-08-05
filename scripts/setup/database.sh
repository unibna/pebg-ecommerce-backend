# docker required
export DB_CONTAINER_NAME='pegb-ecommerce-postgresql'
export DB_NAME='pegb'
export DB_USER='pegb'
export DB_PASSWORD='pegb'

sudo docker run \
--platform=linux/amd64 \
--name $DB_CONTAINER_NAME \
-p 38432:5432 \
-e POSTGRES_PASSWORD=$DB_PASSWORD \
-e POSTGRES_DB=$DB_NAME \
-e POSTGRES_USER=$DB_USER \
-d postgres