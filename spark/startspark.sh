#!/bin/sh

SPARK_PORT_FORWARDING_CHECK="port-forward --namespace spark"
SPARK_PORT_FORWARDING_CHECK_SHORTNAME="port-forward -n spark"

if ! pgrep -f "$SPARK_PORT_FORWARDING_CHECK" > /dev/null && ! pgrep -f "$SPARK_PORT_FORWARDING_CHECK_SHORTNAME" > /dev/null; then
    echo "Starting port-forwarding for spark"
    nohup kubectl port-forward -n spark svc/spark-chart-master-svc 8083:80 --address 0.0.0.0 > /home/ubuntu/kubernetes/spark/port-forward.log 2>&1 &\
	    PORT_FORWARD_PID=$!
    sleep 5
fi
echo "PORTFORWARD PID: $PORT_FORWARD_PID"
echo "spark master's port : 8083"
