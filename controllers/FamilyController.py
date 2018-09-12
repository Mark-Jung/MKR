from datetime import datetime
import string
from random import *
import asyncio

from models.FamilyModel import FamilyModel
from models.MemberModel import MemberModel

from utils.email import Emailer
from utils.logger import Logger

class FamilyController():
    promo_length = 8
    allchar = string.ascii_letters + string.digits
    logger = Logger(__name__)

    @classmethod
    def register_family(cls, data, member_id):
        # check if family with the same name exist
        fam_already = FamilyModel.find_by_name(data['name'])
        if fam_already:
            return "Ill-formed Reqeust. Name should be unique", 400, None
        registerer = MemberModel.find_by_id(member_id)

        try: 
            admin_invite = FamilyController.generate_invite(data['name'] + '_admin_')
            member_invite = FamilyController.generate_invite(data['name'] + '_member_')
            new_fam = FamilyModel(data['address_line1'], data['address_line2'], data['city'], data['state'], data['zip_code'], data['name'], data['phone'], registerer.email, admin_invite, member_invite)
            new_fam.save_to_db()
        except:
            cls.logger.exception("Error creating a family model")
            return "Internal Server Error", 500, None

        registerer.authority = 100
        registerer.fam_id = new_fam.id
        registerer.save_to_db()

        if asyncio.get_event_loop().is_closed():
            asyncio.set_event_loop(asyncio.new_event_loop())

        loop = asyncio.get_event_loop()
        
        # send email to who registered
        tasks = [
            asyncio.ensure_future(Emailer.create_fam(registerer.email, registerer.first_name, new_fam.admin_invite, new_fam.member_invite, new_fam.name))
        ]
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()

        return "", 201, {"admin": new_fam.admin_invite, "member": new_fam.member_invite}
    
    @classmethod
    def generate_invite(cls, keyword):
        found = False
        new_invite = keyword
        while not found:
            for x in range(cls.promo_length):
                new_invite += choice(cls.allchar)
            if FamilyModel.find_by_invite_admin(new_invite) is None and FamilyModel.find_by_invite_member(new_invite) is None:
                found = True
            else:
                new_invite = keyword
            
        return new_invite

    @classmethod
    def join_family(cls, invite_code, member_id):
        family = FamilyModel.find_by_invite_admin(invite_code)
        member = MemberModel.find_by_id(member_id)
        if family:
            fam_id = family.id
            invite_code_admin = family.admin_invite
            invite_code_member = family.member_invite
            authority = 100
        else:
            family = FamilyModel.find_by_invite_member(invite_code)
            if family:
                fam_id = family.id
                authority = 50
            else:
                cls.logger.exception("Invalid invite_code")
                return "Ill-formed Request", 400
        member.authority = authority
        member.fam_id = fam_id
        member.save_to_db()

        if asyncio.get_event_loop().is_closed():
                asyncio.set_event_loop(asyncio.new_event_loop())

        loop = asyncio.get_event_loop()
        
        # send email to who joined
        tasks = [
            asyncio.ensure_future(Emailer.join_fam(member.email, member.first_name, family.name))
        ]
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()

        return "", 200