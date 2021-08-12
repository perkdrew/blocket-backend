# Blocket Code Exercise

## Overview

For this coding exercise with the Blocket team, I decided to use Docker, FastAPI, Postgres, GraphQL, and Pytest. I have worked with FastAPI and Docker extensively in the past, and have used Pytest for any test suite. However, GraphQL is entirely new for me. I thought that this would be something worth implementing to open up the floor for discussion. 

## Database 

In setting up my project, I quickly structured Docker Compose with Postgres and PGAdmin for a lightweight connection with a relational database. From there, I established migrations using SQLAlchemy with Alembic for ORM support:

```
alembic init alembic
docker-compose run app alembic revision --autogenerate -m "New Migration" 
docker-compose run app alembic upgrade head
```

## GraphQL

For structuring the functionality we would like for our classified ads, the typical CRUD functionality is set up as mutations in GraphQL. It allows us to define schemas that we situate for our queries. To start, we need to populate the database with some data as such:

```
mutation CreateNewAdvertisement{ 
  createNewAdvertisement(
    subject:"Promotional", body:"Here is my ad!", price: 300, email: "drewcperkins@gmail.com"
  ) { ok } }
```

Now we can begin to query through the classified ads that we have created. For a general list, we can query as such:

```
query{ allAdvertisements{ subject, body, price, email } }
```

In order for us to sort by a particular field we have in our data model, there are some abstractions in GraphQL and Relay to build out connections that more easily paginate and splice data; However, I created a simple enum between the two types of sorts we would like:

```
query{ allAdvertisements (sort: 0) { createdAt } }
```

```
query{ allAdvertisements (sort: 1) { price } }
```

We can also filter by different fields, such as ID:

```
query{ advertisementById(advertisementId:2){ id subject body } }

```

For deleting any classified ads, I created another mutation that removes them by ID:

```
mutation DeleteAdvertisement{ 
  deleteAdvertisement(advertisementId:2) { ok } }
```

## Conclusion

This exercise gave me some experience to work with GraphQL. For a simple API that we can use for classified ads, this one should suffice. The flexibility of the schema for the client and the central fast, query structure make GraphQL a reasonable alternative to REST. One area where I believe GraphQL would prove quite advantageous would be as an entrypoint for a microservice cluster.  
