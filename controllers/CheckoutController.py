import asyncio

from models.CheckoutModel import CheckoutModel
from models.FamilyModel import FamilyModel
from models.ListToCartModel import ListToCartModel
from models.MemberModel import MemberModel
from models.ProductModel import ProductModel

from utils.logger import Logger
from utils.email import Emailer

class CheckoutController():
    logger = Logger(__name__)

    @classmethod
    def checkout(cls, member_id, fam_id, total, items):
        # make checkout object
        member = MemberModel.find_by_id(member_id)
        if member.authority != 100:
            return "Unauthorized Request", 403
            
        try:
            new_checkout = CheckoutModel(total, member_id)
            new_checkout.save_to_db()
        except:
            cls.logger.exception("Error creating new Checkout object")
            return "Internal Server Error", 500
        
        item_data = []
        for list_to_cart_id in items:
            target = ListToCartModel.find_by_id(list_to_cart_id)
            if target:
                if target.in_cart and target.item_name and target.item_image and target.item_price and target.item_quantity:
                    item_data.append(target.json())
                else:
                    cls.logger.exception("Requested a list_to_cart that doens't have sufficient info for checkout")
                    return "Ill-formed Request", 400
            else:
                cls.logger.exception("Reqeusts a list_to_cart that doesn't exist")
                return "Ill-formed Request", 400
        
        # make the list of objects
        for product in item_data:
            try:
                new_product = ProductModel(product['in_store'], product['item_price'], product['item_image'], product['item_name'], new_checkout.id)
                new_product.save_to_db()
            except:
                cls.logger.exception("Error creating new Product")
                return "Internal Server Error", 500
    
        family = FamilyModel.find_by_id(fam_id)
        
        try:
            loop = asyncio.get_event_loop()
        except:
            asyncio.set_event_loop(asyncio.new_event_loop())
        
        loop = asyncio.get_event_loop()
        # send email to deliver :)
        tasks = [asyncio.ensure_future(Emailer.checkout(total, member.first_name + ' ' + member.last_name, family.name, item_data, new_checkout.id))]
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()

        return "", 201
