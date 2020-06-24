from cloudant.client import CouchDB
from cloudant.design_document import DesignDocument
from cloudant.view import View
import pandas as pd


def view_covid(name, partition_key="", area_col="area_code", var_col="variable", val_col="count", reduce=True,
               group=True, group_level=2,
               docid="", dbname="",
               ip="", username="admin", password="password", port=5984, connect=True):
    """
    View database
    """

    url = f"http://{ip}:{port}"
    client = CouchDB(username, password, url=url, connect=connect)
    db = client[dbname]  # database
    ddoc = DesignDocument(db, docid)

    # View
    view = View(ddoc, name, partition_key=partition_key)
    area_codes = []
    variables = []
    counts = []
    for row in view(reduce=reduce, group=group, group_level=group_level)['rows']:
        var, code = row["key"]  # variable, area code
        variables.append(var)
        area_codes.append(code)
        counts.append(row["value"])

    # Data
    data = pd.DataFrame(
        {area_col: map(str, area_codes), var_col: variables, val_col: counts})  # area code in geo-map string stype

    return data
