# project


** Build System with the following specifications:

    1. Create a file system where the file is read and data is stored in the database.
    2. Create an API to fetch the data with features of search, filter and pagination

    Explanation:

    1. Create one microservice which reads the file line by line with new data on each new line
    2. Use Rabbitmq to create a queue and push a request into the queue in the publisher
    3. Create a new microservice consumer which receives the data and stores it in the Postgresql database in the table
    <HOST:POST>/<enpoint>?pageno=1&pagesize=10&name=xyz

** Share the installation and readme file for setup as well.