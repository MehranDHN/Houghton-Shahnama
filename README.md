# Shah Tahmasp Shahnama (Houghton) Ontology and Controlled Vocabulary

## Overview

This repository hosts the first version of a custom ontology and controlled vocabulary for describing Persian manuscripts, with a focus on the dispersed Houghton Shahnama (Shah Tahmasp Shahnama). The ontology is designed to cover aspects such as manuscript structure, folios (equivalent to IIIF Canvases), miniature paintings, narrative sequences, agential roles, and cultural specifics. It is built on CIDOC-CRM for compatibility with Linked Art and LOUD principles, enabling reconciliation with AAT, TGN, and Wikidata.

The controlled vocabulary provides a minimal set of terms for classifying folio types (e.g., Painting, Colophon), which can be associated with folios via the `:hasFolioType` property.

This initial release includes:
- The ontology in Turtle (TTL) format.
- A standalone controlled vocabulary (`folio-types-controlled-vocabularies.ttl`) as part of the ontology.
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
SELECT ?folio ?typeLabel ?sequence ?episodeLabel ?character
WHERE {
  ?folio a pmo:Folio ;
         pmo:hasFolioType ?type ;
         pmo:sequencePosition ?sequence ;
         pmo:hasRecto|pmo:hasVerso ?painting .
  ?type skos:prefLabel ?typeLabel .
  ?painting pmo:depictsScene ?episode ;
            pmo:depictsCharacter ?char .
  ?episode rdfs:label ?episodeLabel .
  ?char crm:P2_has_type ?character .
  FILTER (?type = pmo:Painting)
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
      "folio_sequence": 22,
      "folio_side": "v",
      "folio_type" : ["mdhn:Painting"], 
      "date": "ca. 1525",
      "medium": "Opaque watercolor, ink, silver, and gold on paper",
      "dimensions": "Painting: 9 1/2 x 9 1/16 in. (24.1 x 23 cm); Page: 18 1/2 x 12 1/2 in. (47 x 31.8 cm)",
      "location": "Metropolitan Museum of Art, New York"
    },
    "description": "Depicts the ancient festival of Sada with fire and celebration; attributed to Sultan Muhammad."
  },
  {
    "title": "Folio 265v: Combat of Giv and Kamus",
    "source_url": "https://cudl.lib.cam.ac.uk/view/MS-ADD-02702/1",
    "metadata": {
      "accession": "78.121",
      "folio_sequence": 265,
      "folio_side": "v",
      "folio_type" : ["mdhn:Painting"],
      "date": "ca. 1525-1535",
      "medium": "Ink, opaque watercolor, and gold on paper",
      "dimensions": "Approx. 47.31 × 32.07 cm",
      "location": "Virginia Museum of Fine Arts"
    },
    "description": "This painting depicts the combat between the Iranian hero Giv and Kamus of Kashan. It shows the moment when, surrounded by their opposing armies, Giv’s lance was “cleaved obliquely like a pen."
  },
  {
    "title": "Folio 23v: Tahmuras Defeats the Divs",
    "source_url": "https://www.metmuseum.org/art/collection/search/452112",
    "metadata": {
      "accession": " 1970.301.3",
      "folio_sequence": 23,
      "folio_side": "v",
      "folio_type" : ["mdhn:Painting"],
      "date": "ca. 1525",
      "medium": "Opaque watercolor, ink, silver, and gold on paper",
      "dimensions": "Painting: 9 1/2 x 9 1/16 in. (24.1 x 23 cm); Page: 18 1/2 x 12 1/2 in. (47 x 31.8 cm)",
      "location": "Metropolitan Museum of Art, New York"
    },
    "description": "Tahmuras, shown here galloping across a meadow, defeated the divs (demons); in exchange for their lives, they taught him the art of writing. This work is attributed to Sultan Muhammad, the master painter and chief administrator of the first generation of artists of this manuscript"
  },  
  {
    "title": "Folio 241r: The Besotted Iranian Camp Attacked by Night",
    "source_url": "https://www.metmuseum.org/art/collection/search/452145",
    "metadata": {
      "accession": "1970.301.29",
      "folio_sequence": 241,
      "folio_side": "r",
      "folio_type" : ["mdhn:Painting"],
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
      "folio_sequence": 243,
      "folio_side": "v",
      "folio_type" : ["mdhn:Painting"],
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
      "folio_sequence": 248,
      "folio_side": "r",
      "folio_type" : ["mdhn:Painting"],
      "date": "ca. 1525",
      "medium": "Opaque watercolor, ink, and gold on paper",
      "dimensions": "Painting: 11 1/8 x 9 1/8 in. (28.3 x 23.2 cm); Page: 18 1/2 x 12 1/2 in. (47 x 31.8 cm)",
      "location": "Metropolitan Museum of Art, New York"
    },
    "description": "Combat scene; vengeance narrative."
  },
  {
    "title": "Folio 28v: The Nightmare of Zahhak",
    "source_url": "https://collections.qm.org.qa/en/objects/the-nightmare-of-zahhak-ms412007",
    "metadata": {
      "accession": "ms412007",
      "folio_sequence": 28,
      "folio_side": "v",
      "folio_type" : ["mdhn:Painting"],
      "highres_image": "https://minicomp.github.io/wax/img/derivatives/iiif/images/obj7/full/full/0/default.jpg",
      "date": "ca. 1525-1535",
      "medium": "Opaque watercolor, ink, and gold on paper",
      "dimensions": "47.2 × 32.1 cm cm",
      "location": "Qatar Museum"
    },
    "description": "The Nightmare of Zahhak"
  },
  {
    "title": "Folio 80v: Manuchihr Welcomes Sam but Orders War upon Mihrab",
    "source_url": "https://www.metmuseum.org/art/collection/search/452118",
    "metadata": {
      "accession": "1970.301.9",
      "folio_sequence": 80,
      "folio_side": "v",
      "folio_type" : ["mdhn:Painting"],
      "date": "ca. 1525",
      "medium": "Opaque watercolor, ink, silver, and gold on paper",
      "dimensions": "Painting: 9 1/2 x 9 1/16 in. (24.1 x 23 cm); Page: 18 1/2 x 12 1/2 in. (47 x 31.8 cm)",
      "location": "Metropolitan Museum of Art, New York"
    },
    "description": "Sam arrived at the imperial court and was received by Shah Manuchihr, who listened with admiration as he reported on the victories and adventures of the campaign"
  },
  {
    "title": "Folio 708v: The Angel Surush Rescues Khusrau Parviz",
    "source_url": "https://www.metmuseum.org/art/collection/search/452182",
    "metadata": {
      "accession": " 1970.301.73",
      "folio_sequence": 708,
      "folio_side": "v",
      "folio_type" : ["mdhn:Painting"],
      "date": "ca. 1530",
      "medium": "Opaque watercolor, ink, and gold on paper",
      "dimensions": "Painting: 11 x 9 in. (27.9 x 22.9 cm); Page: 18 1/2 x 12 1/2 in. (47 x 31.8 cm)",
      "location": "Metropolitan Museum of Art, New York"
    },
    "description": "Rescue scene with angel intervention."
  },
  {
    "title": "Folio 48v: Tur Beheads Iraj",
    "source_url": "https://www.cincinnatiartmuseum.org/art/explore-the-collection?id=24210695&title=Tur-Beheads-Iraj;-Page-from-a-Dispersed-copy-of-the-Shahnama-Book-of-Kings-by-Firdawsi",
    "metadata": {
      "accession": "1984.87",
      "folio_sequence": 48,
      "folio_side": "v",
      "folio_type" : ["mdhn:Painting"],
      "highres_image": "https://artsandculture.google.com/asset/tur-beheads-iraj-sultan-muhammad-iranian-attributed/IQGB-i0WnXtGxw",
      "date": "ca. 1530",
      "medium": "Ink, opaque watercolor, and gold on paper",
      "dimensions": "32.7 x 23.8 cm",
      "location": "Cincinnati Art Museum"
    },
    "description": "Earthly drunkenness scene; stylistic link to Houghton Shahnama."
  },
  {
    "title": "Folio 218r: Kay Khusraw Welcomed by his Grandfather, Kay Kaus, King of Iran",
    "source_url": "https://www.davidmus.dk/art-from-the-islamic-world/miniature-paintings/item/963?culture=en-us",
    "metadata": {
      "accession": "30/1988",
      "folio_sequence": 218,
      "folio_side": "r",
      "folio_type" : ["mdhn:Painting"],
      "highres_image": "https://catalog.cdn-davidmus.dk/storage/representations/proxy/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBdThFIiwiZXhwIjpudWxsLCJwdXIiOiJibG9iX2lkIn19--161d369b711d51196b776544384e49cc8dc6634b/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaDdCem9MWm05eWJXRjBTU0lJYW5CbkJqb0dSVlE2RkhKbGMybDZaVjkwYjE5c2FXMXBkRnNIYVFJQUNta0NBQW89IiwiZXhwIjpudWxsLCJwdXIiOiJ2YXJpYXRpb24ifX0=--2fb0a7ed0031bd5615b9bf0a5ecfe18c7e2c74ed/Copyright_the_David-Collection_Copenhagen_30-1988_photo_Pernille_Klemp_web.jpg",
      "date": "ca. 1530",
      "medium": "Ink, opaque watercolor, and gold on paper",
      "dimensions": "47.6 x 32.1 cm",
      "location": "David Museum"
    },
    "description": "The scene is enacted at the court of Kay Kaus. He is seated on his throne together with his grandson, Kay Khusraw, who has just returned from Turan, where he grew up in secrecy after his father, good Prince Siyawush, was killed."
  },
  {
    "title": "Folio 521v: Haftvad and the Worm",
    "source_url": "https://collections.agakhanmuseum.org/collection/artifact/story-haftvad-and-the-worm-akm164",
    "metadata": {
      "accession": "AKM155",
      "folio_sequence": 521,
      "folio_side": "v",
      "folio_type" : ["mdhn:Painting"],
      "date": "ca. 1530",
      "medium": "Ink, opaque watercolor, and gold on paper",
      "dimensions": "46.8 x 32.3 cm",
      "location": "Agakhan Museum"
    },
    "description": "It has been argued that “The Death of Zahhak” dates to around 1535 and is Sultan Muhammad’s last contribution to the Shahnameh (Book of Kings) of Shah Tahmasp (folio 37 verso). By the mid-1530s, the style of Safavid court painting had matured, and some of the hallmarks of Sultan Muhammad’s own idiom had evolved. "
  },
  {
    "title": "Folio 25v: The Death of King Mirdas",
    "source_url": "https://www.khalilicollections.org/collections/islamic-art/khalili-collection-islamic-art-the-death-of-king-mirdas-mss1030-folio25/",
    "metadata": {
      "accession": "MSS 1030, folio 25v",
      "folio_sequence": 25,
      "folio_side": "v",
      "folio_type" : ["mdhn:Painting"],
      "date": "ca. 1530",
      "medium": "Ink, opaque watercolor, and gold on paper",
      "dimensions": "23.3 x 17.5 cm",
      "location": "Khalili Collection"
    },
    "description": "The Death of King Mirdas’, Folio 25 from the Shahnamah of Shah Tahmasp"
  },
  {
    "title": "Folio 25r: The Death of King Mirdas",
    "source_url": "https://www.khalilicollections.org/collections/islamic-art/khalili-collection-islamic-art-the-death-of-king-mirdas-mss1030-folio25/",
    "metadata": {
      "accession": "MSS 1030, folio 25r",
      "folio_sequence": 25,
      "folio_side": "r",
      "folio_type" : ["mdhn:Illuminated_Heading_Text"],
      "date": "ca. 1530",
      "medium": "Ink, opaque watercolor, and gold on paper",
      "dimensions": "27 x 17.1 cm",
      "location": "Khalili Collection"
    },
    "description": "The Death of King Mirdas’, Folio 25 from the Shahnamah of Shah Tahmasp"
  }
]
```
## Scoped Controlled Vocabularies
Despite the lack of standard global controlled vocabulary related to numerous folio types in Persian manuscripts this controlled vocabulary provides a minimal set of terms for classifying folio types (e.g., Painting, Colophon), which can be associated with folios via the :hasFolioType property. A standalone minimal version of this vocabulary is included to ensure precise classification of folio functions in Persian manuscripts.
However there is a complete version in `KG4OPennResources` project that can be refrenced later.

```turtle
@prefix : <http://mehrandhn.org/pmo#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix crm: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix mdhn: <http://mehrandhn.org/pmo#> .


# Controlled Vocabulary for Folio Types (Standalone Minimal Scheme)
:FolioTypeScheme a skos:ConceptScheme ;
    rdfs:label "Folio Type Vocabulary" ;
    rdfs:comment "A minimal controlled vocabulary for classifying types of folios in Persian manuscripts, such as covers, paintings, etc. Each Folio can have one or more types." ;
    dct:creator "Houghton Shahnama Project" .

:Cover a :FolioType ;
    skos:prefLabel "Cover"@en ;
    skos:definition "The protective outer layer or binding of the manuscript."@en ;
    skos:inScheme :FolioTypeScheme .

:IlluminatedOpeningPage a :FolioType ;
    skos:prefLabel "Illuminated Opening Page"@en ;
    skos:definition "A frontispiece or opening folio with elaborate illumination, such as a shamsa (rosette) or sarlauh (headpiece) in Persian manuscripts."@en ;
    skos:inScheme :FolioTypeScheme .

:OwnersAnnotation a :FolioType ;
    skos:prefLabel "Owners Annotation"@en ;
    skos:definition "A folio containing notes, seals, or inscriptions from previous owners (e.g., ex libris or provenance marks)."@en ;
    skos:inScheme :FolioTypeScheme .

:Painting a :FolioType ;
    skos:prefLabel "Painting"@en ;
    skos:definition "A folio featuring a primary miniature painting or illustration."@en ;
    skos:inScheme :FolioTypeScheme .

:Illumination a :FolioType ;
    skos:prefLabel "Illumination"@en ;
    skos:definition "A folio with decorative elements like goldwork, borders, or marginal illuminations, often without a central painting."@en ;
    skos:inScheme :FolioTypeScheme .

:Colophon a :FolioType ;
    skos:prefLabel "Colophon"@en ;
    skos:definition "A folio with the scribe's note at the end, including details like date, place, and creator."@en ;
    skos:inScheme :FolioTypeScheme .

:Flyleaf a :FolioType ;
    skos:prefLabel "Flyleaf"@en ;
    skos:definition "Blank or minimally decorated pages at the beginning or end of the manuscript (also known as fly pages or endpapers)."@en ;
    skos:inScheme :FolioTypeScheme .

# Additional minimal types for completeness in Persian manuscripts
:Finispiece a :FolioType ;
    skos:prefLabel "Finispiece"@en ;
    skos:definition "An illuminated closing page or tailpiece at the end of the manuscript."@en ;
    skos:inScheme :FolioTypeScheme .

:TextFolio a :FolioType ;
    skos:prefLabel "Text Folio"@en ;
    skos:definition "A standard folio primarily containing calligraphic text without major illustrations."@en ;
    skos:inScheme :FolioTypeScheme .

:Illuminated_Text a :FolioType ;
    skos:prefLabel "Illuminated Text"@en ;
    skos:definition "Illuminated Heading Text folio primarily containing calligraphic text with major illumination"@en ;
    skos:inScheme :FolioTypeScheme .  

:Illuminated_Heading_Text a :FolioType ;
    skos:prefLabel "Illuminated Heading Text folio primarily containing calligraphic text with major illumination and heading."@en ;
    skos:inScheme :FolioTypeScheme .   
```

## License

This ontology and vocabulary are released under CC0 1.0 Universal (CC0 1.0) Public Domain Dedication. Attribute sources for original resources.

## Contributions

Fork and PR for extensions. Issues for bugs/suggestions. Contact for collaboration on full metadata population.

---
*Generated on Sep 15, 2025, by **MehranDHN**, powered by: Grok 3 (xAI).*
