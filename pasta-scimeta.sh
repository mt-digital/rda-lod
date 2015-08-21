#!/bin/bash

# Bash script to download EML science metadata from the LTER Network Information
# System (NIS)

all=0
dry=0
path="."
base_url="https://pasta.lternet.edu/package/"

usage()
{
cat << EOF

usage: $(basename $0) OPTIONS

Download the LTER EML science metadata available at https://pasta.lternet.edu

OPTIONS:
  -h Show this message
  -d Perform a dry run of this operation
  -a Include all revisions
  -s Add scope (not implemented)
  -i Add identifier (scope must also be set) (not implemented)
  -r Add revision (scope and identifier must also be set) (not implemented)
  -p Write files to this directory path

EOF
}

get_scopes()
{
  scopes=`curl -s -X GET ${base_url}eml`
}

get_identifiers() {
  identifiers=`curl -s -X GET ${base_url}eml/$1`
}

get_revisions()
{
  if [ $all -eq 1 ]; then
    revisions=`curl -s -X GET ${base_url}eml/$1/$2`
  else
    revisions=`curl -s -X GET ${base_url}eml/$1/$2?filter=newest`
  fi
}


while getopts "hdap:" OPTION
do
  case $OPTION in
    h) usage; exit 1;;
    d) dry=1;;
    a) all=1;;
    p) path=$OPTARG;;
    \?) usage; exit 1;;
  esac
  
  if [ ! -d $path ]; then
    echo "The directory path \"${path}\" does not exist!"
    exit 1
  fi
  
done

get_scopes

for s in $scopes; do
  get_identifiers $s
  for i in $identifiers; do
    get_revisions $s $i
    for r in $revisions; do
      packageid="$s/$i/$r"
      echo "Downloading $s.$i.$r to file: ${path}/$s-$i-$r.xml"
      if [ ! $dry -eq 1 ]; then
        curl -s -X GET ${base_url}metadata/eml/${packageid} > ${path}/$s-$i-$r.xml
      fi
    done
  done
done
  