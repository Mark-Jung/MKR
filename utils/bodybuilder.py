class BodyBuilder():
    """
    Constructs the html body of the email
    """
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

        