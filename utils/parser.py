class ReqParser(object):
    @classmethod
    def check_body(cls, req, params):
        for param in params:
            if param not in req:
                return False
        return True
    @classmethod
    def as_jsonlist(cls, chunk):
        return list(map(lambda x: x.json() if x else None, chunk))

