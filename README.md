# microblog service

Test task for BYM.

**Prerequisites**

This project created using Ubuntu 18.04

You need PostgreSQL installed and you also need `microblog` database created there with corresponding user and password.


Before you run server, you need to upgrade database using command `flask db upgrade` and to create number of fake users. To do it type `flask shell` and in shell you need to type the following commands:

`from microblog.api.models import User`

`User.generate_fake(count=100)`

100 is default value, you can replace it with your own. 

To run local server just type `flask run` in your terminal

The list of available users available at `/api/v1/users`

To simplify work with service, all users got created with the same password - `Pa$$w0rd`

Repository also contains postman collection with availilable api calls.

**Ways to improve**

1. Add unit tests;
2. Add possibility to run with docker-compose;
3. Add configurations to enable CI/CD.