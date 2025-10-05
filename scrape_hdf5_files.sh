#!/bin/bash

# Script to scrape HDF5 files from OOI RSN DAS data server
# URL: http://piweb.ooirsn.uw.edu/das24/data/

set -e  # Exit on any error

BASE_URL="http://piweb.ooirsn.uw.edu/das24/data/"
LOCAL_DIR="./das24_data"

echo "Starting HDF5 file scraping from ${BASE_URL}"
echo "Files will be saved to: ${LOCAL_DIR}"

# Create local directory if it doesn't exist
mkdir -p "${LOCAL_DIR}"

# Use wget to recursively download HDF5 files
# Options explained:
# -r, --recursive: Enable recursive downloading
# -np, --no-parent: Don't ascend to parent directory
# -nH, --no-host-directories: Don't create hostname directory
# --cut-dirs=2: Remove 2 directory levels from path (removes /das24/data/)
# -A: Accept only files with these extensions
# -P: Directory prefix where files will be saved
# --no-clobber: Don't overwrite existing files
# --progress=bar: Show progress bar
# -e robots=off: Ignore robots.txt
# --wait=1: Wait 1 second between requests to be respectful to the server
# --random-wait: Use random wait times (0.5-1.5 * wait time)

wget \
    --recursive \
    --no-parent \
    --no-host-directories \
    --cut-dirs=2 \
    --accept="*.hdf5,*.h5,*.hdf,*.HDF5,*.H5,*.HDF" \
    --directory-prefix="${LOCAL_DIR}" \
    --no-clobber \
    --progress=bar \
    --execute robots=off \
    --wait=1 \
    --random-wait \
    --continue \
    --timeout=30 \
    --tries=3 \
    "${BASE_URL}"

echo ""
echo "Download complete!"
echo "Files saved to: ${LOCAL_DIR}"
echo ""
echo "Summary of downloaded files:"
find "${LOCAL_DIR}" -type f \( -name "*.hdf5" -o -name "*.h5" -o -name "*.hdf" -o -name "*.HDF5" -o -name "*.H5" -o -name "*.HDF" \) | wc -l | xargs echo "Total HDF5 files:"
find "${LOCAL_DIR}" -type f \( -name "*.hdf5" -o -name "*.h5" -o -name "*.hdf" -o -name "*.HDF5" -o -name "*.H5" -o -name "*.HDF" \) -exec du -ch {} + | tail -1