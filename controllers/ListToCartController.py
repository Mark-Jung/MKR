from models.ListToCartModel import ListToCartModel 
from models.MemberModel import MemberModel

from utils.logger import Logger

class ListToCartController():
    logger = Logger(__name__)

    @classmethod
    def register_list(cls, member_id, fam_id, alias, in_store):
        # make list_to_cart object
        member = MemberModel.find_by_id(member_id)
        try:
            new_list_to_cart = ListToCartModel(alias, in_store, fam_id, member.first_name + " " + member.last_name)
            new_list_to_cart.save_to_db()
        except:
            cls.logger.exception("Error making a new ListToCart object")
            return "Internal Server Error", 500

        return "", 201

    @classmethod
    def register_cart(cls, fam_id, data):
        # find listtocart object and update the fields
        list_to_cart = ListToCartModel.find_by_id(data["list_to_cart_id"])
        if not list_to_cart:
            return "Ill-formed Request", 400

        # Not your family
        if list_to_cart.fam_id != fam_id:
            cls.logger("WARNING WARNING WARNING BREACH ATTEMPA. At this point it should be pretty obvious that this is someone meddling with our endpoint.")
            return "Ill-formed Requst", 400

        try:
            list_to_cart.in_cart = True
            list_to_cart.in_store = data['in_store']
            list_to_cart.item_image = data['item_image']
            list_to_cart.item_name = data['item_name']
            list_to_cart.item_price = data['item_price']
            list_to_cart.item_quantity = data['item_quantity']
            list_to_cart.save_to_db()
        except:
            cls.logger.exception("Error updated ListToCart object")
            return "Internal Server Error", 500

        return "", 200
