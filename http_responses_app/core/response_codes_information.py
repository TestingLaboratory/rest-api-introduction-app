from collections import namedtuple

ResponseInformation = namedtuple("ResponseInformation", ["shortDescription", "longDescription"])

__code_information = {
    200: ResponseInformation("OK", "The request has succeeded"),
    201: ResponseInformation("CREATED", "The request has succeeded and a new resource has been created as a result"),
    400: ResponseInformation("Bad Request", "The server could not understand the request due to invalid syntax."),
    401: ResponseInformation("Unauthorized", "The client must authenticate or authorize itself to get the requested "
                                             "response."),
    403: ResponseInformation("Forbidden", "The client does not have access rights to the content; that is, "
                                          "it is unauthorized, so the server is refusing to give the requested "
                                          "resource."),
    404: ResponseInformation("Not Found", "The server can not find the requested resource. In the browser, this means "
                                          "the URL is not recognized. In an API, this can also mean that the endpoint "
                                          "is valid but the resource itself does not exist"),
    500: ResponseInformation("Internal Server Error", "The server has encountered a situation it doesn't know how to "
                                                      "handle"),
    503: ResponseInformation("Service Unavailable", "The server is not ready to handle the request due to maintenance "
                                                    "or overloaded")
}


def get_code_information(code: int) -> dict:
    return __code_information[code]._asdict()
