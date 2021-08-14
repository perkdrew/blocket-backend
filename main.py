import graphene
from fastapi import FastAPI
from starlette.graphql import GraphQLApp

from mutations import AdvertisementMutations
from queries import Query

app = FastAPI()

schema = graphene.Schema(mutation=AdvertisementMutations, query=Query)

app.add_route("/", GraphQLApp(schema=schema))
