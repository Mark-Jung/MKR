from models.ListToCartModel import ListToCartModel 
from models.MemberModel import MemberModel

from utils.logger import Logger

class ListToCartController():
    logger = Logger(__name__)

    @classmethod
    def delete_list(cls, fam_id, victim_ids):
        for victim in victim_ids:
            target = ListToCartModel.find_by_id(victim)
            
            if not target:
                cls.logger.exception("Invalid delete to list_to_cart object requested")
                return "Ill-formed Request", 400, None
            if target.fam_id != fam_id:
                cls.logger.exception("WARNING WARNING WARNING BREACH ATTEMPT. At this point it should be pretty obvious that this is someone meddling with our endpoint.")
                return "Ill-formed Request", 400, None
            if not target.in_cart:
                try:
                    target.delete_from_db()
                except:
                    cls.logger.exception("Error deleting target list_to_cart")
                    return "Internal Server Error", 500, None
        return "", 200, ListToCartModel.get_fam_list(fam_id)
    
    @classmethod
    def delete_cart(cls, fam_id, victim_ids):
        for victim in victim_ids:
            target = ListToCartModel.find_by_id(victim)
            
            if not target:
                cls.logger.exception("Invalid delete to list_to_cart object requested")
                return "Ill-formed Request", 400, None
            if target.fam_id != fam_id:
                cls.logger.exception("WARNING WARNING WARNING BREACH ATTEMPT. At this point it should be pretty obvious that this is someone meddling with our endpoint.")
                return "Ill-formed Request", 400, None
            if target.in_cart:
                try:
                    target.delete_from_db()
                except:
                    cls.logger.exception("Error deleting target list_to_cart")
                    return "Internal Server Error", 500, None
        return "", 200, ListToCartModel.get_fam_cart(fam_id)


    @classmethod
    def edit_list_to_cart(cls, fam_id, data):
        # find listtocart object and update the fields
        target = ListToCartModel.find_by_id(data["list_to_cart_id"])

        # no such target
        if not target:
            cls.logger.exception("Invalid edit to list_to_target object requested")
            return "Ill-formed Request", 400
        # Not your family
        if target.fam_id != fam_id:
            cls.logger.exception("WARNING WARNING WARNING BREACH ATTEMPT. At this point it should be pretty obvious that this is someone meddling with our endpoint.")
            return "Ill-formed Request", 400

        try:
            target.alias = data['alias']
            target.in_cart = data['in_cart']
            target.in_store = data['in_store']
            target.item_image = data['item_image']
            target.item_name = data['item_name']
            target.item_price = data['item_price']
            target.item_quantity = data['item_quantity']
            target.save_to_db()
        except:
            cls.logger.exception("Error updating ListToCart object")
            return "Internal Server Error", 500

        return "", 200


    @classmethod
    def switch_list_to_cart(cls, fam_id, list_to_cart_id):
        target = ListToCartModel.find_by_id(list_to_cart_id)
        
        if not target:
            cls.logger.exception("Invalid list_to_cart object requested")
            return "Ill-formed Request", 400
        if target.fam_id != fam_id:
            cls.logger.exception("WARNING WARNING WARNING BREACH ATTEMPT. At this point it should be pretty obvious that this is someone meddling with our endpoint.")
            return "Ill-formed Request", 400
        try:
            target.in_cart = not target.in_cart
            target.in_store = ""
            target.item_image = ""
            target.item_name = ""
            target.item_price = 0
            target.item_quantity = 0
            target.save_to_db()
        except:
            cls.logger.exception("Error toggling and saving list_to_cart")
            return "Internal Server Error", 500

        return "", 200


    @classmethod
    def get_cart(cls, fam_id):
        try:
            return "", 200, ListToCartModel.get_fam_cart(fam_id)
        except:
            cls.logger.exception("Failure in getting cart")
            return "Internal Server Error", 500, None
    
    @classmethod
    def get_list(cls, fam_id):
        try:
            return "", 200, ListToCartModel.get_fam_list(fam_id)
        except:
            cls.logger.exception("Failure in getting list")
            return "Internal Server Error", 500, None

    
    @classmethod
    def register_list(cls, member_id, fam_id, alias, in_store):
        # make list_to_cart object
        member = MemberModel.find_by_id(member_id)
        already = ListToCartModel.get_fam_list(fam_id)
        for each in already:
            if each.alias == alias:
                return "Duplicate item in list", 400
        try:
            new_list_to_cart = ListToCartModel(alias, in_store, fam_id, member.first_name + " " + member.last_name)
            new_list_to_cart.save_to_db()
        except:
            cls.logger.exception("Error making a new ListToCart object")
            return "Internal Server Error", 500

        return "", 201
