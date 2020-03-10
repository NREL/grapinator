#!/usr/bin/env bash
cd /opt/mariadb/test_db-master
mysql -uroot -p"f00baZZ123" < employees.sql
echo "Database employeesdb setup complete."
cd sakila
mysql -uroot -p"f00baZZ123" < sakila-mv-schema.sql
mysql -uroot -p"f00baZZ123" < sakila-mv-data.sql
echo "Database sakiladb setup complete."
