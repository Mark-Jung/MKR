import asyncio

from models.CheckoutModel import CheckoutModel
from models.FamilyModel import FamilyModel
from models.MemberModel import MemberModel
from models.ProductModel import ProductModel

from utils.logger import Logger
from utils.email import Emailer

class CheckoutController():
    logger = Logger(__name__)

    @classmethod
    def checkout(cls, member_id, data):
        # make checkout object
        member = MemberModel.find_by_id(member_id)
        if member.authority != 100:
            return "Ill-formed Request", 403
            
        try:
            new_checkout = CheckoutModel(data['total'], member_id)
            new_checkout.save_to_db()
        except:
            cls.logger.exception("Error creating new Checkout object")
            return "Internal Server Error", 500
        
        # make the list of objects
        for product in data['items']:
            try:
                new_product = ProductModel(product['store'], product['price'], product['url'], product['name'], new_checkout.id)
                new_product.save_to_db()
            except:
                cls.logger.exception("Error creating new Product")
                return "Internal Server Error", 500
    
        family = FamilyModel.find_by_id(member.fam_id)
        
        if asyncio.get_event_loop().is_closed():
            asyncio.set_event_loop(asyncio.new_event_loop())
        loop = asyncio.get_event_loop()
        # send email to deliver :)
        tasks = [asyncio.ensure_future(Emailer.checkout(data['total'], member.first_name + ' ' + member.last_name, family.name, data['items'], new_checkout.id))]
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()

        return "", 201
