from models.MemberModel import MemberModel
from models.CheckoutModel import CheckoutModel
from models.ProductModel import ProductModel


from utils.logger import Logger

class CheckoutController():
    logger = Logger(__name__)

    @classmethod
    def checkout(cls, member_id, data):
        # make checkout object
        member = MemberModel.find_by_id(member_id)
        try:
            new_checkout = CheckoutModel(member.fam_id, member.first_name, member.last_name, data['total'])
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

        return "", 201
