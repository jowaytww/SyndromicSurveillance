# Geographic Monitoring for Early Disease Detection (GeoMEDD)

## Disclosure
This analytical engine is in active development.

## What this program does
This project leverages a spatial database and two types of clustering algorithms to identify emerging  patterns of COVID-19 patients that local healthcare providers and health departments can use for rapid response and resource deployment efforts.  See https://www.researchsquare.com/article/rs-39862/v1 for a detailed discussion of the project.

## How to use the program
Spatio-temporal analysis assumes continuous availability of consecutive cases assessed in multiple look-back time periods. Consequently, the project is only limited by source data latency and could be operationalized to provide localities near real time results.

Hierarchical agglomerative and density based (DBSCAN) clustering algorithms are utilized.  Three cluster types are discussed - sentinel, micro, and neighborhood - defined by the number of members within pre-specified proximity.  Since cluster identification is defined solely by case proximity, the program is scalable for any sized geography.

## Technical requirements
The programs are Jupyter notebooks of Python code.  It requires a spatial database to pre-process patient data and integrate sources of important descriptive and/or predictive features; and a geocoding engine to map addresses to appropriate lon/lat coordinates.  The python program reads .csv files for analysis and outputs .csv files that can be consumed by the user's preferred visualization tool.  Supplementing visualization with additional geospatial data layers give clusters context and aid interpretability.

## How to use the program
The program accommodates a single cluster definition.  Consequently, it must be executed for each input file with its corresponding code modifications.

1. Generate the appropriate .csv input file with desired look back period for each cluster.
2. Modify the program with the correct file path
3. Set the minneighbors and maxdistance parameters
4. Repeat for each cluster type file

## Output data
Cluster results are generated both as convex hull polygons and as line shape objects to accommodate different visualization tool requirements.

## Preferred Reference for Citation
Geographic Monitoring for Early Disease Detection (GeoMEDD) Code Repository. Developer Documentation [Internet]. 2020. Available from: https://github.com/JayakrishnanAjayakumar/SyndromicSurveillance.
