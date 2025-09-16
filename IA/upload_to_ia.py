import requests
import json
import internetarchive
from internetarchive import configure, upload
import os  # For checking file existence

# Replace with your Internet Archive access and secret keys
access_key = 'YOUR_ACCESS_KEY_HERE'
secret_key = 'YOUR_SECRET_KEY_HERE'

# Configure the internetarchive library with your keys
#configure(access_key, secret_key)

# URL for the catalog JSON
catalog_url = 'https://raw.githubusercontent.com/MehranDHN/Houghton-Shahnama/refs/heads/main/resources/catalog.json'

# Fetch the JSON data
response = requests.get(catalog_url)
if response.status_code != 200:
    print(f"Failed to fetch catalog: {response.status_code} - {response.text}")
    exit(1)

catalog = response.json()

# Assuming the catalog is a list of dictionaries. Adjust the keys below based on the actual JSON structure.
# For example, expected keys per item: 'folio' (e.g., a number or ID), 'title', 'description', 'image' (filename of the local image).
# Inspect the catalog.json to confirm the exact keys and structure.
# You can print(catalog[0].keys()) to see available keys.

# Local folder where images are stored (change as needed)
local_folder = 'YOUR_LOCLA_FOLDER'  # e.g., '/path/to/your/local/folder/'
# Note: Your local files should be named like '1r.jpg', '1v.jpg', '2r.jpg', etc., matching folio_sequence and folio_side.

# Loop through each folio in the catalog
for item in catalog:
    # Create a unique identifier for the Internet Archive item (adjust based on JSON)
    folio_seq = str(item.get("metadata").get('folio_sequence', 'unknown'))  # Use 'folio' key or similar
    folio_side= str(item.get("metadata").get('folio_side', 'unknown')) 
    folio_id = f"{folio_seq}{folio_side}"
    description = item.get('description', 'No description available.')
    identifier = f'shahnama-shah-tahmasp-{folio_id}'.replace(' ', '-').lower()
    iif3Manifest  = 'https://iiif.archive.org/iiif/3/' +  identifier + '/manifest.json'
    miradorViewer = 'https://projectmirador.org/embed/?iiif-content=' + iif3Manifest 
    biblissimaViewer = 'https://iiif.biblissima.fr/mirador3/?iiif-content=' + iif3Manifest 
    glycerineViewer = 'https://demo.viewer.glycerine.io/viewer?iiif-content=' + iif3Manifest 
    glamLocation = str(item.get("metadata").get('location', 'unknown')) 
    # Prepare metadata (adjust keys and add more as needed from the item)
    metadata = {
        'title': item.get('title', f'Houghton Shahnama Folio {folio_id}'),
        'description': item.get('description', 'A folio from the Houghton Shahnama manuscript.'),
        'creator': 'MehranDHN',  # Author of Shahnama
        'mediatype': 'image',
        'collection': 'opensource_image', 
        'startdate' : '1522-01-01',
        'endtdate' : '1552-01-01',  
        'patron': 'Shah Tahmasp I',
        'wd_reference' : "wd:Q3114572",
        'see_also' : ["https://github.com/MehranDHN/Houghton-Shahnama", "https://wikidata.metaphacts.com/resource/wd:Q3114572"],
        'folio_sequence' : folio_seq,
        "folio_side" : folio_side,
        'folio_seq_side' : folio_id,
        'glamsource': glamLocation.strip(),           
        'iiif3-manifest' : iif3Manifest, 
        'mirador-viewer' : miradorViewer,
        'biblissima-viewer' : biblissimaViewer ,
        'glycerine-viewer' : glycerineViewer,
        'subject' : [
            'Illuminated manuscript',
            'Persian miniature painting',
            'Epic poetry',
            'Historical narrative',
            'Mythological art',
            'Royal patronage and political legitimacy',
            'Iranian national identity and mythology',
            'Cultural diplomacy and gift exchange',
            'Artistic fusion' , 'Tabriz schools',
            'Safavid court life' ,
            'Manuscript production' , 'Preservation',
            'Ferdowsi' ,
            'Shah Ismail I',
            'Shah Tahmasp I',
            'Sultan Muhammad ',
            'Aqa Mirak',
            'Mir Sayyid Ali' ,
            'Arthur Houghton Jr.' ,
            'Stuart Cary Welch' ,
            'Tabriz',
            'Istanbul/Topkapı Palace',
            'Metropolitan Museum of Art',
            'Tehran Museum of Contemporary Art',
            'Harvard Art Museums','Fogg Museum',
            'Safavid dynasty' '16th century',
            'Ottoman Empire' 
            'Timurid artistic legacy'
            'Tabriz Style miniatures'
            'Nastaliq calligraphy'    
            'Islamic art' , 'Persian literature'
            'Iconography of mythical motifs' 
            'cultural heritage' 
        ],
        'genre' : ['Persian Cultural Heritage Collection', 'Shahnama Shah Tahmasp'],
        'language': 'per',  # Persian
        # Add more metadata fields from item, e.g., 'date': item.get('date'), 'artist': item.get('artist')
    }

    # Assume 'image' key in JSON holds the filename; adjust if different
    image_filename = f"{folio_id}.jpg"  # Default to folio_id.jpg if not specified
    image_path = os.path.join(local_folder, image_filename)

    # Check if the image file exists locally
    if not os.path.exists(image_path):
        print(f"Image file not found for {identifier}: {image_path}")
        continue

    # Upload the file with metadata
    # Note: If a folio has multiple images, add them to a list in 'files'
    files = {image_filename: image_path}  # Can be a dict for multiple files
    try:
        response = internetarchive.upload(identifier, files=files, metadata=metadata, access_key=access_key, secret_key=secret_key, verbose=True)

        if response[0].status_code == 200:
            print(f"Successfully uploaded {identifier} to Internet Archive.")
        else:
            print(f"Failed to upload {identifier}. Responses: {[r.text for r in response]}")
    except Exception as e:
        print(f"Error uploading {identifier}: {str(e)}")