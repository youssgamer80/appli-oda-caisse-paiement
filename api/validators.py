
def validateApi(request,SerializeModel):
    res = {}
    res["success"] = True
    res["errors"] = None
    res["details"] = None
    validation = SerializeModel(data=request)
    if validation.is_valid():
        res["success"] = True
        res["data"] = validation
    else:
        res["success"] = False
        res["details"] = "Bad Request Body"
        res["errors"] = validation.errors
    return res