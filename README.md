# Shah Tahmasp Shahnama (Houghton) Ontology and Controlled Vocabulary

## Overview

This repository hosts the first version of a custom ontology and controlled vocabulary for describing Persian manuscripts, with a focus on the dispersed Houghton Shahnama (Shah Tahmasp Shahnama). The ontology is designed to cover aspects such as manuscript structure, folios (equivalent to IIIF Canvases), miniature paintings, narrative sequences, agential roles, and cultural specifics. It is built on CIDOC-CRM for compatibility with Linked Art and LOUD principles, enabling reconciliation with AAT, TGN, and Wikidata.

The controlled vocabulary provides a minimal set of terms for classifying folio types (e.g., Painting, Colophon), which can be associated with folios via the `:hasFolioType` property.

This initial release includes:
- The ontology in Turtle (TTL) format.
- A standalone controlled vocabulary as part of the ontology.
- Sample RDF data for a few folios.
- SPARQL query examples for demonstration.
- A JSON catalog (`catalog.json`) of resources (folios and paintings) to be considered for integration and upload to Internet Archive (IA). This catalog is partial and focuses on publicly accessible digitized folios; expand it as needed.

The project aims to facilitate a virtual reconstruction of the manuscript using IIIF, with metadata in RDF for LOD interoperability.

## Repository Structure Recommendations

For the first version, keep the structure simple and focused on the ontology and vocabulary. As the project grows, add metadata for individual folios and IIIF manifests. Use Git for version control, with semantic versioning (e.g., v1.0.0 for this release).

Recommended file structure:

```
houghton-shahnama-ontology/
├── ontology/
│   └── persian-manuscript-ontology.ttl  # Core ontology and controlled vocabulary in Turtle
├── examples/
│   ├── sample-folio-rdf/
│   │   ├── folio-22v.ttl  # Sample RDF for "The Feast of Sada" (Folio 22v)
│   │   ├── folio-61b.ttl  # Sample for "Birth of Zal" (Folio 61b)
│   │   └── folio-248r.ttl # Sample for "Giv Avenges Bahram" (Folio 248r)
│   └── sparql-queries/
│       ├── query-folios-by-type.sparql   # Example SPARQL files
│       ├── query-artist-attributions.sparql
│       └── query-narrative-sequences.sparql
├── resources/
│   └── catalog.json  # JSON catalog of resources for IA integration
├── docs/
│   ├── ontology-documentation.md  # Detailed docs on classes, properties, and usage
│   └── reconciliation-guide.md   # Guide for mapping to AAT/TGN/Wikidata
├── LICENSE  # CC0 1.0 for metadata/ontology
├── README.md  # This file
└── .gitignore
```

- **/ontology**: Core TTL file. Use Protégé for editing/validation.
- **/examples**: Sample data and queries to demonstrate usage. Load into a triple store like Apache Jena Fuseki for testing.
- **/resources**: The JSON catalog for folios/resources. This serves as an index for gathering originals before creating IIIF manifests and uploading to IA.
- **/docs**: Supplementary Markdown docs for usability (LOUD compliance).
- **Future Expansions**: Add `/metadata` for full RDF per folio, `/iiif` for manifests/collections, and `/scripts` for automation (e.g., Python with RDFLib for generating RDF from CSV).

Publish as a public GitHub repo (e.g., github.com/MehranDHN/houghton-shahnama-ontology). Use GitHub Pages for a simple site hosting docs and a SPARQL endpoint demo if possible.

## Usage

1. **Load the Ontology**: Import `persian-manuscript-ontology.ttl` into tools like Protégé or RDF stores.
2. **Reconciliation**: Use OpenRefine to map properties (e.g., `:materials` to AAT URIs).
3. **Querying**: Set up a local SPARQL endpoint with Fuseki. Load samples and run queries.
4. **JSON Catalog**: Use `catalog.json` to script downloads/IIIF imports. For IA, adapt metadata to DC/MODS and upload images with IIIF support.
5. **Extensions**: For full project, generate IIIF Collection JSON linking to external manifests (e.g., Met's IIIF endpoints).

## SPARQL Query Examples

Below are example SPARQL queries demonstrating query possibilities. Assume the ontology namespace `@prefix pmo: <http://MehranDHN.org/pmo#> .` and samples loaded. These can be run in a tool like Fuseki or Yasgui.

### 1. Retrieve All Folios by Type (e.g., Paintings)
```
PREFIX pmo: <http://MehranDHN.org/pmo#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?folio ?typeLabel ?sequence
WHERE {
  ?folio a pmo:Folio ;
         pmo:hasFolioType ?type ;
         pmo:sequencePosition ?sequence .
  ?type skos:prefLabel ?typeLabel .
  FILTER (?type = pmo:Painting)  # Change to other types like pmo:Colophon
}
ORDER BY ?sequence
```
- **Purpose**: Lists folios classified as "Painting", with sequence for reconstruction.
- **Expected Output** (with samples): Folio 22v ("Painting", sequence 22), Folio 61b ("Painting", sequence 61).

### 2. Find Folios Attributed to a Specific Artist
```
PREFIX pmo: <http://MehranDHN.org/pmo#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?folio ?painting ?artistLabel ?scene
WHERE {
  ?folio a pmo:Folio ;
         pmo:hasRecto|pmo:hasVerso ?painting .
  ?painting a pmo:MiniaturePainting ;
            pmo:attributedTo ?artist ;
            pmo:depictsScene ?episode .
  ?episode rdfs:label ?scene .
  ?artist rdfs:label ?artistLabel .
  FILTER (CONTAINS(?artistLabel, "Sultan Muhammad"))  # Example artist
}
```
- **Purpose**: Queries for attributions, useful for agential analysis in Safavid art.
- **Expected Output**: Folios like 22v attributed to Sultan Muhammad, depicting "The Feast of Sada".

### 3. Retrieve Narrative Sequences and Depicted Characters
```
PREFIX pmo: <http://MehranDHN.org/pmo#>
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?folio ?sequence ?episodeLabel ?character
WHERE {
  ?folio a pmo:Folio ;
         pmo:sequencePosition ?sequence ;
         pmo:hasRecto|pmo:hasVerso ?painting .
  ?painting pmo:depictsScene ?episode ;
            pmo:depictsCharacter ?char .
  ?episode rdfs:label ?episodeLabel .
  ?char crm:P2_has_type ?character .  # Reconciled to Wikidata/AAT
}
ORDER BY ?sequence
```
- **Purpose**: Traces Shahnama narrative across folios, linking to characters (e.g., Zal via Wikidata).
- **Expected Output**: Folio 61b (sequence 61, "Birth of Zal", character "Zal").

### 4. List Folios by Current Location (Reconciled to TGN)
```
PREFIX pmo: <http://MehranDHN.org/pmo#>

SELECT ?folio ?location ?description
WHERE {
  ?folio a pmo:Folio ;
         pmo:currentLocation ?loc ;
         rdfs:comment ?description .  # Optional desc
  ?loc rdfs:label ?location .
  FILTER (?loc = <http://vocab.getty.edu/tgn/7007567>)  # New York (Met)
}
```
- **Purpose**: Filters by provenance/location for dispersal tracking.
- **Expected Output**: Met folios in New York.

These examples showcase sequence handling, agential/subject queries, and reconciliation. For production, host a SPARQL endpoint and add more complex queries (e.g., with GRAPH for federated data).

## JSON Catalog of Resources

The `catalog.json` file in `/resources` is a starting point for cataloging dispersed folios. It includes publicly digitized ones from major institutions. Each entry has:
- `title`: Descriptive title (e.g., "Folio X: Scene").
- `source_url`: URL to the publisher's page/digital object.
- `metadata`: Object with min fields like accession, date, medium, dimensions, location.
- `description`: Optional narrative/scene/provenance info.

This is partial (focusing on ~20 known folios); expand via scripts scraping Met API, Cambridge DL, etc. Use it to fetch resources for IIIF integration and IA upload (adapt to IA's metadata requirements).

Sample `catalog.json` content (as JSON string for illustration; save as file):

```json
[
  {
    "title": "Folio 22v: The Feast of Sada",
    "source_url": "https://www.metmuseum.org/art/collection/search/452111",
    "metadata": {
      "accession": "1970.301.2",
      "date": "ca. 1525",
      "medium": "Opaque watercolor, ink, silver, and gold on paper",
      "dimensions": "Painting: 9 1/2 x 9 1/16 in. (24.1 x 23 cm); Page: 18 1/2 x 12 1/2 in. (47 x 31.8 cm)",
      "location": "Metropolitan Museum of Art, New York"
    },
    "description": "Depicts the ancient festival of Sada with fire and celebration; attributed to Sultan Muhammad."
  },
  {
    "title": "Folio 61b: Birth of Zal",
    "source_url": "https://cudl.lib.cam.ac.uk/view/MS-ADD-02702/1",
    "metadata": {
      "accession": "MS Add.2702",
      "date": "ca. 1525-1535",
      "medium": "Ink, opaque watercolor, and gold on paper",
      "dimensions": "Approx. 47 x 32 cm",
      "location": "Cambridge University Library"
    },
    "description": "Scene of Zal's birth, with simurgh; part of Aga Khan Collection."
  },
  {
    "title": "Folio 241r: The Besotted Iranian Camp Attacked by Night",
    "source_url": "https://www.metmuseum.org/art/collection/search/452145",
    "metadata": {
      "accession": "1970.301.29",
      "date": "ca. 1525",
      "medium": "Opaque watercolor, ink, and gold on paper",
      "dimensions": "Painting: 11 x 9 in. (27.9 x 22.9 cm); Page: 18 1/2 x 12 1/2 in. (47 x 31.8 cm)",
      "location": "Metropolitan Museum of Art, New York"
    },
    "description": "Night attack scene from Turano-Iranian wars."
  },
  {
    "title": "Folio 243v: The Battle of Pashan Begins",
    "source_url": "https://www.metmuseum.org/art/collection/search/452146",
    "metadata": {
      "accession": "1970.301.30",
      "date": "ca. 1525",
      "medium": "Opaque watercolor, ink, and gold on paper",
      "dimensions": "Painting: 11 1/4 x 9 1/8 in. (28.6 x 23.2 cm); Page: 18 1/2 x 12 1/2 in. (47 x 31.8 cm)",
      "location": "Metropolitan Museum of Art, New York"
    },
    "description": "Battle commencement with warriors."
  },
  {
    "title": "Folio 248r: Giv Avenges Bahram by Slaying Tazhav",
    "source_url": "https://www.metmuseum.org/art/collection/search/452148",
    "metadata": {
      "accession": "1970.301.32",
      "date": "ca. 1525",
      "medium": "Opaque watercolor, ink, and gold on paper",
      "dimensions": "Painting: 11 1/8 x 9 1/8 in. (28.3 x 23.2 cm); Page: 18 1/2 x 12 1/2 in. (47 x 31.8 cm)",
      "location": "Metropolitan Museum of Art, New York"
    },
    "description": "Combat scene; vengeance narrative."
  },
  {
    "title": "Bifolio: S1986.102a-d",
    "source_url": "https://asia.si.edu/object/S1986.102a-d/",
    "metadata": {
      "accession": "S1986.102a-d",
      "date": "ca. 1525-1535",
      "medium": "Opaque watercolor, ink, and gold on paper",
      "dimensions": "Approx. 47 x 32 cm",
      "location": "Freer Gallery of Art, Smithsonian"
    },
    "description": "Text and illumination; brotherhood scene between Turanians and Iranians."
  },
  {
    "title": "Double-Page Frontispiece: 1945.169",
    "source_url": "https://www.clevelandart.org/art/1945.169",
    "metadata": {
      "accession": "1945.169",
      "date": "ca. 1525-1530",
      "medium": "Opaque watercolor, ink, and gold on paper",
      "dimensions": "47.5 x 32.5 cm",
      "location": "Cleveland Museum of Art"
    },
    "description": "Illuminated frontispiece with courtly scenes."
  },
  {
    "title": "Folio 37v: Scene from Shahnama",
    "source_url": "https://quod.lib.umich.edu/i/icmc1ic/x-icmc001/ICMC001",
    "metadata": {
      "accession": "ICMC001",
      "date": "ca. 1525",
      "medium": "Ink, watercolor, gold on paper",
      "dimensions": "Unknown",
      "location": "University of Michigan Museum of Art"
    },
    "description": "Narrative illustration; dispersed from Houghton."
  },
  {
    "title": "Folio 708v: The Angel Surush Rescues Khusrau Parviz",
    "source_url": "https://www.metmuseum.org/art/collection/search/452210",
    "metadata": {
      "accession": "1970.301.76",
      "date": "ca. 1530",
      "medium": "Opaque watercolor, ink, and gold on paper",
      "dimensions": "Painting: 11 x 9 in. (27.9 x 22.9 cm); Page: 18 1/2 x 12 1/2 in. (47 x 31.8 cm)",
      "location": "Metropolitan Museum of Art, New York"
    },
    "description": "Rescue scene with angel intervention."
  },
  {
    "title": "Folio from Divan of Hafiz (related to Shahnama style): 1988.460.2",
    "source_url": "https://harvardartmuseums.org/collections/object/165247",
    "metadata": {
      "accession": "1988.460.2",
      "date": "ca. 1530",
      "medium": "Ink, opaque watercolor, and gold on paper",
      "dimensions": "Unknown",
      "location": "Harvard Art Museums"
    },
    "description": "Earthly drunkenness scene; stylistic link to Houghton Shahnama."
  }
]
```

## License

This ontology and vocabulary are released under CC0 1.0 Universal (CC0 1.0) Public Domain Dedication. Attribute sources for original resources.

## Contributions

Fork and PR for extensions. Issues for bugs/suggestions. Contact for collaboration on full metadata population.
