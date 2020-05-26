# author: Vinh Nguyen

import folium


def geomap(geo_data, data, columns, key_on, fill_color="YlOrRd", nan_fill_color="white", fill_opacity=0.7,
           line_opacity=0.2,
           legend_name="value", highlight=True,
           fields=None, aliases=None, labels=True,
           location=(-23.6980, 133.8807), zoom_start=4, tiles="cartodbpositron"):
    """
    Create geospatial map
    Refer Folium documentation for parameters.
    """

    fields = fields or []
    aliases = aliases or []

    # Map
    m = folium.Map(location=location, zoom_start=zoom_start, tiles=tiles)

    # Layer
    choropleth = folium.Choropleth(
        geo_data=str(geo_data),
        data=data,
        columns=columns,
        key_on=key_on,
        fill_color=fill_color,
        nan_fill_color=nan_fill_color,
        fill_opacity=fill_opacity,
        line_opacity=line_opacity,
        legend_name=legend_name,
        highlight=highlight
    ).add_to(m)

    # Pop-up display
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(fields, aliases=aliases, labels=labels)
    )

    folium.LayerControl().add_to(m)

    return m
