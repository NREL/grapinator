# Demo GraphQL Queries

## Return all female employees with a last name of Montemayor sorting by last name ascending.
```
{
  employee(gender:"F" last_name:"Montemayor" logic:"and" sort_by:"last_name" sort_dir:"asc") {
    edges {
      node {
        employee_number
        first_name
        last_name
        birth_day
        hire_date
        gender
        
        employee_department {
          department {
            department_number
            department_name
          }
        }
        
        employee_title {
          title
          from_date
          to_date
        }

        employee_salary {
          salary
          from_date
          to_date
        }
      }
    }
  }
} 
```

## Return all department managers and their employee information.
```
{
	department_managers {
    edges {
      node {
        employee {
          employee_number
          first_name
          last_name
          hire_date
          gender
          
          employee_department {
            department {
              department_number
              department_name
            }
          }
          
          employee_title {
            title
            from_date
            to_date
          }
          
          employee_salary {
            salary
            from_date
            to_date
          }          
        }
      }
    }
  }
}
```