import graphene
from datetime import datetime

import models
from schemas import AdvertisementSchema
from db_conf import db_session

db = db_session.session_factory()


class CreateNewAdvertisement(graphene.Mutation):
    class Arguments:
        subject = graphene.String(required=True)
        body = graphene.String(required=True)
        price = graphene.Float(required=False)
        email = graphene.String(required=True)

    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, subject: str, body: str, email: str, price: float = None):
        advertisement = AdvertisementSchema(
            subject=subject, body=body, price=price, email=email,
        )
        db_ad = models.Advertisement(
            subject=advertisement.subject,
            body=advertisement.body,
            price=advertisement.price,
            email=advertisement.email,
        )
        db.add(db_ad)
        db.commit()
        db.refresh(db_ad)
        return CreateNewAdvertisement(ok=True)


class UpdateAdvertisement(graphene.Mutation):
    class Arguments:
        advertisement_id = graphene.ID(required=True)
        subject = graphene.String(required=False)
        body = graphene.String(required=False)
        price = graphene.Float(required=False)
        email = graphene.String(required=False)

    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, advertisement_id: int, subject: str = None, body: str = None,
               email: str = None, price: float = None):

        advertisement = db.query(models.Advertisement).filter(models.Advertisement.id == advertisement_id).first()

        if advertisement is None:
            return UpdateAdvertisement(ok=False)

        partial_update = {"updated_at": datetime.utcnow()}
        if subject is not None:
            partial_update["subject"] = subject
        if body is not None:
            partial_update["body"] = body
        if email is not None:
            partial_update["email"] = email
        if price is not None:
            partial_update["price"] = price

        db.query(models.Advertisement).filter(models.Advertisement.id == advertisement_id).update(partial_update)
        db.commit()
        return UpdateAdvertisement(ok=True)


class DeleteAdvertisement(graphene.Mutation):
    class Arguments:
        advertisement_id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, advertisement_id: int):

        advertisement = db.query(models.Advertisement).filter(models.Advertisement.id == advertisement_id).first()
        if advertisement is None:
            return DeleteAdvertisement(ok=False)

        db.query(models.Advertisement).filter(models.Advertisement.id == advertisement_id).delete()
        db.commit()
        return DeleteAdvertisement(ok=True)


class AdvertisementMutations(graphene.ObjectType):
    create_new_advertisement = CreateNewAdvertisement.Field()
    update_advertisement = UpdateAdvertisement.Field()
    delete_advertisement = DeleteAdvertisement.Field()
