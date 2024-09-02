nohup kubectl port-forward --address=0.0.0.0 svc/airflow-webserver 8080:8080 -n airflow > port-forward.log 2>&1 &

