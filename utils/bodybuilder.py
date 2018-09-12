class BodyBuilder():
    """
    Constructs the html body of the email
    """
    @classmethod
    def alert_order(cls, total, member_name, family_name, items, checkout_id):
        body = """
        <html>
            <body style="text-align:center; font-size: 18px; font-family: 'Times New Roman', Times, serif;">
                <h3>{member_name} from family {family_name} has placed an order!</h3>
                <div style="margin-top: 3px;">Checkout ID: {checkout_id} </div>
                <div style="margin-top: 3px;">Move yo ass! </div>
                <br>
                <div style="margin-top: 3px;">estimated total is {total} </div>
                <div>Thank you</div>
                <br>
                <hr style="width:50%;">
                <br>
                <div>items list:</div>
                <br>
        """.format(total=float(total/100), member_name=member_name, family_name=family_name, checkout_id=checkout_id)
        for product in items:
            body += """
                <br>
                <div style="margin-top: 3px;">Item ID(in niche database): {id} </div>
                <div style="margin-top: 3px;">Item Name: {name} </div>
                <div style="margin-top: 3px;">Item Store: {store} </div>
                <div style="margin-top: 3px;">Item Price: {price} </div>
                <div style="margin-top: 3px;">Item Image below </div>
                <img style="width: 200px; height: 110px;" src="{url}" alt="item picture" title="picture"/>
                <br>
            """.format(id=product['id'], store=product['in_store'], price='%.2f' % float(product['item_price']/100), url=product['item_image'], name=product['item_name'])
        body += """
            </body>
        </html>"""
        return body 

    @classmethod
    def signup_createfam(cls, name, admin_invite, member_invite, fam_name):
        body = """
        <html>
            <body style="text-align:center; font-size: 18px; font-family: 'Times New Roman', Times, serif;">
                <h3>Dear, {name}</h3>
                <div style="margin-top: 3px;">Thank you for joining Niche! </div>
                <div style="margin-top: 3px;">You've created a family called </div>
                <br>
                <div style="margin-top: 3px;">{fam_name} </div>
                <div style="margin-top: 3px;">Below are the invite codes for the family</div>
                <div style="margin-top: 3px;">Admin Invite Code: {admin_invite}</div>
                <div style="margin-top: 3px;">Member Invite Code: {member_invite} USD</div>
                <div>Thank you</div>
                <br>
                <hr style="width:50%;">
                <br>
                <div>Send us any questions or comments you have! We want to hear from you. <3</div>
                <br>
                <hr style="width:50%;">
                <br>
                <div>Team Niche</div>
            </body>
        </html>
        """.format(name=name, admin_invite=admin_invite, member_invite=member_invite, fam_name=fam_name)
        return body
    @classmethod
    def signup_joinfam(cls, name, fam_name):
        body = """
        <html>
            <body style="text-align:center; font-size: 18px; font-family: 'Times New Roman', Times, serif;">
                <h3>Dear, {name}</h3>
                <div style="margin-top: 3px;">Thank you for joining Niche! </div>
                <div style="margin-top: 3px;">You've joined a family called </div>
                <br>
                <div style="margin-top: 3px;">{fam_name} </div>
                <div>Thank you</div>
                <br>
                <hr style="width:50%;">
                <br>
                <div>Send us any questions or comments you have! We want to hear from you. <3</div>
                <br>
                <hr style="width:50%;">
                <br>
                <div>Team Niche</div>
            </body>
        </html>
        """.format(name=name, fam_name=fam_name)
        return body

    @classmethod
    def verification(cls, name, code):
        body = """
        <html>
            <body style="text-align:center; font-size: 18px; font-family: 'Times New Roman', Times, serif;">
                <h3>Dear, {name}</h3>
                <div style="margin-top: 3px;">Here is your verification code! </div>
                <br>
                <div style="margin-top: 3px;">{code} </div>
                <div>Thank you</div>
                <br>
                <hr style="width:50%;">
                <br>
                <div>Send us any questions or comments you have! We want to hear from you. <3</div>
                <br>
                <hr style="width:50%;">
                <br>
                <div>Team Niche</div>
            </body>
        </html>
        """.format(name=name, code=code)
        return body
    
        