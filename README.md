# LIDD: Linked Interdisciplinary Data Discovery

What does Linked Data mean? What are its foundations: standards or
relationships? Ultimately I want to pursue any way to link data together.
Standards are being regarded as unimportant, though present in design
considerations. 

## Rediscovering what really matters

This project is currently at the prototype stage. I've created functionality
to ingest [ICPSR](https://www.icpsr.umich.edu/icpsrweb/landing.jsp) metadata
into a MongoDB database. I extract "normal" fields from the ICPSR metadata
and "normalize" them. So far we have extracted the title field, which we could
use directly from its native form, and extracted time information if available
and constructed `start_datetime` and `end_datetime`.


### Quickstart

```bash
git clone https://github.com/mtpain/rda-lod
```

#### Install dependencies

```bash
cd rda-lod
pip install -r requirements.txt
```

Using [homebrew](http://brew.sh), install MongoDB if you don't already have it installed

```bash
brew install mongodb
```

Follow the instructions to start MongoDB and start the server on computer startup as well.

#### Initialize the ICPSR Mongo Store

First step, unzip `icpsr-ddi-metadata.tar.gz` to whichever directory you choose.
Probably you'll just want to run

```bash
tar -xvf icpsr-ddi-metadata.tar.gz
```

Now we insert that metadata into its Mongo collection form.

First, start an iPython Flask web app shell

```bash
$ python manage.py shell
```

Then run the following commands

```python
import glob
from parsers.icpsr import make_normalized_icpsr

glb = glob.glob('icpsr-ddi-metadata/*')

for g in glb:
    nmd = make_normalized_icpsr(g)
    nmd.save() 
```

It should complete without complaint. One way to check this worked is to start
up a mongo shell (just type `mongo`) and run

```javascript
> use rda_lod
> db.normalized_metadata.count()
```

It should be 9667, the total number of metadata documents in that archive.


Now, run `startup.py`

```bash
./startup.py
```

and navigate to http://localhost:8000 to see the app in its current form.
