# GIS and Census work and notes

## US Census

### Tiger files
```
To read TIGER data and use it programmatically, especially for tasks like determining if a given latitude/longitude falls within a specific geographic boundary defined by TIGER/Line shapefiles, you can follow these steps:

### 1. **Download TIGER/Line Shapefiles:**
   - Visit the [U.S. Census Bureau's TIGER/Line Shapefiles page](https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html) to download the relevant shapefiles for the area of interest, such as Census block groups, tracts, neighborhoods, etc.

### 2. **Set Up Your Environment:**
   - You'll need Python with libraries like `geopandas`, `shapely`, and `fiona`. Install these using pip:
     ```bash
     pip install geopandas shapely fiona
     ```

### 3. **Load and Inspect the Shapefiles:**
   - Use `geopandas` to load the TIGER/Line shapefile:
     ```python
     import geopandas as gpd

     # Load the shapefile
     shapefile_path = "path_to_your_shapefile.shp"
     gdf = gpd.read_file(shapefile_path)

     # Inspect the data
     print(gdf.head())
     ```
   - `gdf` is a GeoDataFrame containing the geometries of the geographic areas.

### 4. **Load and Prepare the Address Data:**
   - If you have a list of addresses with latitude/longitude coordinates, you can create a GeoDataFrame from these:
     ```python
     import pandas as pd
     from shapely.geometry import Point

     # Sample DataFrame with lat/long
     data = {
         'address': ['Address1', 'Address2', 'Address3'],
         'latitude': [40.7128, 34.0522, 41.8781],
         'longitude': [-74.0060, -118.2437, -87.6298]
     }
     df = pd.DataFrame(data)

     # Convert to GeoDataFrame
     geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]
     gdf_addresses = gpd.GeoDataFrame(df, geometry=geometry)

     print(gdf_addresses.head())
     ```

### 5. **Check If Points Are Within the TIGER/Line Areas:**
   - Use the `within` method to check if each point is within the boundary:
     ```python
     # Ensure both GeoDataFrames use the same coordinate reference system (CRS)
     gdf_addresses = gdf_addresses.set_crs(gdf.crs, allow_override=True)

     # Iterate through each polygon in the TIGER/Line data
     for _, row in gdf.iterrows():
         # Get the geometry (polygon) of the current area
         polygon = row['geometry']

         # Check if each address is within the polygon
         gdf_addresses[f'in_{row["NAME"]}'] = gdf_addresses['geometry'].apply(lambda x: x.within(polygon))

     print(gdf_addresses.head())
     ```

   - This will add a new column to `gdf_addresses` indicating whether each point is inside the specific geographic area defined by the shapefile.

### 6. **Analyze the Results:**
   - You can then analyze or export the results as needed:
     ```python
     # Export to CSV or another format
     gdf_addresses.to_csv('output.csv', index=False)
     ```

### Summary:
- **Load the TIGER/Line shapefiles** into a GeoDataFrame using `geopandas`.
- **Load the address data** and convert it to a GeoDataFrame with `shapely.geometry.Point`.
- **Check if the points (addresses)** are within the boundaries defined by the shapefiles using the `within` method.

This approach allows you to programmatically determine whether specific latitude/longitude coordinates fall within a geographic area defined by TIGER/Line shapefiles.
```

## Embedding Comparison(s)

### Popular Models
* OpenAI models
  * 'text-embedding-3-small',
    * small, fast, quite nice
  * 'text-embedding-3-large',
    * larger, better accuracy, but significantly slower
  * 'text-embedding-ada-002'
    * old/outdated defacto-standard
* Open Source models
  * 


## Generative vs Extractive
https://haystack.deepset.ai/blog/generative-vs-extractive-models

### Reader-Retriever Haystack Pipeline
Their purely extractive property means the model can only provide answers that quote verbatim from a text. Abstraction, paraphrasing, and the formation of well-formed answers are not in the repertoire of this model family.

Because of their extractive nature, these models have no use for storing factual information, and therefore do not necessarily benefit from having more parameters. Compared to their generative cousins, extractive models are therefore usually much smaller in size and require less training data.

## Use cases / contexts
**Semantic search** seems most _trustworthy_ at the moment. Generative ML/AI is quite impressive, but ultimately the challenge of hallucinations makes it difficult to rely on. 

**Summaraization & classification** also do well for those use cases that benefit from either/both.

**RAG** has great potential if it is possible to get good initial `retrieval`, otherwise GIGO

**ChatBots** are nice and flashy, but so far it is tough to show actual benefit in many cases.

### Semantic Search
**Brute-force/development:**
* decompose corpus into documents and (likely) document segments.
* embed and store document vectors
* get query 
  * embed it
  * send to storage for filtering and/or search
    * NOTE: pay attention to scoring method of the embedding model
    * e.g. cosine, doc-product,...
  * development mode: in memory doc store, compare all docs
  * production mode: use vector-db

**More Elegant:**
* Retriever-Reader
  * https://haystack.deepset.ai/tutorials/03_scalable_qa_system (old version)
  * these pipelines tend to be shorter/more terse than RAG (see below)


### RAG (retrieval augmented generation)
Often: quick/light sparse keyword search (solr, elastic, ... BM25/tf-idf).  
Aim is to find most 'relevant' documents already indexed, and add them to the prompt to the LLM.  
LLM is trained on... large language... and uses that training to analyze the prompt-content (prompt stuffing) and combines the training with the 'new' content in the prompt to return delicious peanutbutter cups. 
**Almost** like micro-training the LLM on new documents. 


### Summarization


### Classification


### General chatbot




## Notes / ToDo
https://haystack.deepset.ai/tutorials/03_scalable_qa_system
```from haystack import Pipeline
from haystack.nodes import TextConverter, PreProcessor

indexing_pipeline = Pipeline()
text_converter = TextConverter()
preprocessor = PreProcessor(
    clean_whitespace=True,
    clean_header_footer=True,
    clean_empty_lines=True,
    split_by="word",
    split_length=200,
    split_overlap=20,
    split_respect_sentence_boundary=True,
)
```
