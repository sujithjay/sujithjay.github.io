---
layout: post
title: A Point of Distinction between MariaDB and MySQL
desc: Difference between MariaDB and MySQL in handling of FROM subquery
permalink: /2017/12/01/A-Point-of-Distinction-between-MariaDB-and-MySQL/
---

## TL; DR
In MariaDB, query with `ORDER BY` in a `FROM` subquery produces an unordered result. In effect, `ORDER BY` is ignored in `FROM` subqueries. MySQL does not ignore `ORDER BY` in `FROM` subqueries.

<!--break-->
## Longer Version
Older versions of MariaDB(< 10.2.0) did not have window functions such as `rank()`, `dense_rank()`, `row_number()` among others. To understand where you would use such a function, `dense_rank()` for instance, consider the following example:

*Given an Employee table and a Department table as shown below, find employees who earn the top three salaries in each of the department.*

Employee Table
--------------------------------------
| Id | Name  | Salary | DepartmentId |
|:--:|:-----:|:------:|:------------:|
| 1  | Joe   | 70000  | 1            |
| 2  | Henry | 80000  | 2            |
| 3  | Sam   | 60000  | 2            |
| 4  | Max   | 90000  | 1            |
| 5  | Janet | 69000  | 1            |
| 6  | Randy | 85000  | 1            |
--------------------------------------

Department Table
-----------------
| Id | Name     |
|:--:|:--------:|
| 1  | IT       |
| 2  | Sales    |
-----------------


I list three approaches to solving this problem, starting with the easiest one which makes use of `dense_rank()`.



### The Dense-Rank Version
Using `dense_rank()`, this can be accomplished using:
```
SELECT * FROM 
     (
      SELECT d.Name as Department, e.Name as Employee, Salary,
      DENSE_RANK() OVER (PARTITION BY DepartmentId ORDER BY Salary DESC) Rank
      FROM Employee e JOIN Department d ON e.DepartmentId = d.id
     ) t
    WHERE rank <= 3
    ORDER BY Department, Rank;
```
[Fiddle Link](http://dbfiddle.uk/?rdbms=mariadb_10.2&fiddle=cc9082f8d09b48dc7f374456ef817a73)


( Homework Assignment: Why use `dense_rank()` instead of `rank()`? How does it affect your result? )



### No Window Functions?!
Things get slightly ugly when you do not have access to window functions. Of course, a workaround could be to use a join and sub-query as shown below:
```
SELECT
    d.Name AS 'Department', e1.Name AS 'Employee', e1.Salary
FROM
    Employee e1
        JOIN
    Department d ON e1.DepartmentId = d.Id
WHERE
    3 > (SELECT
            COUNT(DISTINCT e2.Salary)
        FROM
            Employee e2
        WHERE
            e2.Salary > e1.Salary
                AND e1.DepartmentId = e2.DepartmentId
        );
```
	
But this is sub-optimal, and we can do better. 


### Session Variables
Another way would be to use Session Variables in your queries. This is where the observed behavior of MariaDB and MySQL part ways. I wrote the following query on a fiddle against MySQL 5.6 and expected it to work on MariaDB. Alas!
```
set @did := NULL;
set @rn := 1;
set @sal := NULL;

select `Department`, `Employee`, `Salary` from (
	select t.`Department`, t.`Employee`, t.Salary,
		@rn:= if(@did = DepartmentId, if(@sal = Salary, @rn, @rn + 1), 1 ) as rank,
		@did:= DepartmentId,
		@sal:= Salary
	from 
		(
			select d.name as `Department`, e.Name as `Employee`, DepartmentId, Salary from Employee e 
			inner join Department d on e.DepartmentId = d.Id order by DepartmentId, Salary desc
		) t
	) f where rank <= 3;
```
[Fiddle Link](http://sqlfiddle.com/#!9/627639/697)



As you can see, I make use of an ORDER BY clause inside a FROM subquery. MariaDB blatantly ignores it, while MySQL is more gracious. A few wasted hours and some googling thereafter, I realized this difference and more so, find out that this is not a bug on MariaDB; more of a deliberate feature. According to MariaDB [FAQ](https://mariadb.com/kb/en/library/why-is-order-by-in-a-from-subquery-ignored/),

>A "table" (and subquery in the FROM clause too) is - according to the SQL standard - an unordered set of rows. Rows in a table (or in a >subquery in the FROM clause) do not come in any specific order. That's why the optimizer can ignore the ORDER BY clause that you have >specified. In fact, the SQL standard does not even allow the ORDER BY clause to appear in this subquery (we allow it, because ORDER BY >... LIMIT ... changes the result, the set of rows, not only their order).

>You need to treat the subquery in the FROM clause, as a set of rows in some unspecified and undefined order, and put the ORDER BY on the >top-level SELECT.


It is a bit of a snag to work with this "feature", and I am still trying to solve the original problem in MariaDB versions <10.2.0 using session variables. If you have a solution in mind, or have something more to add to this conversation, comment below.
