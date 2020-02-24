# Documentation for grapinator schema

## Introduction
The schema you define for this code is the core of the program's operation.  This is where you define the database tables, primary keys, dynamically created SQLAlchemy classes, table relationships, and all the associated Graphene definitions for your specific needs.  From this file, grapinator is able to dynamically generate at runtime a fully functional GraphQL query service.

Since the code is in an alpha state, I am just going to describe the current configuration.  Please assume that this may change over time as the code matures.

### Dictionary definition
In simple terms the grapinator schema is a list of Python dictionaries.  Each dictionary within the list contains all the elements that define a specific table to graph, including further lists of dictionaries that define each column you wish to expose from the database and their relationships to other tables.

### Dictionary elements
- **GQL_CLASS_NAME:** The name of the class for GraphQL
- **GQL_CONN_CLASS_NAME:** The name of the GraphQL connection class
- **GQL_CONN_QUERY_NAME:** The name to use within a query
- **GQL_CONN_QUERY_NAME:** The name of the SQLAlchemy model class
- **DB_TABLE_NAME:** The name of the table in the database
- **DB_TABLE_PK:** The column name of the primary key used by the database
- **DB_DEFAULT_SORT_COL:** Default sort column
- **FIELDS:** List of dictionaries defining each column to expose
    - **gql_col_name:** GraphQL column name
    - **gql_type:** Graphene type
    - **gql_description:** Description string for the GraphiQL web browser
    - **db_col_name:** Database column name.  
    - **db_type:** SQLAlchemy database type
- **RELATIONSHIPS:** List of dictionaries containing SQLAlchemy class model [relationships](https://docs.sqlalchemy.org/en/13/orm/relationship_api.html#sqlalchemy.orm.relationship)
    - **rel_name:** SQLAlchemy relationship name
    - **rel_class_name:** SQLAlchemy model class name
    - **rel_arguments:** Dictionary of elements to pass to database class constructor
        - **foreign_keys:** Foreign keys in this relationship
        - **primaryjoin:** SQLAlchemy join

### Included example schema for the MySQL Employee Sample Database

```
[
    {
        'GQL_CLASS_NAME': 'Departments'
        ,'GQL_CONN_CLASS_NAME': 'DepartmentsConnection'
        ,'GQL_CONN_QUERY_NAME': 'departments'
        ,'DB_CLASS_NAME': 'db_Departments'
        ,'DB_TABLE_NAME': 'departments'
        ,'DB_TABLE_PK': 'dept_no'
        ,'DB_DEFAULT_SORT_COL': 'dept_no'
        ,'FIELDS': [
            {
                'gql_col_name': 'department_number'
                ,'gql_type': graphene.String
                ,'gql_description': 'Department number (PK).'
                ,'db_col_name': 'dept_no'
                ,'db_type': String
            },
            {
                'gql_col_name': 'department_name'
                ,'gql_type': graphene.String
                ,'gql_description': 'Department name.'
                ,'db_col_name': 'dept_name'
                ,'db_type': String
            },
        ]
        ,'RELATIONSHIPS': []
    },
    {
        'GQL_CLASS_NAME': 'DeptEmp'
        ,'GQL_CONN_CLASS_NAME': 'DeptEmpConnection'
        ,'GQL_CONN_QUERY_NAME': 'employee_department'
        ,'DB_CLASS_NAME': 'db_DeptEmp'
        ,'DB_TABLE_NAME': 'dept_emp'
        ,'DB_TABLE_PK': 'emp_no'
        ,'DB_DEFAULT_SORT_COL': 'emp_no'
        ,'FIELDS': [
            {
                'gql_col_name': 'employee_number'
                ,'gql_type': graphene.String
                ,'gql_description': 'Employee number (PK).'
                ,'db_col_name': 'emp_no'
                ,'db_type': Integer
            },
            {
                'gql_col_name': 'department_number'
                ,'gql_type': graphene.String
                ,'gql_description': 'Department number.'
                ,'db_col_name': 'dept_no'
                ,'db_type': String
            },
            {
                'gql_col_name': 'from_date'
                ,'gql_type': graphene.String
                ,'gql_description': 'Start date of department service.'
                ,'db_col_name': 'from_date'
                ,'db_type': Date
            },
            {
                'gql_col_name': 'to_date'
                ,'gql_type': graphene.String
                ,'gql_description': 'End date of department service.'
                ,'db_col_name': 'to_date'
                ,'db_type': Date
            },
        ]
        ,'RELATIONSHIPS': [
            {
                'rel_name': 'employee'
                ,'rel_class_name': 'db_Employees'
                ,'rel_arguments': {
                    'foreign_keys': 'db_DeptEmp.employee_number'
                    ,'primaryjoin': 'remote(db_Employees.employee_number) == foreign(db_DeptEmp.employee_number)'
                }
            },
            {
                'rel_name': 'department'
                ,'rel_class_name': 'db_Departments'
                ,'rel_arguments': {
                    'foreign_keys': 'db_DeptEmp.employee_number'
                    ,'primaryjoin': 'remote(db_Departments.department_number) == foreign(db_DeptEmp.department_number)'
                }
            },
        ]
    },
    {
        'GQL_CLASS_NAME': 'DeptManager'
        ,'GQL_CONN_CLASS_NAME': 'DeptManagerConnection'
        ,'GQL_CONN_QUERY_NAME': 'department_managers'
        ,'DB_CLASS_NAME': 'db_DeptManager'
        ,'DB_TABLE_NAME': 'dept_manager'
        ,'DB_TABLE_PK': 'emp_no'
        ,'DB_DEFAULT_SORT_COL': 'emp_no'
        ,'FIELDS': [
            {
                'gql_col_name': 'employee_number'
                ,'gql_type': graphene.String
                ,'gql_description': 'Employee number (PK).'
                ,'db_col_name': 'emp_no'
                ,'db_type': Integer
            },
            {
                'gql_col_name': 'department_number'
                ,'gql_type': graphene.String
                ,'gql_description': 'Department number.'
                ,'db_col_name': 'dept_no'
                ,'db_type': String
            },
            {
                'gql_col_name': 'from_date'
                ,'gql_type': graphene.String
                ,'gql_description': 'Start date of department manager service.'
                ,'db_col_name': 'from_date'
                ,'db_type': Date
            },
            {
                'gql_col_name': 'to_date'
                ,'gql_type': graphene.String
                ,'gql_description': 'End date of department manager service.'
                ,'db_col_name': 'to_date'
                ,'db_type': Date
            },
        ]
        ,'RELATIONSHIPS': [
            {
                'rel_name': 'employee'
                ,'rel_class_name': 'db_Employees'
                ,'rel_arguments': {
                    'foreign_keys': 'db_DeptManager.employee_number'
                    ,'primaryjoin': 'remote(db_Employees.employee_number) == foreign(db_DeptManager.employee_number)'
                }
            },
            {
                'rel_name': 'department'
                ,'rel_class_name': 'db_Departments'
                ,'rel_arguments': {
                    'foreign_keys': 'db_DeptManager.employee_number'
                    ,'primaryjoin': 'remote(db_Departments.department_number) == foreign(db_DeptManager.department_number)    '
                }
            },
        ]
    },
    {
        'GQL_CLASS_NAME': 'Employee'
        ,'GQL_CONN_CLASS_NAME': 'EmployeeConnection'
        ,'GQL_CONN_QUERY_NAME': 'employee'
        ,'DB_CLASS_NAME': 'db_Employees'
        ,'DB_TABLE_NAME': 'employees'
        ,'DB_TABLE_PK': 'emp_no'
        ,'DB_DEFAULT_SORT_COL': 'emp_no'
        ,'FIELDS': [
            {
                'gql_col_name': 'employee_number'
                ,'gql_type': graphene.String
                ,'gql_description': 'Employee number (PK).'
                ,'db_col_name': 'emp_no'
                ,'db_type': Integer
            },
            {
                'gql_col_name': 'first_name'
                ,'gql_type': graphene.String
                ,'gql_description': 'First name.'
                ,'db_col_name': 'first_name'
                ,'db_type': String
            },
            {
                'gql_col_name': 'last_name'
                ,'gql_type': graphene.String
                ,'gql_description': 'Last name.'
                ,'db_col_name': 'last_name'
                ,'db_type': String
            },
            {
                'gql_col_name': 'birth_day'
                ,'gql_type': graphene.Date
                ,'gql_description': 'Birth day.'
                ,'db_col_name': 'birth_date'
                ,'db_type': Date
            },
            {
                'gql_col_name': 'hire_date'
                ,'gql_type': graphene.Date
                ,'gql_description': 'Hire day.'
                ,'db_col_name': 'hire_date'
                ,'db_type': Date
            },
            {
                'gql_col_name': 'gender'
                ,'gql_type': graphene.String
                ,'gql_description': 'Gender.'
                ,'db_col_name': 'gender'
                ,'db_type': String
            }
        ]
        ,'RELATIONSHIPS': [
            {
                'rel_name': 'employee_department'
                ,'rel_class_name': 'db_DeptEmp'
                ,'rel_arguments': {
                    'foreign_keys': 'db_Employees.employee_number'
                    ,'primaryjoin': 'remote(db_DeptEmp.employee_number) == foreign(db_Employees.employee_number)'
                }
            },
            {
                'rel_name': 'employee_salary'
                ,'rel_class_name': 'db_Salaries'
                ,'rel_arguments': {
                    'foreign_keys': 'db_Employees.employee_number'
                    ,'primaryjoin': 'remote(db_Salaries.employee_number) == foreign(db_Employees.employee_number)'
                }
            },
            {
                'rel_name': 'employee_title'
                ,'rel_class_name': 'db_Titles'
                ,'rel_arguments': {
                    'foreign_keys': 'db_Employees.employee_number'
                    ,'primaryjoin': 'remote(db_Titles.employee_number) == foreign(db_Employees.employee_number)'
                }
            },
        ]
    },
    {
        'GQL_CLASS_NAME': 'Salaries'
        ,'GQL_CONN_CLASS_NAME': 'SalariesConnection'
        ,'GQL_CONN_QUERY_NAME': 'employee_salary'
        ,'DB_CLASS_NAME': 'db_Salaries'
        ,'DB_TABLE_NAME': 'salaries'
        ,'DB_TABLE_PK': 'emp_no'
        ,'DB_DEFAULT_SORT_COL': 'emp_no'
        ,'FIELDS': [
            {
                'gql_col_name': 'employee_number'
                ,'gql_type': graphene.String
                ,'gql_description': 'Employee number.'
                ,'db_col_name': 'emp_no'
                ,'db_type': Integer
            },
            {
                'gql_col_name': 'salary'
                ,'gql_type': graphene.Int
                ,'gql_description': 'Employee salary.'
                ,'db_col_name': 'salary'
                ,'db_type': Integer
            },
            {
                'gql_col_name': 'from_date'
                ,'gql_type': graphene.String
                ,'gql_description': 'Start date of salary assignment.'
                ,'db_col_name': 'from_date'
                ,'db_type': Date
            },
            {
                'gql_col_name': 'to_date'
                ,'gql_type': graphene.String
                ,'gql_description': 'End date of salary assignment.'
                ,'db_col_name': 'to_date'
                ,'db_type': Date
            },
        ]
        ,'RELATIONSHIPS': []
    },
    {
        'GQL_CLASS_NAME': 'Titles'
        ,'GQL_CONN_CLASS_NAME': 'TitlesConnection'
        ,'GQL_CONN_QUERY_NAME': 'employee_title'
        ,'DB_CLASS_NAME': 'db_Titles'
        ,'DB_TABLE_NAME': 'titles'
        ,'DB_TABLE_PK': 'emp_no'
        ,'DB_DEFAULT_SORT_COL': 'emp_no'
        ,'FIELDS': [
            {
                'gql_col_name': 'employee_number'
                ,'gql_type': graphene.String
                ,'gql_description': 'Employee number.'
                ,'db_col_name': 'emp_no'
                ,'db_type': Integer
            },
            {
                'gql_col_name': 'title'
                ,'gql_type': graphene.String
                ,'gql_description': 'Employee title.'
                ,'db_col_name': 'title'
                ,'db_type': String
            },
            {
                'gql_col_name': 'from_date'
                ,'gql_type': graphene.String
                ,'gql_description': 'Start date of title assignment.'
                ,'db_col_name': 'from_date'
                ,'db_type': Date
            },
            {
                'gql_col_name': 'to_date'
                ,'gql_type': graphene.String
                ,'gql_description': 'End date of title assignment.'
                ,'db_col_name': 'to_date'
                ,'db_type': Date
            },
        ]
        ,'RELATIONSHIPS': []
    },
]
```