#!/bin/sh
DASHBOARD_PORT_FORWARDING="10443:443"
DASHBOARD_PROXY="kubectl proxy"

if ! pgrep -f "$DASHBOARD_PORT_FORWARDING" > /dev/null; then
    echo "Starting port-forwarding for dashboard"
    nohup kubectl port-forward -n kubernetes-dashboard service/kubernetes-dashboard-kong-proxy 10443:443 --address 0.0.0.0 > /home/ubuntu/kubernetes/dashboard/port-forward.log 2>&1 & \
    PORT_FORWARD_PID=$!

    sleep 5
fi

if ! pgrep -f "$DASHBOARD_PROXY" > /dev/null; then
    echo "Starting proxy"
    nohup kubectl proxy > /home/ubuntu/kubernetes/dashboard/proxy.log 2>&1 & PROXY_PID=$!
fi

echo "Applying admin user"

kubectl apply -f /home/ubuntu/kubernetes/dashboard/dashboard-adminuser.yaml

echo "Creating token for admin user"
TOKEN=$(kubectl get secret admin-user -n kubernetes-dashboard -o jsonpath={".data.token"} | base64 -d)

echo "PORTFORWARD PID: $PORT_FORWARD_PID"
echo "PROXY_PID: $PROXY_PID"
echo "token:"
echo "$TOKEN">/home/ubuntu/kubernetes/dashboard/token
cat /home/ubuntu/kubernetes/dashboard/token
