# Entity Extraction

Extracting entities from user input

Link to flask API: 'https://dev.ird.----.com/entity-model/entity_extraction'

Input is a JSON with the following format:
{"user_input_text":"","state":"", "intent": ""}

Returns string with a json format with the structure below:
{"axes": [{"name": "plot_y", "value": "CTR"}, {"name": "plot_x", "value": "discount"}, {"name": "plot_groupby", "value": "discount"}], "filters": [{"name": "brand", "value": "upscale"}, {"name": "discount", "value": "0"}]}
