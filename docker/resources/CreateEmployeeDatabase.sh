#!/usr/bin/env bash
cd /opt/employees_db/test_db-master
mysql -uroot -p"f00baZZ123" < employees.sql
echo "Database employeesdb setup complete."