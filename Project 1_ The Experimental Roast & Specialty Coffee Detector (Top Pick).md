### **Project 1: The Experimental Roast & Specialty Coffee Detector (Top Pick)**

**Concept:** Bridge the gap between generic TikTok/Google Maps coffee listings and true specialty coffee roasters offering experimental processes (anaerobic, thermal shock, carbonic maceration).

* **APIs & Data Sources:**  
  1. **Coffee Beans & Processing Data:** **RoastDB API** or **LoffeeLabs Bean Base API** (free REST API endpoint querying \~10k specialty coffee beans with origin, roaster, and process fields). Alternatively, ingest open raw JSON extracts from **coffeeDB**.  
  2. **Location Data:** **Google Places API** or **Overpass API (OpenStreetMap)** to query coffee shops by lat/long bounding box.  
* **Pipeline Architecture:**  
  1. **Ingestion (dlt):** Fetch live bean payloads (filtering process types like anaerobic, experimental, natural) and map them against roaster location lists into **DuckDB**.  
  2. **dbt Transformation:**  
     * stg\_roasters & stg\_beans: Normalize processing names (e.g., standardizing "anaerobic fermentation", "co-ferment", "experimental" into a unified flag).  
     * fct\_specialty\_availability: Join local coffee shops with active roaster bean catalogs to compute a "Specialty Score" (ratio of experimental single-origins vs standard blends).  
  3. **Semantic Layer & Analytics:** Expose metrics.yaml with dimensions (roaster\_city, process\_category, flavor\_profile) and measures (experimental\_bean\_count).  
* **Why it Ships in 2 Hours:** Clear schema, zero complex OAuth required, and delivers a tangible product (e.g., "Find shops within 5 miles serving anaerobic coffees").

