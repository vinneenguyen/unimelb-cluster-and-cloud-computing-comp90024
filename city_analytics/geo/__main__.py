import time
from datetime import datetime, timedelta
import configparser
from pathlib import Path
import pandas as pd
import geopandas as gpd
from IPython.display import display

from utils.couch import view_covid
from utils.plots import geomap

# Global constants
DATADIR = Path("data")
RESULTDIR = Path("static")
GEOFILE = DATADIR / "aurin_datasource-AU_Govt_ABS-UoM_AURIN_DB_3_sa4_aggregated_pop_and_dwelling_counts_census_2016.json"
INVFILE = "../inventories/hosts_auto.ini"  # inventory file
DBGROUP = "couchdbgroup"  # db cluster
HOSTNAME = "thinkbox2 ansible_host"  # to retrieve IP address
USERNAME = "admin"
PASSWORD = "password"


def _get_ip():
    """
    Parse IP address from inventory file
    :return:
    """

    config = configparser.ConfigParser()
    config.read(INVFILE)
    ip = config[DBGROUP][HOSTNAME]

    return ip


def _do_covid():
    """
    Retrieve tweet data and plot map
    :return:
    """

    ip = _get_ip()

    # View
    dbname = "tweet-covid"
    docid = "covid"
    name = "sentiment_location"
    partition_key = "name"
    area_col = "area_code"
    var_col = "variable"
    val_col = "count"
    stat_col = "count"
    data = view_covid(name, partition_key=partition_key, area_col=area_col, var_col=var_col, val_col=val_col,
                      docid=docid, dbname=dbname, ip=ip, username=USERNAME, password=PASSWORD)
    var_levels = data[var_col].unique()  # variable levels
    data = pd.pivot_table(data, values=val_col, index=[area_col], columns=[var_col], fill_value=0).reset_index()
    data[stat_col] = data[var_levels].sum(axis=1)  # sum all variable levels
    display(data)

    # Map
    outfile = RESULTDIR / "covid_sa4.html"  # output map
    columns = [area_col, stat_col]
    key_on = "feature.properties.sa4_code_2016"
    fill_color = "YlOrRd"
    legend_name = "No. of tweets"
    fields = ["sa4_code_2016", "sa4_name"]
    aliases = ["area code", "area name"]
    labels = True
    m = geomap(GEOFILE, data, columns, key_on, fill_color=fill_color, legend_name=legend_name, fields=fields,
               aliases=aliases, labels=labels)
    display(m)
    m.save(outfile.as_posix())


def _do_covidsafe():
    """
    Retrieve tweet data and plot map
    :return:
    """

    ip = _get_ip()

    # View
    dbname = "tweet-covid-covidsafe"
    docid = "covidsafe"
    name = "sentiment_location"
    partition_key = "name"
    area_col = "area_code"
    var_col = "variable"
    val_col = "count"
    stat_col = "rate"
    data = view_covid(name, partition_key=partition_key, area_col=area_col, var_col=var_col, val_col=val_col,
                      docid=docid, dbname=dbname, ip=ip, username=USERNAME, password=PASSWORD)
    var_levels = data[var_col].unique()  # variable levels
    data = pd.pivot_table(data, values=val_col, index=[area_col], columns=[var_col], fill_value=0).reset_index()
    data[stat_col] = data.positive / (data.positive + data.negative)  # positive tweet ratio
    display(data)

    # Map
    outfile = RESULTDIR / "covidsafe_sentiment_sa4.html"  # output map
    columns = [area_col, stat_col]
    key_on = "feature.properties.sa4_code_2016"
    fill_color = "RdYlGn"
    legend_name = "Positivity rate"
    fields = ["sa4_code_2016", "sa4_name"]
    aliases = ["area code", "area name"]
    labels = True
    m = geomap(GEOFILE, data, columns, key_on, fill_color=fill_color, legend_name=legend_name, fields=fields,
               aliases=aliases, labels=labels)
    display(m)
    m.save(outfile.as_posix())


def _do_symptoms():
    """
    Retrieve tweet data and plot graphs
    :return:
    """

    ip = _get_ip()
    datageo = gpd.read_file(GEOFILE)

    # View
    dbname = "symptoms"
    docid = "symptoms"
    name = "symptoms_location"
    partition_key = ""
    area_col = "area_code"
    var_col = "symptom"
    val_col = "count"
    stat_col = "count"
    data = view_covid(name, partition_key=partition_key, area_col=area_col, var_col=var_col, val_col=val_col,
                      docid=docid, dbname=dbname, ip=ip, username=USERNAME, password=PASSWORD)
    data = data[pd.to_numeric(data[area_col]) >= 0]  # drop invalid area values
    data = data.explode(var_col)  # unpack lists in column
    var_levels = data[var_col].unique()  # variable levels
    data = pd.pivot_table(data, values=val_col, index=[area_col], columns=[var_col], fill_value=0).reset_index()
    data[stat_col] = data[var_levels].sum(axis=1)
    display(data)

    # Tweet count by symptom for top areas
    outfile = RESULTDIR / "symptoms_top_areas_sa4.png"  # output graph
    ntop = 3
    data_ntop = data.nlargest(ntop, "count")  # by area
    data_ntop["area_name"] = datageo.set_index("sa4_code_2016").lookup(data_ntop.area_code, ["sa4_name"] * ntop)
    data_ntop = data_ntop.set_index(["area_name", "area_code"])[var_levels]
    data_trans = data_ntop.T  # transpose
    ax = data_trans.plot.barh(rot=0, figsize=(12, 8))
    ax.invert_yaxis()  # invert for largest on top
    for p in ax.patches:
        ax.text(p.get_width(), p.get_y(), p.get_width())  # annotation
    ax.set_xlabel("No. of tweets")
    ax.set_ylabel("Symptom")
    ax.get_figure().savefig(outfile, bbox_inches="tight")

    # Tweet count by symptom total
    outfile = RESULTDIR / "symptoms_total_sa4.png"  # output graph
    data_total = data[var_levels].sum().to_frame(name="total_tweets")  # total by symptom
    ax = data_total.plot.pie(y="total_tweets", autopct="%.2f", labels=None, figsize=(8, 8))
    ax.get_figure().savefig(outfile, bbox_inches="tight")


def main():
    """
    Create graphs
    :return:
    """
    _do_covid()
    _do_covidsafe()
    _do_symptoms()


if __name__ == "__main__":
    cyc = 60  # seconds
    while True:
        main()
        print(f"Next execution scheduled at {datetime.now() + timedelta(seconds=cyc)}")
        time.sleep(cyc)
