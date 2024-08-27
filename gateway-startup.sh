#!/bin/sh

KONG_ADMIN_URL="http://localhost:8001"

# Wait for Kong to be ready
until $(curl --output /dev/null --silent --head --fail $KONG_ADMIN_URL); do
  printf '.'
  sleep 5
done

# Register product_service
curl -i -X POST $KONG_ADMIN_URL/services/ \
  --data "name=product_service" \
  --data "url=http://host.docker.internal:8085"

# Register product_service route
curl -i -X POST $KONG_ADMIN_URL/services/product_service/routes \
  --data "paths[]=/product_service" \
  --data "strip_path=true"

# Register inventory_service
curl -i -X POST $KONG_ADMIN_URL/services/ \
  --data "name=inventory_service" \
  --data "url=http://host.docker.internal:8086"

# Register inventory_service route
curl -i -X POST $KONG_ADMIN_URL/services/inventory_service/routes \
  --data "paths[]=/inventory_service" \
  --data "strip_path=true"

# Register order_service
curl -i -X POST $KONG_ADMIN_URL/services/ \
  --data "name=order_service" \
  --data "url=http://host.docker.internal:8087"

# Register order_service route
curl -i -X POST $KONG_ADMIN_URL/services/order_service/routes \
  --data "paths[]=/order_service" \
  --data "strip_path=true"

# Register user_service
curl -i -X POST $KONG_ADMIN_URL/services/ \
  --data "name=user_service" \
  --data "url=http://host.docker.internal:8088"

# Register user_service route
curl -i -X POST $KONG_ADMIN_URL/services/user_service/routes \
  --data "paths[]=/user_service" \
  --data "strip_path=true"

# Register notification_service
curl -i -X POST $KONG_ADMIN_URL/services/ \
  --data "name=notification_service" \
  --data "url=http://host.docker.internal:8089"

# Register notification_service route
curl -i -X POST $KONG_ADMIN_URL/services/notification_service/routes \
  --data "paths[]=/notification_service" \
  --data "strip_path=true"

# Register payment_service
curl -i -X POST $KONG_ADMIN_URL/services/ \
  --data "name=payment_service" \
  --data "url=http://host.docker.internal:8090"

# Register payment_service route
curl -i -X POST $KONG_ADMIN_URL/services/payment_service/routes \
  --data "paths[]=/payment_service" \
  --data "strip_path=true"
